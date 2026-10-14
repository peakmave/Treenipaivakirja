# Treenipäiväkirja

Treenipäiväkirja on web-sovellus, jonka avulla käyttäjä voi kirjata omat treeninsä ylös ja seurata niitä ajan mittaan.

Käyttäjä voi luoda tunnuksen ja kirjautua sovellukseen omilla tunnuksillaan.
Kirjautunut käyttäjä voi lisätä uusia treenejä, joihin merkitään päivämäärä, laji (esim. voimaharjoittelu, juoksu, jooga), kesto minuutteina, vapaamuotoiset muistiinpanot sekä yksi tai useampi luokka (voimaharjoittelu, kestävyys, liikkuvuus tai muu).
Käyttäjä näkee omat treeninsä listana, ja voi muokata tai poistaa niitä. Treenejä voi hakea hakusanalla, joka etsii osumia sekä lajin että muistiinpanojen tekstistä.
Jokaisella käyttäjällä on oma profiilisivunsa, jossa näkyvät hänen uniikki @-käyttäjänimensä, profiilikuvana nimen ensimmäinen kirjain, tilastot (treenien määrä ja yhteenlaskettu kesto) sekä kaikki hänen lisäämänsä treenit. Muiden käyttäjien sivuille ja treeneihin pääsee navigaation Käyttäjät-linkistä, ja kuka tahansa kirjautunut käyttäjä voi kirjoittaa kommentteja toisen käyttäjän treeniin.

## Keskeiset toiminnot
- Käyttäjän rekisteröityminen ja kirjautuminen
- Treenien lisääminen, muokkaaminen ja poistaminen
- Kaikkien omien treenien näkeminen listana
- Treenien hakeminen hakusanalla (laji tai muistiinpanot)
- Käyttäjäprofiilit: uniikki @-käyttäjänimi, profiilikuvana nimen ensimmäinen kirjain sekä käyttäjän tilastot ja treenit
- Treenille voi valita yhden tai useamman luokan (esim. voimaharjoittelu, kestävyys)
- Käyttäjä voi kommentoida toisen käyttäjän treeniä
- Etusivu, jolla näkyvät kaikkien käyttäjien viimeisimmät treenit

## Sovelluksen testaaminen omalla koneella

Vaatimukset: Python 3, `pip` ja `sqlite3`-komentorivityökalu. Debian- ja Ubuntu-järjestelmissä tarvitaan lisäksi paketti `python3-venv`.

1. Kloonaa repositorio ja siirry sen juurikansioon:
   ```
   git clone https://github.com/peakmave/Treenipaivakirja.git
   cd Treenipaivakirja
   ```

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

7. Kokeile sovellusta selaimessa:
   - Luo tunnus "Luo tunnus" -linkistä ja kirjaudu sisään. Käyttäjänimi on 3-30 merkkiä (a-z, 0-9 ja alaviiva), sen pitää olla uniikki kirjainkoosta riippumatta, ja se näkyy muille muodossa @nimi.
   - Lisää treeni ("Lisää uusi treeni") ja valitse sille yksi tai useampi luokka. Luokat (Voimaharjoittelu, Kestävyys, Liikkuvuus ja Muu) luodaan tietokantaan `schema.sql`-tiedostosta.
   - Kokeile treenin muokkausta, poistoa (poisto kysyy vahvistuksen erillisellä sivulla) ja hakua.
   - Etusivulla näkyvät kaikkien käyttäjien viimeisimmät treenit.
   - Kokeile virheellisiä syötteitä (esim. liian pitkä kesto): lomake näyttää virheilmoituksen ja säilyttää kirjoitetut tiedot.
   - Kommentointia varten tarvitaan toinen käyttäjä: luo toinen tunnus esimerkiksi incognito-ikkunassa. Lisää ensimmäisellä tunnuksella treeni, kirjaudu toisella tunnuksella, avaa navigaation Käyttäjät-linkistä ensimmäisen käyttäjän sivu (siellä näkyvät tilastot ja treenit), avaa treeni ja kirjoita kommentti.

**Huom:** `database.db` ei kuulu repositorioon (ks. `.gitignore`), koska se syntyy paikallisesti. Tiedosto `config.py` on mukana repositoriossa, jotta sovellus käynnistyy suoraan kloonauksen jälkeen.
