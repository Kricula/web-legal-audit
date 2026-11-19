# Kontrola živého webu

Potřebuješ ovládání prohlížeče se čtením síťových požadavků a spouštěním JavaScriptu. Bez prohlížeče tento krok vynech a v reportu uveď, že runtime kontrola neproběhla.

## Postup

1. Otevři web v čistém profilu (bez dřívějšího souhlasu – případně smaž cookies domény).
2. Načti hlavní stránku a 2–3 podstránky (kontakt, produkt/služba, košík).
3. **Před jakoukoli interakcí s lištou** zaznamenej:
   - síťové požadavky na třetí strany: `google-analytics.com`, `googletagmanager.com`, `doubleclick.net`, `facebook.com/tr`, `connect.facebook.net`, `hotjar`, `clarity.ms`, `c.seznam.cz`, `fonts.googleapis.com`, `youtube.com`, `maps.googleapis.com`, chat widgety,
   - cookies a úložiště:
     ```js
     ({ cookies: document.cookie, local: Object.keys(localStorage), session: Object.keys(sessionStorage) })
     ```
4. Klikni **„Odmítnout vše“** a kontrolu opakuj. Po odmítnutí ověř, zda se neukládají/nečtou technologie vyžadující souhlas. U síťových požadavků rozliš běžné načtení stránky, omezené Consent Mode pingy a skutečné předání identifikátorů či dat. Samotný požadavek na doménu dodavatele není bez dalšího důkazem porušení. Posouzení umístění a výraznosti tlačítka založ na aktuální metodice a celkovém UX; neoznačuj automaticky druhou vrstvu za porušení bez dalšího posouzení.
5. Ověř, že lze souhlas **změnit/odvolat** (odkaz v patičce otevře nastavení).
6. Klikni „Přijmout vše“ a ověř, že se služby načtou (lišta funguje, nejen zobrazuje).
7. Zkontroluj HTTPS, přesměrování z HTTP, mixed content.
8. Projdi patičku (identifikace, odkazy na zásady a cookies), kontakt, formuláře (texty, checkboxy – **neodesílat**), košík a checkout **bez dokončení objednávky** (text tlačítka objednávky, ceny dopravy, souhlasy).
9. Pokud je k dispozici Node: `npx @axe-core/cli <URL>` nebo `npx pa11y <URL>` pro přístupnost.
10. Bezpečnostní hlavičky (lze i bez prohlížeče):
    ```bash
    curl -sI https://example.cz | grep -iE 'strict-transport|content-security|x-content-type|referrer-policy|permissions-policy'
    ```

## Zakázané akce
- Neodesílej formuláře, objednávky, registrace ani žádosti o odstoupení.
- Nezkoušej přihlášení cizími údaji ani bezpečnostní útoky; kontroluj jen veřejně dostupné chování.
