---
name: web-legal-audit-cz
description: Právní audit českých webů podle české a EU legislativy – cookies a cookie lišta, GDPR, identifikace provozovatele, e-shop a spotřebitelské smlouvy, newslettery, přístupnost, AI Act. Projde zdrojový kód i živý web, najde služby třetích stran, navrhne opravy a doplní chybějící texty a souhlasy. Použij, když uživatel chce zkontrolovat web, cookie lištu, GDPR, obchodní podmínky e-shopu nebo soulad webu s legislativou.
license: MIT
compatibility: Určeno pro české weby (cs). Kontrola kódu funguje v každém agentovi s přístupem k souborům a Pythonu 3. Kontrola živého webu vyžaduje ovládání prohlížeče (síťové požadavky, cookies), ověření novinek vyžaduje vyhledávání na webu.
metadata:
  author: Petr (retailmedia.cz)
  version: "2.1.0"
  legislation-as-of: "2026-11-11"
  language: cs
---

# Právní audit webu – ČR a EU

Zkontroluj český web (zdrojový kód a/nebo živou URL) proti české a unijní legislativě, navrhni konkrétní opravy a doplň chybějící dokumenty a souhlasy. Výstupy piš česky.

Jde o odbornou technicko-právní kontrolu, ne o právní radu advokáta. U e-shopů s vysokým obratem, finančních, zdravotnických a dětských služeb doporuč finální revizi advokátem.

## Kdy použít

- „Zkontroluj web / cookie lištu / GDPR / obchodní podmínky“
- „Je web v souladu se zákonem?“, „co musí být v patičce“, „doplň zásady ochrany osobních údajů“
- příprava e-shopu na novou povinnost (např. tlačítko pro odstoupení od 1. 1. 2027)

Pokud uživatel chce jen část („jen cookies“), proveď jen příslušné moduly.

## Postup

### 0. Ověř aktuálnost legislativy
Přečti [references/legislativa-stav.md](references/legislativa-stav.md). Pokud máš vyhledávání na webu, spusť 2–3 dotazy na novinky (dotazy jsou v souboru). Změny oproti souboru uveď v reportu v sekci „Legislativní novinky“ a řiď se novějším stavem. Používej hierarchii zdrojů a pravidla z [references/pravni-metodika.md](references/pravni-metodika.md) a [references/zdroje-a-judikatura.md](references/zdroje-a-judikatura.md).

### 1. Zjisti kontext
Z kódu a webu zjisti, případně se zeptej jednou otázkou jen na to, co dohledat nejde:
- **zdroj**: složka/repozitář (WordPress, Divi, Next.js, PHP, statické HTML) a/nebo URL,
- **typ webu**: prezentační · s formulářem · rezervace/vstupenky/akce · e-shop B2C · B2B · SaaS s registrací · obsah uživatelů · veřejná instituce,
- **provozovatel**: OSVČ / s.r.o. / a.s. / spolek / veřejný subjekt; plátce DPH; mikropodnik (< 10 zaměstnanců a obrat nebo bilanční suma ≤ 2 mil. EUR).

### 2. Inventura služeb v kódu
Spusť detekční skript nad zdrojovým kódem:

```bash
python3 scripts/detect_services.py <cesta-k-webu> --format md > inventura.md
```

Skript vypíše nalezené služby třetích stran se souborem a řádkem, kategorií a typickým rizikem. Výsledek ověř čtením kódu (vyřaď falešné nálezy, např. v `node_modules` nebo komentářích) a doplň, jak se služba načítá (před/po souhlasu). Výklad ke každé službě a specifika WordPressu/Divi: [references/sluzby-tretich-stran.md](references/sluzby-tretich-stran.md).

### 3. Kontrola živého webu (je-li URL a prohlížeč)
Postup v [references/kontrola-zivy-web.md](references/kontrola-zivy-web.md): síťové požadavky a cookies před souhlasem, po „Odmítnout vše“, odvolání souhlasu, HTTPS, patička, formuláře, checkout. **Nikdy neodesílej formuláře ani objednávky na produkčním webu bez výslovného pokynu.**

### 4. Vyhodnoť podle modulů
Načti jen moduly relevantní pro typ webu:

