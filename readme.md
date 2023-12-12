# Filmová databáze

## Databáze
- [x] Země
  - [x] název
- [x] Žánr
  - [x] název 
- Filmy (Movie)
  - [x] Originální název filmu
  - [x] Český název filmu
  - [x] Slovenský název filmu
  - [x] země -> ManyToMany(Země)
  - [x] Žánr -> ManyToMany(Žánr)
  - [x] Režisér -> ManyToMany(Person)
  - [x] Herci -> ManyToMany(Person)
  - [x] Rok premiéry
  - [x] hodnocení -> FK(Hodnocení)
  - [x] komentáře -> FK(Hodnocení)
  - obrázky -> FK(Obrázky)
  - [x] video -> url odkaz na youtube na trailer
  - [x] popis
- [x] Hodnocení
  - [x] id filmu
  - [x] id uživatele
  - [x] hodnocení (hodnota 0-100 v %)
- [x] Komentáře
  - [x] id filmu
  - [x] id uživatele
  - [x] komentář
- Obrázky
  - id filmu
  - obrázek (název souboru/image ?)
  - popis
- [x] Person
  - [x] Jméno
  - [x] Příjmení
  - [x] Datum narození
  - [x] informace

## Funkce (views + templates)
- zobrazit novinky (homepage)
- [x] zobrazit seznam všech filmů
- filtrování filmů (seznam) 
  - podle žánru
  - podle hodnocení
  - [x] podle herce
  - [x] podle režiséra
- [x] zobrazit detail filmu
- přihlášený uživatel může:
  - [x] hodnotit filmy
  - [x] komentovat filmy
- admin může:
  - přidat/editovat/smazat film/herce/režiséra/žánr/země/komentáře