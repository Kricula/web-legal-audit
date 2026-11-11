# Tlačítko pro odstoupení od smlouvy – příprava na § 1830a OZ

**Právní stav:** zákon č. 159/2026 Sb. zavádí § 1830a občanského zákoníku s účinností od 1. 1. 2027. Před nasazením ověř aktuální znění zákona, působnost a případné výjimky v e-Sbírce.

Tato pomůcka není univerzálním hotovým řešením. Povinnost se týká distančních smluv uzavřených prostřednictvím online rozhraní, u nichž má spotřebitel právo odstoupit. Nezaměňuj odstoupení ve lhůtě s běžným ukončením předplatného.

## Doporučený proces

1. Zobraz výrazný a snadno přístupný prvek s textem „Odstoupit od smlouvy“ nebo jednoznačnou formulací.
2. Umožni spotřebiteli snadno vyplnit nebo potvrdit jméno, údaje o smlouvě a elektronický kontakt pro potvrzení.
3. Před odesláním zobraz srozumitelné shrnutí.
4. Odeslání proveď samostatným tlačítkem „Potvrdit odstoupení od smlouvy“ nebo jednoznačným ekvivalentem.
5. Bez zbytečného odkladu odešli potvrzení v textové podobě, včetně obsahu prohlášení a data a času odeslání spotřebitelem.
6. Bezpečně zaznamenej přijetí, čas, identifikátor smlouvy a obsah prohlášení; stanov přístup a retenční pravidla.

## Návrh formuláře – pouze výchozí UX

```html
<form method="post" action="[DOPLNIT bezpečný endpoint]">
  <label for="customer-name">Jméno a příjmení</label>
  <input id="customer-name" name="customer_name" autocomplete="name" required>

  <label for="contract-reference">Číslo objednávky / identifikace smlouvy</label>
  <input id="contract-reference" name="contract_reference" required>

  <label for="confirmation-email">E-mail pro potvrzení přijetí</label>
  <input id="confirmation-email" name="confirmation_email" type="email" autocomplete="email" required>

  <button type="submit">Potvrdit odstoupení od smlouvy</button>
</form>
```

Ukázka sama nezajišťuje právní soulad. Doplň ochranu proti CSRF, autentizaci/ověření oprávnění přiměřené riziku, potvrzovací krok, bezpečné doručení, záznam času a automatické potvrzení. Nevyžaduj přihlášení, pokud by fakticky ztížilo zákonné právo; posuzuj konkrétní proces.

## Testovací checklist

- [ ] prvek je dostupný po celou zákonnou lhůtu
- [ ] formulář lze ovládat klávesnicí a čtečkou
- [ ] údaje o smlouvě lze snadno identifikovat
- [ ] potvrzovací krok je samostatný a jednoznačný
- [ ] systém zaznamená přesný obsah a čas odeslání
- [ ] potvrzení obsahuje obsah prohlášení a datum/čas odeslání
- [ ] potvrzení je doručeno na zadaný elektronický kontakt
- [ ] výjimky z práva odstoupit jsou posouzeny podle konkrétní smlouvy
