# Treenipäiväkirja

Treenipäiväkirja on web-sovellus, jonka avulla käyttäjä voi kirjata omat treeninsä ylös ja seurata niitä ajan mittaan.

Käyttäjä voi luoda tunnuksen ja kirjautua sovellukseen omilla tunnuksillaan.
Kirjautunut käyttäjä voi lisätä uusia treenejä, joihin merkitään päivämäärä, laji (esim. voimaharjoittelu, juoksu, jooga), kesto minuutteina, vapaamuotoiset muistiinpanot sekä yksi tai useampi luokka (voimaharjoittelu, kestävyys, liikkuvuus tai muu).
Käyttäjä näkee omat treeninsä listana, ja voi muokata tai poistaa niitä. Treenejä voi hakea hakusanalla, joka etsii osumia sekä lajin että muistiinpanojen tekstistä.
Jokaisella käyttäjällä on oma käyttäjäsivunsa, jossa näkyvät hänen tilastonsa (treenien määrä ja yhteenlaskettu kesto) sekä kaikki hänen lisäämänsä treenit. Muiden käyttäjien sivuille ja treeneihin pääsee navigaation Käyttäjät-linkistä, ja kuka tahansa kirjautunut käyttäjä voi kirjoittaa kommentteja toisen käyttäjän treeniin.

## Keskeiset toiminnot
- Käyttäjän rekisteröityminen ja kirjautuminen
- Treenien lisääminen, muokkaaminen ja poistaminen
- Kaikkien omien treenien näkeminen listana
- Treenien hakeminen hakusanalla (laji tai muistiinpanot)
- Käyttäjäsivut, jotka näyttävät käyttäjän tilastot ja hänen lisäämänsä treenit
- Treenille voi valita yhden tai useamman luokan (esim. voimaharjoittelu, kestävyys)
- Käyttäjä voi kommentoida toisen käyttäjän treeniä

## Sovelluksen testaaminen omalla koneella

Vaatimukset: Python 3 ja `pip`.

1. Kloonaa repositorio ja siirry sen juurikansioon.

2. Luo ja aktivoi virtuaaliympäristö:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
   (Windowsilla ilman WSL:ää aktivointi: `venv\Scripts\activate`)

3. Asenna riippuvuudet:
   ```
   pip install flask
   ```

4. Luo tietokanta `schema.sql`-tiedoston perusteella:
   ```
   sqlite3 database.db < schema.sql
   ```

5. Käynnistä sovellus:
   ```
   flask run
   ```

6. Avaa selaimessa osoite [http://127.0.0.1:5000](http://127.0.0.1:5000)

7. Luo sovellukseen tunnus "Luo tunnus" -linkistä, kirjaudu sisään ja kokeile treenien lisäystä, muokkausta, poistoa ja hakua.

**Huom:** Tiedosto `database.db` ei kuulu repositorioon (ks. `.gitignore`). Testaajan tulee luoda se itse yllä olevan ohjeen mukaisesti `schema.sql`-tiedoston pohjalta.

## Muiden käyttäjien treenit

Navigaation Käyttäjät-linkistä pääsee käyttäjälistaan ja sieltä jokaisen käyttäjän omalle sivulle, jossa näkyvät tilastot ja treenit. Treenin sivulla voi lukea ja kirjoittaa kommentteja.
