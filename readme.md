# 🗓️ SuperEvents

Projekt SuperEvents je webová aplikace sloužící k přehledné správě, organizaci
a prezentaci událostí. Uživatelé si mohou události zobrazovat, přihlašovat se na
ně, komentovat je a v případě organizátorů, je také vytvářet a spravovat.

SuperEvents je webová aplikace vytvořená v Django frameworku pro správu a vytváření událostí.  
Umožňuje uživatelům vyhledávat události, registrovat se na ně a zobrazovat jejich podrobnosti.

### 👥 Tým
- [AFitzpatrik](https://github.com/AFitzpatrik)
- [Nunu8888](https://github.com/Nunu8888)  
- [OndZii](https://github.com/OndZii)  


---

## ✨ Funkce aplikace

### 👤 Uživatelské účty
- Registrace a ověření nových uživatelů
- Možnost přidání speciálních rolí (např. organizátor, admin, staff...)
- Obnova zapomenutého hesla a změna stávajícího hesla
- Uživatelský panel:
  - Zobrazení svých osobních údajů
  - Seznam organizovaných a rezervovaných událostí

### 📅 Události
- Přidávání, mazání a úprava událostí
- Přehledný seznam událostí a zobrazení podrobností v detailu události
- Oprávnění podle role (kdo může co spravovat)
- Možnost registrace na konkrétní událost
- Zobrazení obsazenosti události
- Komentáře:
  - Možnost přidávání komentářů pro přihlášené uživatele
  - Zobrazení komentářů pro nepřihlášené uživatele

### 🔍 Ostatní funkce
- Vyhledávání událostí podle konkrétního slova
- Filtrování událostí podle místa a času

### 🌐 API
- REST API pro zpracování dat
- Zobrazení aktuálního **počasí** v místě události pomocí API
- Zobrazení základních informací o **státech** pomocí API

---

## 🧾 Struktura projektu
**(DOPLNIT!!!!!)**  

---

## 🗺️ ER Diagram
**(DOPLNIT!!!!!)**  

---

## 📸 Screenshoty
**(DOPLNIT!!!!!)** 

---

## 🛠️ Instalace

1. **Naklonuj repozitář**
```bash
git clone https://github.com/AFitzpatrik/petr_ondra_patrik_finalni_projekt
cd project_name
```

2. **Vytvoř a aktivuj virtuální prostředí**
```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

3. **Nainstaluj potřebné knihovny**
```bash
pip install -r requirements.txt
```

4. **Spusť a proveď migrace**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Spusť vývojový server**
```bash
python manage.py runserver
```



---
---
---
---
---
---
---
---
---
---
---
---































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


- [x] 5.0 Úprava událostí - PATRIK
  - [x] 5.1 Úprava 
    - [X] 5.1.1 Pouze PŘIHLÁŠENÝ UŽIVATEL
    - [x] 5.1.2 Pouze ORGANIZÁTOR
  - [x] 5.2 Mazání 
    - [x] 5.2.1 Pouze ORGANIZÁTORA
    - [x] 5.2.2 Pouze ORGANIZÁTOR který je VLASTNÍK  !!! PRIORITA 1


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


- [x] 12.0 API cizí - PETR
-   [x] 12.1.Počasí
-   [ ] 12.2 Mapa


- [x] 13.0 Filtr eventů - PETR
  - [x] od/do
  - [x] typ
  - [x] město

- [x] 14.0 Stránkování eventů - PATRIK


- [ ] 15.0 Přehled organizátora o události - ONDRA
  - [ ] účastníci





- [x] 17.0 Admin panel - PETR
-   [x] 12.1 Počasí
-   [ ] 12.2 Mapa
-   [x] 12.3 Rest API


- [x] 18.0 Země - PETR
  - [x] Události v zemi
  - [x] Údaje o zemi z API





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






