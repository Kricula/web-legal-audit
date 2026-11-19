# Texty k formulářům

## Kontaktní / poptávkový formulář
Bez povinného checkboxu se souhlasem (právní základ je jednání o smlouvě / oprávněný zájem). Pod tlačítko odeslání:

```html
<p class="form-info">
  Odesláním formuláře nám předáváte osobní údaje, které zpracujeme za účelem vyřízení vaší poptávky.
  Více v <a href="/zasady-ochrany-osobnich-udaju">Zásadách ochrany osobních údajů</a>.
</p>
```

## Přihlášení k newsletteru
Samostatný, nepovinný, nepředzaškrtnutý; double opt-in.

```html
<label>
  <input type="checkbox" name="newsletter" value="1">
  Chci dostávat novinky a nabídky e-mailem. Souhlas mohu kdykoli odvolat odkazem v každém e-mailu.
  <a href="/zasady-ochrany-osobnich-udaju">Více informací</a>
</label>
```

Samostatný formulář pro newsletter: odeslání může představovat souhlas pouze tehdy, pokud je účel a souhlas předem jasně a jednoznačně vysvětlen a uživatel provede aktivní úkon výhradně za tímto účelem. Bezpečnější variantou je nepředzaškrtnuté potvrzení:

```html
<p class="form-info">
  Kliknutím na tlačítko „Přihlásit k newsletteru“ souhlasíte se zasíláním newsletteru na zadaný e-mail. Souhlas můžete kdykoli odvolat odkazem v každém e-mailu.
  <a href="/zasady-ochrany-osobnich-udaju">Ochrana osobních údajů</a>
</p>
```

## Checkout – soft opt-in pro stávající zákazníky (§ 7 odst. 3 zák. 480/2004 Sb.)

```html
<p>Váš e-mail můžeme použít k zasílání nabídek obdobného zboží a služeb. Odhlásit se můžete kdykoli.</p>
<label><input type="checkbox" name="no_marketing" value="1"> Nepřeji si dostávat obchodní sdělení.</label>
```

## Checkout – souhlas s VOP
Souhlas s obchodními podmínkami je seznámení se smluvními podmínkami, ne souhlas se zpracováním osobních údajů. Tyto dvě věci nespojuj.

```html
<label>
  <input type="checkbox" name="terms" required>
  Souhlasím s <a href="/obchodni-podminky" target="_blank">obchodními podmínkami</a> a beru na vědomí
  <a href="/obchodni-podminky#odstoupeni" target="_blank">poučení o odstoupení od smlouvy</a>.
</label>
<p class="form-info">Osobní údaje zpracujeme podle <a href="/zasady-ochrany-osobnich-udaju">Zásad ochrany osobních údajů</a>.</p>

<button type="submit">Objednávka zavazující k platbě</button>
```

## Patička e-mailu (obchodní sdělení)

```
Toto je obchodní sdělení společnosti [Firma], IČO [IČO], [adresa].
Tento e-mail dostáváte, protože [jste se přihlásil(a) k odběru / jste náš zákazník].
Odhlásit se můžete jedním kliknutím: [odkaz na odhlášení]
```
