# Web Legal Audit CZ – verze 2.1.0

Český Agent Skill pro technicko-právní orientační audit webů podle českého a evropského práva.

## Obsah

- `SKILL.md` – hlavní instrukce a pracovní postup.
- `references/` – právní moduly, metodika, zdroje a pokyny pro kontrolu živého webu.
- `assets/` – pracovní šablony a textové vzory.
- `scripts/detect_services.py` – bezpečná statická inventura známých služeb.
- `tests/` – automatické regresní testy.

## Požadavky

- Python 3.8 nebo novější (pouze standardní knihovna pro detekční skript a testy).
- Pro audit živého webu prohlížeč s možností kontroly síťových požadavků, cookies a úložišť.
- Pro aktuální právní stav přístup k primárním zdrojům (e-Sbírka, EUR-Lex a weby příslušných orgánů).

## Použití

Z kořenového adresáře skillu:

```bash
python3 scripts/detect_services.py /cesta/k/webu --format md > inventura.md
python3 scripts/detect_services.py /cesta/k/webu --format json > inventura.json
python3 -m unittest discover -s tests -v
```

Skript prohledává pouze vybrané textové zdrojové soubory. Záměrně vynechává `.env*`, soubory s credentials, klíče, certifikáty, databáze, závislosti a minifikované JS. Ukázky ve výstupu jsou sanitizovány. Statický nález není důkazem aktivního provozu služby ani právního nesouladu.

## Bezpečnost a ochrana dat

- Spouštěj pouze nad kopií zdrojového kódu, pokud není jiný postup výslovně schválen.
- Nepřikládej výstupy obsahující osobní údaje nebo obchodní tajemství bez kontroly a redakce.
- Skript nemá síťovou komunikaci a nemění skenované soubory.
- Nikdy nevkládej tajné klíče, hesla ani produkční `.env` do reportu.

## Právní omezení

Skill poskytuje orientační technicko-právní analýzu, nikoli právní službu ani záruku souladu. Právní stav ověřuj při každém auditu. U regulovaných, vysoce rizikových nebo sporných případů doporuč právníka. Datum poslední redakční kontroly zdrojů v této verzi: 11. 11. 2026.

## Změny ve verzi 2.1.0

- bezpečnostní přepis detekčního skriptu: vyloučení tajných souborů a sanitizace výstupu;
- rozlišení prokázaného nesouladu, pravděpodobného nesouladu, neověřeného stavu a doporučení;
- odstranění univerzálních retenčních lhůt a paušálních právních závěrů;
- zpřesnění B2B/spotřebitel, § 1837 OZ, cookies/Consent Mode, AI Act, přístupnosti a DSA;
- aktualizace šablon a přidání metodiky, seznamu primárních zdrojů a automatických testů.
