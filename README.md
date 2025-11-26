# GestureBoard [![English](https://img.shields.io/badge/lang-EN-blue)](README_EN.md)
A GestureBoard egy innovatív alkalmazás, amely lehetővé teszi, hogy kézmozdulataidhoz számítógépes műveleteket rendelj, mindezt egy intuitív grafikus felhasználói felületen keresztül.

A gesztusfelismerés és a kézpozíciók megtanulása neurális háló segítségével történik, amit a [<i>Google MediaPipe</i>](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer) valósít meg.


## Futtatás
A kliens futtatható a release verziókban található futtathatók segítségével, vagy közvetlen a <i>App</i> mappában található main.py elindításával.


## Alapgesztusok
<div align="center">


| **Nyílt tenyér** | **Zárt ököl** | **Felfelé mutatás** | **Két ujjal balra** |
|:-------------------:|:------------------:|:-------------------:|:------------------:|
| <img src="img/Nyilt_tenyer.png" alt="Nyílt tenyér" width="225"/> | <img src="img/Zart_okol.png" alt="Zárt ököl" width="225"/> | <img src="img/Mutatas_fel.png" alt="Felfelé mutatás" width="225"/> | <img src="img/Ket_ujjal_oldalra.png" alt="Két ujjal balra" width="225"/> |





</div>

## Saját gesztusok tanítása
Ha szeretnéd lecserélni vagy bővíteni a 4 alapgesztust, a tanítás idejére szükség van egy tanítószerverre. Készíthetsz saját szervert, megadhatsz egy létező kiszolgálót, vagy használhatod a GestureBoard által biztosított felhőalapú tanítószervert.

A felhőalapú tanítás használatakor a tanítási folyamat akár 1-2 percet is igénybe vehet.

> **Adatvédelem**  
> A GestureBoard tanítási szakaszában a szoftver fényképeket készít a felhasználó kezéről. Ezekre a képekre kizárólag a tanítás ideje alatt van szükség, és azok semmilyen formában nem kerülnek továbbításra vagy megosztásra harmadik fél számára.
>
>A szoftver használata saját felelősségre történik. Kérlek, ügyelj arra, hogy a képeken ne szerepeljen semmilyen érzékeny adat, személyes információ, vagy olyan tartalom, amely adatvédelmi vagy biztonsági kockázatot jelenthet.


### Tanítószerver létrehozása
A tanítószerver könnyedén elkészíthető és elindítható [<i>Docker</i>](https://www.docker.com/) segítségével. A Docker telepítése után a projekt <i>docker</i> mappájába navigálva add ki a következő parancsokat:

```bash
docker compose build
docker compose up -d
```



## Követelmények
A szoftver megköveteli a legfrissebb Microsoft C++ Redistributable meglétét.

Amennyiben a programot nem az elkészített futtatható állományból szeretnéd indítani, a Python függőségek a következő parancsokkal telepíthetők:
```bash
pip install -r requirements.txt
```

## Tippek
<details>
  <summary>Kattints a kibontáshoz/összecsukáshoz</summary>

- Akkor fog a <i>GestureBoard</i> a legjobban működni, hogyha a kezed lazán tartod.

- Használat előtt a kamera-beállításokban próbáld ki a gesztusokat! A kameraképen látni fogod, hogy a program hogyan érzékeli a kezedet, és milyen gesztusokat ismer fel. 

- A program azokat a gesztusokat fogja a legjobban, legpontosabban felismerni, amiket Te tanítasz meg neki.

-  Próbálj olyan kéztartásokat választani, ahol az ujjaid nem fedik egymást, vagy csak kis mértékben! Ha a program nem elég pontos a tanítás után, javasolt a tanítási folyamat újbóli futtatása, szükség esetén a minták újbóli felvétele.

</details>


## Köszönet az ikonok készítőinek
<details>
  <summary>Kattints a kibontáshoz/összecsukáshoz</summary>
<br>

A GestureBoard a [flaticon](flaticon.com) ingyenes ikonjait használja. Köszönet illeti a következő alkotókat:
- joalfa - [Konzol ikon](https://www.flaticon.com/free-icons/command)
- juicy_fish - [Billentyűzet ikon](https://www.flaticon.com/free-icons/hardware)
- Creative Avenue - [Választható műveletek ikonja](https://www.flaticon.com/free-icons/widget)
- berkahicon - [Kéz ikon](https://www.flaticon.com/free-icons/cursor)
- Dixit Lakhani_02 - [Pipa](https://www.flaticon.com/free-icons/tick)

- Good Ware - [Kamera ikon](https://www.flaticon.com/free-icons/camera)

</details>