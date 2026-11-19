# Modul C – GDPR a ochrana osobních údajů

**Právní rámec:** GDPR (EU) 2016/679, zákon č. 110/2019 Sb. a související předpisy.

Šablony: `assets/zasady-ochrany-osobnich-udaju.md`, `assets/texty-formulare.md`.

## Zásady podle čl. 13 a 14 GDPR

- [ ] totožnost a kontaktní údaje správce; kontakt pověřence, je-li jmenován
- [ ] konkrétní účely a samostatný právní základ pro každý účel
- [ ] oprávněné zájmy, pokud je použit čl. 6 odst. 1 písm. f), a stručné vysvětlení
- [ ] příjemci nebo kategorie příjemců; role správce / společného správce / zpracovatele
- [ ] předání do třetích zemí, použitý mechanismus a informace o zárukách
- [ ] konkrétní doba uložení nebo srozumitelná kritéria jejího určení
- [ ] práva subjektu údajů, právo podat stížnost ÚOOÚ a právo odvolat souhlas
- [ ] zda je poskytnutí údajů zákonným/smluvním požadavkem a důsledky neposkytnutí
- [ ] informace o automatizovaném rozhodování podle čl. 22, je-li relevantní
- [ ] zdroj údajů, pokud nebyly získány od subjektu (čl. 14)

## Právní základy – důležitá pravidla

- Poptávka může spadat pod čl. 6 odst. 1 písm. b), pokud jde o kroky před uzavřením smlouvy na žádost subjektu. Obecný dotaz, který není krokem na žádost subjektu směřujícím ke smlouvě, může vyžadovat jiný základ, často posouzený oprávněný zájem.
- Neuváděj „b) nebo f)“ jako univerzální alternativu. Urči účel a zvolený základ.
- Newsletter: souhlas podle GDPR a pravidla obchodních sdělení podle § 7 zákona č. 480/2004 Sb. jsou dvě související, ale odlišné roviny. U stávajících zákazníků prověř podmínky zákonného soft opt-in.
- Cookies: vedle GDPR posuzuj samostatně § 89 odst. 3 ZEK.
- Účetní a daňové uchování: zjisti typ dokladu a příslušný předpis; deset let není univerzální doba pro všechny údaje na webu.
- Promlčecí lhůta sama o sobě automaticky neurčuje dobu uchování všech zákaznických údajů. Posuď nezbytnost, právní nároky a minimalizaci.

## Retenční lhůty

Nikdy nepřebírej obecné hodnoty typu 1 rok, 4 roky, 90 dní nebo 30 dní jako zákonný standard. Pokud dobu nelze doložit konkrétním právním předpisem nebo provozním důvodem, použij `[DOPLNIT – správce stanoví a odůvodní dobu]`. Odděl aktivní data, archivaci, právní blokaci a zálohy.

## Formuláře, účty a zabezpečení

- Kontaktní formulář obvykle nepotřebuje samostatný souhlas, pokud je zpracování založeno na jiném vhodném základu; informační povinnost však zůstává.
- Minimalizuj povinná pole a omez přístup k uloženým zprávám.
- Ověř, zda formulářová rozšíření ukládají zprávy do databáze a zda je to zohledněno v účelech, příjemcích a retenčních pravidlech.
- Právo na výmaz neznamená bezpodmínečné smazání všech údajů; zvaž zákonné povinnosti a právní nároky.
- GDPR obecně neukládá každé webové aplikaci univerzální funkci „smazat účet“; ověř konkrétní právní režim, smluvní závazky a práva subjektu.
- Bezpečnost hesel (silné hashování, např. Argon2id/bcrypt) je technické bezpečnostní opatření; závěr o porušení vyžaduje důkaz o konkrétní implementaci.
- Věk 15 let podle § 7 zákona č. 110/2019 Sb. se týká souhlasu dítěte v souvislosti se službami informační společnosti nabízenými přímo dítěti; neznamená obecnou hranici pro veškeré zpracování údajů dítěte.

## Mimo rozsah technického webového auditu

DPA, záznamy o činnostech, DPIA, balanční test oprávněného zájmu, interní retenční politika a řízení incidentů označ jako „nelze ověřit“, pokud nebyly dodány interní podklady.
