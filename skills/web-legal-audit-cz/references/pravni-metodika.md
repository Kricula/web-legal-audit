# Metodika právního vyhodnocení

**Verze metodiky:** 2.1.0 · **Ověření zdrojů:** 11. 11. 2026

## 1. Hierarchie zdrojů

1. Platné znění právního předpisu v e-Sbírce nebo EUR-Lexu.
2. Rozhodnutí soudů a závazné akty příslušných orgánů.
3. Oficiální metodiky a stanoviska ÚOOÚ, ČOI, MPO, Evropské komise a dalších dozorových orgánů.
4. Odborné komentáře a sekundární zdroje pouze podpůrně.

Neodvozuj právní povinnost pouze z blogu, marketingové stránky dodavatele ani z výsledku vyhledávání. Ověř účinnost, přechodná ustanovení, působnost a případné novely.

## 2. Povinné štítky nálezů

Každý nález označ jedním z těchto typů:
- **PROKÁZANÝ NESOULAD** – existuje konkrétní důkaz o chování nebo obsahu a přesná právní povinnost.
- **PRAVDĚPODOBNÝ NESOULAD** – důkazy silně nasvědčují problému, ale chybí runtime nebo provozní ověření.
- **NELZE OVĚŘIT** – potřebná informace není ve zdrojích dostupná; nepředkládej ji jako porušení.
- **DOPORUČENÍ** – dobrá praxe, bezpečnostní opatření nebo snížení rizika bez tvrzení, že jde o samostatnou zákonnou povinnost.
- **BUDOUCÍ POVINNOST** – pravidlo dosud není účinné; uveď datum účinnosti a přechodná pravidla.

## 3. Závažnost

- **Kritická:** doložený závažný nesoulad s bezprostředním dopadem na práva osob nebo vysokým právním rizikem.
- **Vysoká:** doložené nesplnění významné povinnosti.
- **Střední:** neúplnost, nejistota nebo významné doporučení.
- **Nízká / informativní:** drobná technická poznámka nebo budoucí povinnost.

Samotná přítomnost knihovny, domény nebo identifikátoru ve zdrojovém kódu není důkazem, že služba skutečně běží, ukládá cookies nebo odesílá osobní údaje. Samotná absence detekce není důkazem, že služba není používána.

## 4. Práce s právními základy a lhůtami

- Pro každý účel zpracování určuj samostatně právní základ a vysvětli jeho použitelnost.
- Nekombinuj čl. 6 odst. 1 písm. b) a f) GDPR jako univerzální alternativu bez rozlišení konkrétních účelů.
- Nevymýšlej retenční lhůty. Použij konkrétní zákonnou lhůtu, pokud existuje; jinak označ `[DOPLNIT – správce musí určit a odůvodnit]`.
- Rozliš dobu aktivního zpracování, archivaci, blokaci a dobu uchování záloh.
- U oprávněného zájmu vyžaduj identifikaci zájmu a posouzení nezbytnosti a vyvážení práv.

## 5. Práce s důkazy

U každého nálezu uveď:
- ID a typ nálezu;
- přesné místo důkazu (soubor a řádek, URL, síťový požadavek, screenshot nebo výstup nástroje);
- co bylo skutečně ověřeno a co je pouze předpoklad;
- konkrétní ustanovení včetně odstavce/písmene;
- odkaz na primární zdroj a datum ověření;
- opravu a test, kterým se ověří její účinnost.

## 6. Hranice auditu

Audit není právní stanovisko advokáta, penetrační test, DPIA ani úplný audit interních procesů správce. Bez přístupu k administraci, smlouvám, nastavení dodavatelů a reálnému provozu výslovně popiš omezení. Neodesílej formuláře, objednávky ani osobní údaje do produkčních systémů bez výslovného souhlasu.
