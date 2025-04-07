# GestureBoard
A GestureBoard egy innovatív alkalmazás, amely lehetővé teszi, hogy kézmozdulataidhoz számítógépes műveleteket rendelj, mindezt egy intuitív grafikus felhasználói felületen keresztül.

Az alkalmazás 4 gesztust ismer alapból. Amennyiben szeretnéd kihasználni a GestureBoard teljes funkciótárát, hozz létre egy tanítószervert!

## Futtatás
A kliens futtatható a release verziókban található futtathatók segítségével, vagy közvetlen a <i>UI</i> mappában található main.pyw elindításával.


## Tanítószerver létrehozása
A tanítószerver könnyedén elkészíthető és elindítható [Docker](https://www.docker.com/) segítségével. A Docker telepítése után a projekt <i>docker</i> mappájába navigálva add ki a következő parancsokat:

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

## Köszönet az ikonok készítőinek
A GestureBoard a [flaticon](flaticon.com) ingyenes ikonjait használja. Köszönet illeti a következő alkotókat:
- joalfa - [Konzol ikon](https://www.flaticon.com/free-icons/command)
- juicy_fish - [Billentyűzet ikon](https://www.flaticon.com/free-icons/hardware)
- Creative Avenue - [Választható műveletek ikonja](https://www.flaticon.com/free-icons/widget)
- berkahicon - [Tanítás varázslójának képe](https://www.flaticon.com/free-icons/cursor)
- Dixit Lakhani_02 - [Pipa](https://www.flaticon.com/free-icons/tick)

- Good Ware - [Kamera ikon](https://www.flaticon.com/free-icons/camera)