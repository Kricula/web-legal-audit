# Modul B – Cookies a obdobné technologie

**Právní rámec:** § 89 odst. 3 zákona č. 127/2005 Sb.; GDPR, zejména čl. 4, 5, 6, 7, 12–14 a 21; relevantní výklad ÚOOÚ a judikatura SDEU.

Šablony: `assets/cookie-lista.html`, `assets/cookies-stranka.md`.

## Kontrolní postup

1. Otevři web v čistém profilu / anonymním okně a zaznamenej síťové požadavky, cookies, localStorage a sessionStorage před volbou.
2. Zvol „Odmítnout vše“ a ověř, že se nespustí technologie vyžadující předchozí souhlas.
3. Uděl souhlas jen pro jednu kategorii a ověř, že se aktivuje pouze odpovídající technologie.
4. Odvolej souhlas a ověř zastavení dalšího ukládání/čtení nepovinných identifikátorů v rozsahu technicky možném.
5. Opakuj test na mobilu a pro relevantní jazykové/regionální varianty.

## Hodnoticí pravidla

- U technologií, na které dopadá § 89 odst. 3 ZEK, je předchozí souhlas pravidlem; výjimku posuzuj podle konkrétní nezbytnosti pro přenos nebo službu výslovně požadovanou uživatelem. Neoznačuj analytiku automaticky za nezbytnou.
- Uživatel musí mít reálnou a informovanou volbu. Odmítnutí nesmí být skryté nebo podstatně obtížnější než přijetí. První vrstvu navrhuj s jasnou volbou přijmout, odmítnout a nastavit; přesné právní hodnocení založ na aktuální metodice a okolnostech.
- Samotné zavření lišty nelze bez dalšího považovat za souhlas. Význam zavření / pokračování musí být jasně vysvětlen a nesmí být předvolený.
- Granulární volby a evidence souhlasu jsou vhodné pro prokazatelnost; konkrétní rozsah evidence přizpůsob skutečnému řešení.
- Cookie wall neposuzuj paušálně. Zkoumej svobodnost souhlasu, alternativu, povahu služby, proporcionalitu a aktuální výklad dozorových orgánů a soudů.
- Neexistuje univerzální zákonná lhůta 6 nebo 12 měsíců, po níž musí být souhlas znovu vyžádán. Nastav přiměřenou platnost podle účelu, změn a použitelného doporučení; nevydávej interní nastavení za zákonnou lhůtu.
- Google Consent Mode není souhlas ani náhrada blokování. Ověř skutečné načítání tagů, default consent před tagy, update po volbě a chování každého dodavatele. Režim advanced může před souhlasem odesílat omezené pingy; vyhodnoť je samostatně.
- YouTube nocookie, DNT nebo „anonymizace“ samy o sobě neprokazují, že není třeba souhlas.

## Klasifikace

Klasifikuj konkrétní účel a technologii, ne pouze značku. Stejná služba může mít nezbytné i nepovinné funkce. U externích fontů, map, videí, chatů a CAPTCHA posuzuj také přenos IP adresy a dalších údajů; neoznačuj automaticky každý požadavek za cookie.

## Právní a metodické zdroje

- § 89 odst. 3 zákona č. 127/2005 Sb. – aktuální znění v e-Sbírce.
- ÚOOÚ: https://uoou.gov.cz/ – aktuální metodiky ke cookies.
- GDPR: https://eur-lex.europa.eu/eli/reg/2016/679/oj
