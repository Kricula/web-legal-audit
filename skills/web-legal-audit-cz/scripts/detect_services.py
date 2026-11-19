#!/usr/bin/env python3
"""Bezpečná statická inventura známých služeb ve zdrojovém kódu webu.

Skript záměrně NEČTE soubory s konfigurací a tajnými údaji (.env, klíče,
certifikáty, credentials). Výstupní ukázky jsou navíc sanitizovány.
Použití: python3 scripts/detect_services.py CESTA [--format md|json]
Pouze standardní knihovna Pythonu 3.8+.
"""
import argparse
import json
import os
import re
import sys

PATTERNS = [
    ("Google Analytics 4", "analytické", r"gtag\(|['\"]G-[A-Z0-9]{6,}['\"]|google-analytics\.com|googletagmanager\.com/gtag", "ověřit souhlas a skutečné načítání"),
    ("Google Tag Manager", "správa tagů", r"GTM-[A-Z0-9]{4,}|googletagmanager\.com/gtm\.js|@next/third-parties", "zkontrolovat všechny tagy a consent podmínky"),
    ("Google Consent Mode", "nastavení souhlasu", r"gtag\(\s*['\"]consent['\"]", "ověřit default, update a blokování tagů"),
    ("Meta Pixel", "marketingové", r"fbq\(|connect\.facebook\.net|facebook\.com/tr", "ověřit předchozí souhlas a předávání údajů"),
    ("Hotjar", "analytické", r"hotjar\.com|\bhj\(", "ověřit souhlas, maskování a retenci"),
    ("Microsoft Clarity", "analytické", r"clarity\.ms", "ověřit souhlas a konfiguraci"),
    ("YouTube embed", "externí obsah", r"youtube\.com/embed|youtu\.be/", "ověřit načítání až po volbě uživatele / souhlasu"),
    ("YouTube nocookie", "externí obsah", r"youtube-nocookie\.com", "omezený režim sám o sobě neprokazuje soulad"),
    ("Vimeo", "externí obsah", r"player\.vimeo\.com", "ověřit parametry, cookies a načítání"),
    ("Google Maps", "externí obsah", r"maps\.googleapis\.com|google\.com/maps/embed|et_pb_map", "ověřit požadavky před souhlasem nebo aktivací"),
    ("Google Fonts", "externí zdroj", r"fonts\.googleapis\.com|fonts\.gstatic\.com", "vyhodnotit předávání IP a informační povinnost"),
    ("reCAPTCHA", "ochrana formuláře", r"recaptcha/api\.js|grecaptcha|google\.com/recaptcha", "posoudit nezbytnost, právní základ a informační povinnost"),
    ("Cloudflare Turnstile", "ochrana formuláře", r"challenges\.cloudflare\.com/turnstile", "ověřit konfiguraci a informační povinnost"),
    ("Smartsupp", "chat", r"smartsupp", "ověřit účely, dodavatele, cookies a retenci"),
    ("Intercom", "chat", r"intercom", "ověřit účely, dodavatele a případné předávání"),
    ("OpenAI / AI rozhraní", "AI", r"api\.openai\.com|\bopenai\b", "zjistit roli subjektu, účel a použitelná pravidla AI Act"),
    ("Anthropic / Claude", "AI", r"api\.anthropic\.com|anthropic", "zjistit roli subjektu, účel a použitelná pravidla AI Act"),
    ("Ecomail", "newsletter", r"ecomail", "ověřit právní základ a odhlášení"),
    ("Mailchimp", "newsletter", r"mailchimp|list-manage\.com", "ověřit právní základ, dodavatele a předávání"),
    ("MailerLite", "newsletter", r"mailerlite", "ověřit právní základ a odhlášení"),
    ("Brevo", "newsletter", r"brevo|sendinblue|sibforms", "ověřit právní základ a odhlášení"),
    ("Stripe", "platby", r"js\.stripe\.com|\bstripe\b", "ověřit roli dodavatele a tok platebních údajů"),
    ("GoPay", "platby", r"gopay", "ověřit roli dodavatele a tok platebních údajů"),
    ("Comgate", "platby", r"comgate", "ověřit roli dodavatele a tok platebních údajů"),
    ("Calendly", "rezervace", r"calendly\.com", "ověřit účely, dodavatele a případné předávání"),
    ("Contact Form 7", "formulář", r"contact-form-7|wpcf7", "ověřit ukládání, příjemce a dobu uchování"),
    ("WPForms / Gravity Forms", "formulář", r"wpforms|gravityforms|gform_", "ověřit ukládání, příjemce a dobu uchování"),
    ("Divi kontaktní formulář", "formulář", r"et_pb_contact_form", "ověřit ukládání, příjemce a dobu uchování"),
    ("WooCommerce", "e-shop", r"woocommerce", "provést modul e-shopu a checkoutu"),
    ("Complianz", "správa souhlasů", r"complianz", "ověřit reálné blokování a záznam souhlasu"),
    ("Cookiebot", "správa souhlasů", r"cookiebot", "ověřit reálné blokování a záznam souhlasu"),
    ("CookieYes", "správa souhlasů", r"cookieyes|cookie-law-info", "ověřit reálné blokování a záznam souhlasu"),
    ("ODR platforma", "spotřebitelské informace", r"ec\.europa\.eu/consumers/odr", "ověřit a odstranit zastaralý odkaz; platforma ukončila činnost"),
]