| Modul | Soubor | Kdy |
|---|---|---|
| A – Identifikace provozovatele | [references/a-identifikace.md](references/a-identifikace.md) | vždy u podnikatele |
| B – Cookies a sledování | [references/b-cookies.md](references/b-cookies.md) | vždy |
| C – GDPR | [references/c-gdpr.md](references/c-gdpr.md) | vždy |
| D – Obchodní sdělení, newsletter | [references/d-newsletter.md](references/d-newsletter.md) | newsletter, e-mailing |
| E – E-shop, spotřebitelské smlouvy | [references/e-eshop.md](references/e-eshop.md) | prodej / rezervace / vstupenky online |
| F – Přístupnost | [references/f-pristupnost.md](references/f-pristupnost.md) | e-shopy, služby, veřejný sektor (u ostatních jako doporučení) |
| G – AI Act | [references/g-ai-act.md](references/g-ai-act.md) | AI chatbot, AI obsah |
| H – DSA, bezpečnost, ostatní | [references/h-ostatni.md](references/h-ostatni.md) | obsah uživatelů; bezpečnost vždy |
| Metodika | [references/pravni-metodika.md](references/pravni-metodika.md) | vždy |
| Primární zdroje | [references/zdroje-a-judikatura.md](references/zdroje-a-judikatura.md) | vždy |

Každé zjištění nejprve označ typem: **PROKÁZANÝ NESOULAD**, **PRAVDĚPODOBNÝ NESOULAD**, **NELZE OVĚŘIT**, **DOPORUČENÍ** nebo **BUDOUCÍ POVINNOST**. Teprve poté přiřaď závažnost podle [references/pravni-metodika.md](references/pravni-metodika.md). Samotný statický výskyt skriptu není důkazem porušení.

### 5. Napiš report
Použij šablonu [assets/report-sablona.md](assets/report-sablona.md). Každé zjištění musí mít ID (písmeno modulu + číslo), místo (soubor:řádek nebo URL/požadavek), předpis a konkrétní opravu. Žádné obecné rady bez vazby na nalezený stav. Report doruč jako dokument (formát dle možností prostředí a přání uživatele).

### 6. Oprav a doplň
Nabídni, nebo rovnou proveď, pokud o to uživatel požádal:
1. **Opravy kódu** v repozitáři/kopii, nikdy přímo na produkčním serveru; ke každé změně krátký popis.
2. **Chybějící texty a prvky** ze šablon v `assets/`:

| Potřeba | Šablona |
|---|---|
| Identifikace provozovatele v patičce | [assets/paticka-provozovatel.html](assets/paticka-provozovatel.html) |
| Cookie lišta + Google Consent Mode v2 | [assets/cookie-lista.html](assets/cookie-lista.html) |
| Stránka „Cookies“ | [assets/cookies-stranka.md](assets/cookies-stranka.md) |
| Zásady ochrany osobních údajů | [assets/zasady-ochrany-osobnich-udaju.md](assets/zasady-ochrany-osobnich-udaju.md) |
| Texty u formulářů, newsletteru, checkoutu | [assets/texty-formulare.md](assets/texty-formulare.md) |
| Upozornění u AI chatbotu | [assets/ai-chatbot-oznameni.html](assets/ai-chatbot-oznameni.html) |
| Prohlášení o přístupnosti | [assets/prohlaseni-o-pristupnosti.md](assets/prohlaseni-o-pristupnosti.md) |
| Tlačítko a formulář pro odstoupení | [assets/odstoupeni-tlacitko.md](assets/odstoupeni-tlacitko.md) |
| Doložky do obchodních podmínek | [assets/vop-dolozky.md](assets/vop-dolozky.md) |

3. Šablony vyplň vším, co je zjistitelné (název, IČO, adresa, služby z inventury); zbytek označ `[DOPLNIT: …]`.
4. Na konci vypiš checklist pro člověka (podepsat smlouvy se zpracovateli, nastavit Consent Mode v GTM, doplnit údaje, revize advokátem).

## Zásady

- Hodnoť skutečný stav (kód + chování webu), ne jen existenci stránky „GDPR“.
- Nevymýšlej údaje provozovatele; neznámé označ `[DOPLNIT]`.
- Rozlišuj povinnost a doporučení.
- Čísla předpisů a termíny uváděj přesně; při nejistotě ověř a uveď zdroj.
- Nevymýšlej retenční lhůty, právní základy, role dodavatelů ani skutkové okolnosti. Neznámé označ `[DOPLNIT]` nebo `NELZE OVĚŘIT`.
- Rozlišuj zákonnou povinnost, oficiální metodický výklad a doporučenou praxi.
- Každý právní nález podlož konkrétním ustanovením a primárním zdrojem s datem ověření.
- U statické inventury výslovně uváděj, že přítomnost kódu sama neprokazuje aktivní načítání ani právní nesoulad.
- Nepoužívej výstup detekčního skriptu jako důkaz, že web je bezpečný nebo v souladu.
- Před sdílením reportu zkontroluj, že neobsahuje přístupové údaje, tokeny, osobní údaje nebo obchodní tajemství.
