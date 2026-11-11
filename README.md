# Web Legal Audit CZ

**Český Agent Skill pro technicko-právní audit webových stránek podle českého a evropského práva.**

Web Legal Audit CZ pomáhá systematicky prověřit webové stránky, identifikovat používané služby třetích stran, zkontrolovat vybrané právní a technické oblasti a připravit konkrétní návrhy nápravy. Výstupy jsou vytvářeny v češtině a zohledňují české právní prostředí i relevantní právo Evropské unie.

> **Upozornění:** Skill poskytuje orientační technicko-právní analýzu. Nenahrazuje právní služby advokáta, individuální právní posouzení ani odborný bezpečnostní audit. Výsledek závisí na dostupných podkladech, přístupu k webu a aktuálnosti ověřených zdrojů.

## Co skill kontroluje

| Oblast | Zaměření |
|---|---|
| Identifikace provozovatele | Povinné údaje o podnikateli a provozovateli webu |
| Cookies a sledování | Cookie lišta, souhlasy, analytické a marketingové technologie, Google Consent Mode |
| GDPR | Osobní údaje, účely a právní základy zpracování, informační povinnost, příjemci a doby uchování |
| Newslettery | Obchodní sdělení, souhlasy, zákaznická výjimka a odhlášení |
| E-shopy a spotřebitelské smlouvy | Informace před uzavřením smlouvy, objednávkový proces, obchodní podmínky a odstoupení |
| Přístupnost | Relevantní požadavky na přístupnost webů a digitálních služeb |
| AI Act | Povinnosti podle role subjektu a konkrétního použití AI |
| DSA a další oblasti | Povinnosti podle typu služby, uživatelského obsahu a související bezpečnostní otázky |

Audit se přizpůsobuje typu webu. Prezentační web, e-shop, rezervační systém, SaaS aplikace a web s uživatelským obsahem nemají automaticky stejné povinnosti.

## Hlavní funkce

- **Analýza zdrojového kódu** – statická inventura známých služeb třetích stran a technologií.
- **Kontrola živého webu** – při dostupném prohlížeči kontrola cookies, síťových požadavků, chování cookie lišty a vybraných částí webu.
- **Modulární právní kontrola** – načítání pouze oblastí relevantních pro konkrétní web.
- **Práce s primárními zdroji** – přednost mají právní předpisy a oficiální metodiky příslušných institucí.
- **Klasifikace nálezů** – rozlišení prokázaného nesouladu, pravděpodobného nesouladu, neověřeného stavu, doporučení a budoucí povinnosti.
- **Konkrétní návrhy oprav** – doporučení navázaná na konkrétní soubor, místo na webu nebo zjištěné chování.
- **Pracovní šablony** – vzory a podklady pro cookie informace, zásady ochrany osobních údajů, formuláře a další dokumenty.

## Struktura projektu

Úplná struktura skillu, právní reference, šablony, skripty a testy jsou součástí přiloženého archivu `web-legal-audit-cz-v2.1.0.zip`.

## Použití

Skill je určen pro AI agenty a prostředí, která podporují formát **Agent Skills**. Způsob instalace se může lišit podle konkrétního agenta nebo klienta. Po instalaci musí být dostupný celý adresář skillu včetně `SKILL.md`, referencí, skriptů a šablon.

Skill aktivuj například požadavkem:

- „Proveď právní audit tohoto webu.“
- „Zkontroluj cookie lištu a načítání analytických skriptů.“
- „Prověř GDPR a formuláře na tomto webu.“
- „Zkontroluj obchodní podmínky a objednávkový proces e-shopu.“
- „Prověř, jaké služby třetích stran používá tento repozitář.“

Pro dílčí kontrolu výslovně uveď požadovanou oblast, například „zkontroluj pouze cookies“.

### Požadavky

- Python **3.8 nebo novější** pro detekční skript a automatické testy.
- Pro statickou inventuru přístup ke zdrojovému kódu webu.
- Pro kontrolu živého webu prohlížeč umožňující kontrolu síťových požadavků, cookies a úložišť.
- Pro ověření aktuální legislativy přístup k primárním právním zdrojům.

### Statická inventura služeb

Z kořenového adresáře rozbaleného skillu spusť:

```bash
python3 scripts/detect_services.py /cesta/k/webu --format md > inventura.md
```

Výstup ve formátu JSON:

```bash
python3 scripts/detect_services.py /cesta/k/webu --format json > inventura.json
```

