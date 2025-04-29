# GestureBoard
A GestureBoard egy innovatív alkalmazás, amely lehetővé teszi, hogy kézmozdulataidhoz számítógépes műveleteket rendelj, mindezt egy intuitív grafikus felhasználói felületen keresztül.

A gesztusfelismerés és a kézpozíciók megtanulása neurális háló segítségével történik, amit a [<i>Google MediaPipe</i>](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer) valósít meg.


## Futtatás
A kliens futtatható a release verziókban található futtathatók segítségével, vagy közvetlen a <i>UI</i> mappában található main.pyw elindításával.


<div align="center">

## Alapgesztusok

| **Nyílt tenyér** | **Zárt ököl** |
|:----------------:|:-------------:|
| <img src="img/Nyilt_tenyer.png" alt="Nyílt tenyér" width="200"/> | <img src="img/Zart_okol.png" alt="Zárt ököl" width="200"/> |

| **Felfelé mutatás** | **Két ujjal balra** |
|:-------------------:|:------------------:|
| <img src="img/Mutatas_fel.png" alt="Felfelé mutatás" width="200"/> | <img src="img/Ket_ujjal_oldalra.png" alt="Két ujjal balra" width="200"/> |

</div>

## Saját gesztusok tanítása
Ha szeretnéd lecserélni vagy bővíteni a 4 alapgesztust, akkor létre kell hoznod vagy meg kell adnod egy létező tanítószervert. Ez egy olyan kiszolgáló, ami fogadja a kezedről készült mintákat és a GestureBoard programnak megtanítja az új kéztartásaid. Erre a kiszolgálóra csak a tanítás idejére van szükség.

### Tanítószerver létrehozása
A tanítószerver könnyedén elkészíthető és elindítható [Docker](https://www.docker.com/) segítségével. A Docker telepítése után a projekt <i>docker</i> mappájába navigálva add ki a következő parancsokat:

```bash
docker compose build
docker compose up -d
```

## Tippek
- Akkor fog a <i>GestureBoard</i> a legjobban működni, hogyha a kezed lazán tartod.

- A program azokat a gesztusokat fogja a legjobban, legpontosabban felismerni, amiket Te tanítasz meg neki.

-  Próbálj olyan kéztartásokat választani, ahol az ujjaid nem fedik egymást, vagy csak kis mértékben! Ha a program nem elég pontos a tanítás után, javasolt a tanítási folyamat újbóli futtatása, szükség esetén a minták újbóli felvétele.



## Követelmények
A szoftver megköveteli a legfrissebb Microsoft C++ Redistributable meglétét.

Amennyiben a programot nem az elkészített futtatható állományból szeretnéd indítani, a Python függőségek a következő parancsokkal telepíthetők:
```bash
pip install -r requirements.txt
```

## Köszönet az ikonok készítőinek
A GestureBoard a [flaticon](flaticon.com) ingyenes ikonjait használja. Köszönet illeti a következő alkotókat:
- joalfa - [Konzol ikon](https://www.flaticon.com/free-icons/command)
- juicy_fish - [Billentyűzet ikon](https://www.flaticon.com/free-icons/hardware)
- Creative Avenue - [Választható műveletek ikonja](https://www.flaticon.com/free-icons/widget)
- berkahicon - [Kéz ikon](https://www.flaticon.com/free-icons/cursor)
- Dixit Lakhani_02 - [Pipa](https://www.flaticon.com/free-icons/tick)

- Good Ware - [Kamera ikon](https://www.flaticon.com/free-icons/camera)