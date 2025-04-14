import json
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'UI'))
os.chdir(project_root)


def test_PredefinedActions():
    assert os.path.exists('Config/PredefinedActionMap.json'), 'Az elődefiniált beállítások konfigurációs fájl nem található'
    with open('Config/PredefinedActionMap.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for key, value in data.items():
        assert value is not None and value != '', f'A {key} kulcsnak nincs értéke'
