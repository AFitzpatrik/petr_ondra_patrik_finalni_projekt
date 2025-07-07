https://journey.study/v2/learn/courses/10302/modules/26102/units/16/materials/44239

- [ ] 1.0 Seznam událostí
  - 

- [ ] 2.0 Detail události

- [ ] 3.0 Vyhledávání událostí

- [ ] 4.0 Přidávání událostí
  - [ ] 4.1 Vytvoření události
  - [ ] 

- [ ] 5.0 Úprava událostí
  - [ ] 5.1 Úprava (pouze organizátor svojí událost)
  - [ ] 5.2 Mazání (pouze organizátor svojí událost)

- [ ] 6.0 Autentizace
  - [ ] 6.1 registrační formulář
  - [ ] 6.2 email
  - [ ] 6.3 user name
  - [ ] 6.4 jméno
  - [ ] 6.5 příjmení
  - [ ] 6.6 role organizátora (vytvořit v admin panelu)

- [ ] 7.0 Autorizace 

- [ ] 8.0 Přidávání komentářů
  - [ ] 8.1 pouze registrovaný uživatel

- [ ] 9.0 Přihlášení na akce
  - [ ] 9.1 Pouze přihlášený uživatel

- [ ] 10.0 API počasí/mapa












STRUKTURA DATABÁZE

- [ ] 1.0 Event
  - [ ] 1.1 name
  - [ ] 1.2 type (FK -> Type)
  - [ ] 1.3 description
  - [ ] 1.4 start_date_time
  - [ ] 1.5 end_date_time
  - [ ] 1.6 event_image
  - [ ] 1.7 owner_of_event (FK -> User)
  - [ ] 1.8 location (FK - > Location)


- [ ] 2.0 Location
  - [ ] 2.1 name
  - [ ] 2.2 description
  - [ ] 2.3 address
  - [ ] 2.4 city (FK -> City)


- [ ] 3.0 City
  - [ ] 3.1 name
  - [ ] 3.2 country (FK -> Country)
  - [ ] 3.3 zip code


- [ ] 4.0 Country
  - [ ] 4.1 name


- [ ] 5.0 Comment
 - [ ] 5.1 user (FK -> User)
 - [ ] 5.2 event (FK -> Event)
 - [ ] 5.3 content
 - [ ] 5.4 date_time posted


- [ ] 6.0 Type
  - [ ] name






