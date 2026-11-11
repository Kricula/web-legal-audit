# Služby třetích stran – výklad k inventuře

Detekční vzory jsou v `scripts/detect_services.py`. Tady je, co s nálezem dělat.

## Výstup inventury

Tabulka: služba → kde v kódu (soubor:řádek) → kategorie → právní základ → načítá se před souhlasem (ano/ne/neznámo) → přenos mimo EHP → uvedeno v zásadách (ano/ne).

## Služby a typická opatření

| Služba | Kategorie | Opatření |
|---|---|---|
| Google Analytics 4, GTM | dle konkrétních tagů | ověřit účel a právní režim; Consent Mode není souhlas ani blokátor; ověřit skutečné tagy, požadavky a předávání |
| Meta Pixel, Facebook SDK/embed | marketingové | blokovat do souhlasu; embedy přes „click-to-load“ |
| Seznam Sklik, retargeting | marketingové | předávat parametr `consent` (0/1) do retargetingu i konverzí; skript až po souhlasu |
| Heureka (Ověřeno zákazníky, konverze), Zboží.cz | marketingové | konverzní kódy po souhlasu; Ověřeno zákazníky uvést v zásadách (předání e-mailu) |
| Hotjar, Microsoft Clarity, Smartlook | analytické | nahrávání relací jen po souhlasu; maskovat formulářová pole |
| YouTube | externí obsah | náhled s načtením po kliknutí; `youtube-nocookie.com` samo o sobě nezaručuje výjimku ze souhlasu |
| Vimeo | analytické | parametr `dnt=1`, případně click-to-load |
| Google Maps (iframe, API, Divi modul mapy) | třetí strana | statický náhled (obrázek + odkaz) a načtení po kliknutí, nebo Mapy.cz odkaz |
| Google Fonts z CDN | přenos IP | doporuč self-hosting (🟡); rozsudek LG München 2022 je německý, ale ukazuje riziko |
| reCAPTCHA | sporné | uvést v zásadách; zvážit Cloudflare Turnstile / hCaptcha / honeypot |
| Chat widgety (Smartsupp, Tawk, Intercom, Crisp, LiveChat) | funkční/marketingové | načíst po souhlasu nebo po kliknutí na ikonu; zpracovatel v zásadách |
| AI chatbot | AI Act + GDPR | upozornění „mluvíte s AI“ (modul G); zpracovatel, uchování konverzací |
| Newsletter (Ecomail, Mailchimp, SmartEmailing, MailerLite, Brevo) | GDPR + obch. sdělení | nepředzaškrtnutý souhlas, double opt-in (modul D) |
| Platební brány (Stripe, GoPay, Comgate, ThePay, PayPal) | platby / předávání údajů | rozliš platební zpracování a cookies/trackery; ověř roli dodavatele, údaje a právní základ |
| Rezervace (Calendly, Reservio, SimplyBook, Bookio) | zpracovatel | uvést v zásadách |
| CDN (cdnjs, jsDelivr, unpkg, Cloudflare) | přenos IP | uvést, případně hostovat lokálně |
| Sdílení (AddThis, ShareThis, X/Instagram embed) | marketingové | po souhlasu nebo prosté odkazy bez skriptu |
| Vlastní `document.cookie`, `localStorage`, `setcookie()` | dle účelu | klasifikovat; nezbytné jen pro provoz (košík, přihlášení, volba cookies) |

## WordPress / Divi

- **Divi**: volba *Improve Google Fonts Loading* fonty stále stahuje z Googlu – použij lokální fonty. Modul mapy (`et_pb_map`) = Google Maps API. Divi kontaktní formulář (`et_pb_contact_form`) neukládá do DB, ale posílá e-mail.
- **Skripty**: projdi `wp_enqueue_script` v child theme a pluginech, *Theme Options → Integration* (Divi vkládá kód do `<head>`), vlastní HTML moduly.
- **Ukládání formulářů**: Flamingo (CF7), WPForms entries, Gravity Forms – uvést v zásadách a nastavit dobu uchování / automatické mazání.
- **Komentáře**: WP ukládá IP a e-mail, Gravatar přenáší hash e-mailu – vypnout nebo uvést.
- **Cookie pluginy** (Complianz, CookieYes, Cookiebot, Cookie Notice): ověř, že skripty skutečně **blokují**, ne jen zobrazují lištu.
- **WooCommerce**: modul E (tlačítko objednávky, VOP, odstoupení, Omnibus slevy).

## Next.js / React

- Skripty v `app/layout.tsx`, `pages/_document.tsx`, `next/script` se `strategy` – ověř, že analytika se renderuje podmíněně podle souhlasu.
- `@next/third-parties` (GoogleAnalytics, GoogleTagManager) se načítá hned – nutný Consent Mode default `denied` nebo podmíněné vložení.
- `next/font/google` fonty self-hostuje při buildu – v pořádku.
