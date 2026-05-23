# Plan

## Opseg projekta

Tim E obraduje pitanja 9 i 10 iz datoteke `anketa_utorak.xlsx`.

Naslov rada:

`Analiza javnog mnijenja o sigurnosti SMR tehnologije i prihvatljivosti izgradnje u blizini mjesta stanovanja`

Dodijeljena pitanja:

- P9: "Sto smatrate najvecom prednoscu SMR tehnologije?"
- P10: "Smatrate li opravdanim drzavnu subvenciju razvoja SMR tehnologije umjesto ulaganja u jednu klasicnu, veliku nuklearnu elektranu?"

Iako je naslov siri od dodijeljenih pitanja, izvjestaj ce rezultate P9 i P10 tumaciti u kontekstu percepcije SMR tehnologije, njezinih prednosti i drustvene prihvatljivosti ulaganja u takvu tehnologiju.

## Dogovorene odluke

- Jezik izvjestaja i prezentacije: hrvatski.
- Analiticki projekt: `uv` projekt unutar direktorija `analysis/`.
- Clanovi tima na naslovnici: svi clanovi Tima E, samo imena i prezimena.
- Stil izvjestaja: jednostavan akademski LaTeX dokument.
- Stil prezentacije: Beamer prezentacija s naglasenom vizualnom hijerarhijom.
- Statistika: ukljuciti formalne statisticke testove.
- Demografske usporedbe: analizirati sve, a u tekstu istaknuti znacajne ili sadrzajno bitne nalaze.
- Oznake grafikona: skracene oznake na hrvatskom, uz legendu/objasnjenje.
- Dodatak: ukljuciti tocna anketna pitanja i ponudene odgovore.
- Slike u prezentaciji: prvo koristiti rezervirana mjesta, a naknadno po potrebi dodati slobodne slike s atribucijom.
- Kompilacija: pokusati lokalno izraditi PDF izvjestaja i prezentacije ako je LaTeX instaliran.

## Struktura direktorija

```text
analysis/
  pyproject.toml
  .python-version
  src/
    analyze.py
  outputs/
    figures/
    tables/

report/
  main.tex
  sections/
    uvod.tex
    metodologija.tex
    rezultati.tex
    rasprava.tex
    zakljucak.tex
  figures/
  tables/
  references.bib
  Makefile

presentation/
  main.tex
  figures/
  Makefile

notes/
  report_outline.md
  presentation_outline.md
```

## Plan analize

1. Ucitati `anketa_utorak.xlsx`.
2. Izdvojiti demografska obiljezja:
   - zupanija,
   - spol,
   - dob,
   - najvisi zavrsen stupanj obrazovanja,
   - status zaposlenosti.
3. Izdvojiti pitanja Tima E:
   - P9,
   - P10.
4. Ocistiti oznake odgovora i evidentirati nedostajuce vrijednosti.
5. Izracunati strukturu ispitanika:
   - ukupan broj valjanih odgovora,
   - raspodjele prema spolu, dobi, obrazovanju i statusu zaposlenosti.
6. Analizirati P9:
   - frekvencije i postotke po odgovoru,
   - dominantnu percipiranu prednost SMR tehnologije.
7. Analizirati P10:
   - frekvencije i postotke za odgovore `Da`, `Ne` i `Ne znam`,
   - razinu potpore drzavnom subvencioniranju razvoja SMR tehnologije.
8. Izraditi krizne tablice:
   - P9 prema dobi, spolu, obrazovanju i statusu zaposlenosti,
   - P10 prema dobi, spolu, obrazovanju i statusu zaposlenosti,
   - P10 prema P9.
9. Provesti formalne statisticke testove:
   - hi-kvadrat test neovisnosti za kategorijske varijable,
   - interpretirati rezultate uz razinu znacajnosti 0,05,
   - naglasiti ogranicenja ako su ocekivane frekvencije male.
10. Generirati grafikone i tablice:
    - stupcasti grafikon za P9,
    - stupcasti grafikon za P10,
    - odabrane slozene stupcaste grafikone za demografske usporedbe,
    - tablice rezultata testova.
11. Napisati izvjestaj u LaTeXu.
12. Izraditi Beamer prezentaciju za izlaganje od oko 6 minuta.

## Nacrt izvjestaja

1. Uvod
2. Opis ankete i podataka
3. Metodologija
4. Rezultati
   - struktura ispitanika,
   - P9: percipirane prednosti SMR tehnologije,
   - P10: stav prema drzavnim subvencijama,
   - usporedbe po demografskim obiljezjima,
   - povezanost P9 i P10.
5. Rasprava
6. Zakljucak
7. Dodatak s pitanjima i odgovorima

## Nacrt prezentacije

Cilj: 6 minuta, priblizno 7 do 8 slajdova.

1. Naslov i cilj analize
2. Podaci i uzorak
3. Struktura ispitanika
4. Rezultati za P9
5. Rezultati za P10
6. Najvaznije demografske razlike
7. Povezanost P9 i P10
8. Zakljucak

## Ideje za slike u prezentaciji

Prvo se koriste rezervirana mjesta. Ako se kasnije dodaju stvarne slike, treba koristiti samo slobodne slike s jasnom atribucijom.

Moguci motivi:

- nuklearna elektrana ili rashladni tornjevi,
- koncept malog modularnog reaktora,
- elektroenergetska mreza ili dalekovodi,
- vizual tranzicije prema niskougljicnoj energetici.