Skript prohledává vybrané textové zdrojové soubory a hledá známé vzory služeb. Záměrně vynechává soubory s citlivou konfigurací, například `.env*`, klíče, certifikáty, databáze a adresáře závislostí.

**Důležité omezení:** Statický výskyt kódu neprokazuje, že se služba skutečně načítá v prohlížeči, že ukládá cookies nebo že web porušuje právní předpis. Nálezy je nutné ověřit v kontextu kódu a podle možností také runtime kontrolou.

### Spuštění testů

Z kořenového adresáře skillu:

```bash
python3 -m unittest discover -s tests -v
```

Testy používají standardní knihovnu Pythonu a nevyžadují instalaci dalších balíčků.

## Jak skill vyhodnocuje nálezy

Každé zjištění má být nejprve zařazeno do jedné z kategorií:

- **PROKÁZANÝ NESOULAD** – dostupné důkazy potvrzují rozpor s konkrétní povinností.
- **PRAVDĚPODOBNÝ NESOULAD** – zjištěné skutečnosti nasvědčují problému, ale chybí část důkazů.
- **NELZE OVĚŘIT** – dostupné podklady nestačí k závěru.
- **DOPORUČENÍ** – zlepšení nad rámec prokázané zákonné povinnosti.
- **BUDOUCÍ POVINNOST** – požadavek, který se má uplatnit k budoucímu datu nebo za stanovených podmínek.

Následně se přiřazuje závažnost podle metodiky v `references/pravni-metodika.md`.

Právní závěr má být podložen konkrétním ustanovením a pokud možno primárním zdrojem. Skill musí rozlišovat zákonnou povinnost, oficiální metodický výklad a doporučenou praxi. Pokud chybí skutkové informace, nesmí je domýšlet.

## Bezpečnost a ochrana dat

- Přednostně prováděj analýzu nad kopií repozitáře nebo zdrojových souborů.
- Do vstupních podkladů ani reportů nevkládej hesla, API klíče, přístupové tokeny, privátní klíče nebo produkční konfigurační soubory.
- Před sdílením výstupu zkontroluj, zda neobsahuje osobní údaje, obchodní tajemství nebo jiné citlivé informace.
- Detekční skript je určen pro lokální statickou analýzu; sám nemá měnit skenované soubory ani provádět síťové požadavky.
- Nikdy neodesílej formuláře, objednávky ani jiné produkční transakce bez výslovného pokynu.
- Výstup skriptu nepovažuj za důkaz bezpečnosti nebo právního souladu webu.

## Právní upozornění a disclaimer

**Tento skill nebyl vytvořen, odborně posouzen ani schválen advokátem nebo jiným právníkem. Jeho obsah není právním stanoviskem ani právní službou.**

Skill vychází pouze z dostupných zdrojů legislativy, veřejně dostupných metodik, výkladových materiálů a dalších uvedených podkladů. Přesnost a úplnost výstupu proto závisí na dostupnosti, aktuálnosti a správné interpretaci těchto zdrojů. Ani uvedení odkazu na právní předpis nebo oficiální metodiku samo o sobě nezaručuje, že je právní závěr úplný nebo správný pro konkrétní situaci.

Výstupy slouží pouze jako orientační technicko-právní pomůcka. Nepředstavují právní radu, nezakládají vztah advokát–klient a nezaručují soulad webu s právními předpisy. Autor ani projekt neposkytují záruku za správnost, úplnost nebo aktuálnost výstupů a nenesou odpovědnost za rozhodnutí učiněná výhradně na jejich základě.

Právní předpisy, jejich výklad i metodiky se mění. Při každém auditu je proto nutné ověřit aktuální znění relevantních předpisů, jejich účinnost a použitelnost na konkrétní případ. Zvláštní pozornost vyžadují hraniční případy, výjimky, regulované služby a zpracování citlivých údajů. Před přijetím právně významných rozhodnutí nebo zveřejněním právních dokumentů doporučujeme nezávislou kontrolu kvalifikovaným právníkem.

## Verze a změny

Aktuální verze: **2.1.0**

Podrobnosti o změnách najdeš v souboru `CHANGELOG.md` uvnitř archivu.

## Licence

Projekt je distribuován pod licencí MIT. Podrobnosti jsou uvedeny v souboru `LICENSE` uvnitř archivu.

---

**Jazyk projektu:** čeština  
**Právní prostředí:** Česká republika a Evropská unie
