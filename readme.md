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

- [ ] 3.0 Vyhledávání událostí - PETR
  - [ ] 3.1 Textové pole pro vyhledávání

- [ ] 4.0 Přidávání událostí - ONDRA
  - [ ] 4.1 Omezení 'pouze organizátor může přidat událost'
  - [ ] 4.2 Název
  - [ ] 4.3 Datum od/do
  - [ ] 4.4 Čas od/do
  - [ ] 4.5 Vlastník (uživatel, který událost vytvořil)
  - [ ] 4.6 Obrázek události

- [ ] 5.0 Úprava událostí - PATRIK
  - [ ] 5.1 Úprava (pouze organizátor svojí událost)
  - [ ] 5.2 Mazání (pouze organizátor svojí událost)

- [ ] 6.0 Autentizace - PATRIK
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
    - [ ] 6.3.4 Můj profil page
  - [x] 6.4 Registration success page
    - [x] 6.5 Proklik na login
  - [x] 6.5 Logout success page
  - [x] 6.6 Login success page


- [ ] 7.0 Autorizace - PATRIK
  -[ ] 7.1 role organizátora (vytvořit v admin panelu)


- [ ] 8.0 Přidávání komentářů - ONDRA
  - [ ] 8.1 Pouze registrovaný uživatel
  - [ ] 8.2 Max 500 znaků?
  - [ ] 8.3 Řazení od nejnovějších
        





- [ ] 9.0 Přihlášení na akce
  - [ ] 9.1 Pouze přihlášený uživatel

- [ ] 10.0 API počasí/mapa


- [ ] 11.0 Admin panel











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