SKIP_DIRS = {".git", "node_modules", "vendor", ".next", "dist", "build", ".cache", "__pycache__", ".svn", "coverage", ".turbo", ".vercel", "wp-admin", "wp-includes", "secrets", "credentials", ".ssh", ".aws", "certs", "certificates"}
SKIP_NAMES = {".env", ".env.local", ".env.production", ".env.development", ".env.test", "id_rsa", "id_ed25519", "known_hosts", "credentials", "secrets.json", "service-account.json"}
SKIP_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".crt", ".cer", ".der", ".keystore", ".jks", ".sqlite", ".db")
TEXT_EXT = {".html", ".htm", ".php", ".phtml", ".twig", ".latte", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".json", ".liquid", ".hbs", ".njk", ".ejs", ".md", ".mdx", ".py", ".rb", ".xml", ".yml", ".yaml", ".css", ".scss"}
MAX_BYTES = 2_000_000
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|passwd|authorization|client[_-]?secret)(\s*[:=]\s*)([\"'])(.*?)\3"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password|passwd|authorization|client[_-]?secret)(\s*[:=]\s*)([^\s,;\"']+)"),
    re.compile(r"(?i)\b(sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16})\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]+=*"),
]


def is_sensitive_file(name):
    low = name.lower()
    return low in SKIP_NAMES or low.startswith(".env") or low.endswith(SKIP_SUFFIXES) or "secret" in low or "credential" in low


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if is_sensitive_file(name) or name.lower().endswith(".min.js"):
                continue
            path = os.path.join(dirpath, name)
            ext = os.path.splitext(name.lower())[1]
            if ext in TEXT_EXT:
                try:
                    if os.path.getsize(path) <= MAX_BYTES:
                        yield path
                except OSError:
                    pass


def sanitize(text):
    text = text.strip()
    for rx in SECRET_PATTERNS:
        text = rx.sub(lambda m: (m.group(1) + m.group(2) + (m.group(3) + "[REDACTED]" + m.group(3) if m.lastindex and m.lastindex >= 4 and m.group(3) in ("\"", "'") else "[REDACTED]")) if m.lastindex and m.lastindex >= 3 else "[REDACTED]", text)
    # Redakce běžných hodnot v URL query stringu.
    text = re.sub(r"(?i)([?&](?:key|token|secret|password|signature)=)[^&\s]+", r"\1[REDACTED]", text)
    return text[:120] + ("..." if len(text) > 120 else "")


def scan(root):
    compiled = [(s, c, re.compile(p, re.IGNORECASE), risk) for s, c, p, risk in PATTERNS]
    hits = []
    for path in iter_files(root):
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                for lineno, line in enumerate(fh, 1):
                    for service, category, rx, risk in compiled:
                        if rx.search(line):
                            hits.append({"service": service, "category": category, "file": os.path.relpath(path, root), "line": lineno, "snippet": sanitize(line), "risk": risk, "evidence": "statický výskyt – vyžaduje ruční ověření"})
        except (OSError, UnicodeError):
            continue
    return hits


def to_markdown(hits, root):
    out = [f"# Inventura služeb – `{root}`", "", "> Statický výskyt není důkazem aktivního načítání ani porušení práva. Ukázky jsou sanitizovány.", ""]
    if not hits:
        return "\n".join(out + ["Nebyly nalezeny známé vzory. Prověř také administraci CMS, databázi, GTM a runtime požadavky."])
    grouped = {}
    for hit in hits:
        grouped.setdefault(hit["service"], []).append(hit)
    out += ["## Souhrn", "", "| Služba | Kategorie | Výskytů |", "|---|---|---:|"]
    for name, items in sorted(grouped.items()):
        out.append(f"| {name} | {items[0]['category']} | {len(items)} |")
    out += ["", "## Výskyty", "", "| Služba | Soubor:řádek | Ukázka | Co ověřit |", "|---|---|---|---|"]
    for h in hits:
        snippet = h["snippet"].replace("|", "\\|").replace("`", "'")
        out.append(f"| {h['service']} | `{h['file']}:{h['line']}` | `{snippet}` | {h['risk']} |")
    out += ["", "## Omezení", "", "- Skript neprohledává `.env`, soubory s klíči, certifikáty, databáze ani adresáře závislostí.", "- Nezjišťuje dynamické načítání, obsah GTM, nastavení CMS ani chování prohlížeče.", "- Každý nález ověř ručně a runtime kontrolou před souhlasem, po odmítnutí a po udělení souhlasu."]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="kořenová složka webu / repozitáře")
    parser.add_argument("--format", choices=["md", "json"], default="md")
    args = parser.parse_args()
    if not os.path.isdir(args.path):
        print(f"Chyba: složka '{args.path}' neexistuje.", file=sys.stderr)
        return 2
    hits = scan(os.path.abspath(args.path))
    if args.format == "json":
        json.dump(hits, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        print(to_markdown(hits, args.path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
