# Historie změn

## 2.2.0 – 19. 11. 2026

Obsah skillu (právní moduly, šablony, detekční skript) se nemění; verze přináší nové způsoby instalace a vydávání.

- Marketplace pro Claude Code (`.claude-plugin/marketplace.json`, `plugin.json`) – instalace a aktualizace přes `/plugin`.
- Marketplace pro Codex a další agenty (`.agents/plugins/marketplace.json`).
- Instalační skripty: volba `--ref` / `-Ref` pro instalaci konkrétní verze (tag, větev, commit).
- ZIP pro aplikaci Claude neobsahuje `tests/`, `README.md` ani `CHANGELOG.md`.
- GitHub Release s hotovým ZIPem při každém tagu `v*`.
- CI: testy, validace skillu a pluginu, kontrola instalátorů a shody verzí.

## 2.1.0 – 11. 11. 2026

- Bezpečnostní přepis detekčního skriptu: vynechání `.env*`, credentials, klíčů, certifikátů a databází; redakce podezřelých tajných hodnot ve výstupech.
- Odstraněna možnost `--include-vendor`, která by mohla vést k rozsáhlému a hlučnému skenování závislostí.
- Přidána metodika právních nálezů a seznam primárních zdrojů.
- Zpřesněny moduly GDPR, cookies, e-shop, B2B, přístupnost, AI Act, DSA a identifikace podnikatele.
- Odstraněny univerzální retenční lhůty z privacy šablony; neznámé údaje se označují k doplnění.
- Zpřesněny šablony cookie informací, odstoupení, obchodních podmínek a AI upozornění.
- Přidány README, LICENSE a automatické regresní testy.
