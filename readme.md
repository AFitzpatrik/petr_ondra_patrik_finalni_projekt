https://journey.study/v2/learn/courses/10302/modules/26102/units/16/materials/44239

- [x] 1.0 Seznam událostí - ONDRA/PATRIK
  - [x] 1.1 Řazení podle nejblížšího data
  - [x] 1.2 Titulek události, datum, obrázek, prvních 50 znaků z description


- [x] 2.0 Detail události - PATRIK
-   [x] 2.1 Název
-   [x] 2.2 Datum od/do
-   [x] 2.3 Čas od/do
-   [x] 2.4 Celý popis události
-   [x] 2.5 Adresa,lokace
-   [x] 2.6 Obrázek
-   [x] 2.7 Proklik ze seznamu událostí


- [x] 3.0 Vyhledávání událostí - PETR
  - [x] 3.1 Textové pole pro vyhledávání


- [x] 4.0 Přidávání událostí - ONDRA
  - [x] 4.1 Omezení 'pouze organizátor může přidat událost'
  - [x] 4.2 Název
  - [x] 4.3 Datum od/do
  - [x] 4.4 Čas od/do
  - [x] 4.5 Vlastník (uživatel, který událost vytvořil)
  - [x] 4.6 Obrázek události


- [ ] 5.0 Úprava událostí - PATRIK
  - [x] 5.1 Úprava 
    - [X] 5.1.1 Pouze PŘIHLÁŠENÝ UŽIVATEL
    - [x] 5.1.2 Pouze ORGANIZÁTOR
  - [x] 5.2 Mazání 
    - [x] 5.2.1 Pouze ORGANIZÁTORA
    - [ ] 5.2.2 Pouze ORGANIZÁTOR který je VLASTNÍK  !!! PRIORITA 1


- [x] 6.0 Autentizace - PATRIK
  - [x] 6.1 registrační formulář - REGISTRACE
    - [x] 6.1.1  email
    - [x] 6.1.2  user name
    - [x] 6.1.3  jméno
    - [x] 6.1.4  příjmení
  - [x] 6.2 přihlašovací formulář - PŘIHLÁŠENÍ
  - [x] 6.3 Zobrazení přihlášeného uživatele
    - [x] 6.3.1 Dropdown menu
    - [x] 6.3.2 Změna hesla
    - [x] 6.3.3 Reset hesla
    - [x] 6.3.4 Můj profil page
  - [x] 6.4 Registration success page
    - [x] 6.5 Proklik na login
  - [x] 6.5 Logout success page
  - [x] 6.6 Login success page


- [x] 7.0 Autorizace - PATRIK
  -[x] 7.1 role organizátora (vytvořit v admin panelu)


- [x] 8.0 Přidávání komentářů - ONDRA
  - [x] 8.1 Pouze registrovaný uživatel
  - [x] 8.2 Max 500 znaků?
  - [x] 8.3 Řazení od nejnovějších


- [ ] 9.0 Seznam míst  - ONDRA
  - [ ] 9.1 Proklik na události v dánem místě

- [ ] 10.0 Seznam měst  - ONDRA
  - [ ] 10.1 Proklik na události v dánem městě


- [x] 11.0 Přihlášení na akci
  - [x] 11.1 Pouze přihlášený uživatel
  - [x] 11.1 Událost se přidá uživateli do MOJE UDÁLOSTI
      - KDYŽ BUDE ČAS UDĚLAT SÓLO STRÁNKY S FILTREM


- [ ] 12.0 API cizí - PETR
-   [x] 12.1.Počasí
-   [ ] 12.2 Mapa


- [ ] 13.0 Filtr eventů - PETR
  - [ ] od/do
  - [ ] typ
  - [ ] město

- [ ] 14.0 Stránkování eventů - PATRIK


- [ ] 15.0 Přehled organizátora o události - ONDRA
  - [ ] účastníci





- [ ] 17.0 Admin panel - KDYŽ BUDE ČAS
    [ ] 12.1 Počasí
    [ ] 12.2 Mapa
    [ ] 12.3 Rest API









STRUKTURA DATABÁZE

- [x] 1.0 Event
  - [x] 1.1 name
  - [x] 1.2 type (FK -> Type)
  - [x] 1.3 description
  - [x] 1.4 start_date_time
  - [x] 1.5 end_date_time
  - [x] 1.6 event_image
  - [x] 1.7 owner_of_event (FK -> User)
  - [x] 1.8 location (FK - > Location)


- [x] 2.0 Location
  - [x] 2.1 name
  - [x] 2.2 description
  - [x] 2.3 address
  - [x] 2.4 city (FK -> City)


- [x] 3.0 City
  - [x] 3.1 name
  - [x] 3.2 country (FK -> Country)
  - [x] 3.3 zip code


- [x] 4.0 Country
  - [x] 4.1 name


- [x] 5.0 Comment
  - [x] 5.1 user (FK -> User)
  - [x] 5.2 event (FK -> Event)
  - [x] 5.3 content
  - [x] 5.4 date/time posted
  - [x] 5.5 date/time updated
  - 


- [x] 6.0 Type
  - [x] name






