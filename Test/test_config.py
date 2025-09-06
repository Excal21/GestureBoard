import os
import json


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'App'))
os.chdir(project_root)


def test_configFile():
    config_path = os.path.join(project_root, 'Config', 'UserSettings.json')
    assert os.path.exists(config_path), f'Config fájl nem található: {config_path}'

  
    with open(config_path, 'r') as file:
        json_data = json.load(file)
    assert json_data is not None, 'Config fájl üres'

    for key in json_data.keys():
        assert any(char.isdigit() for char in key), f'A konfigurációs fájl egyik kulcsa helytelen: {key}'

    for key, value in json_data.items():
        assert isinstance(value, dict), f'A(z) {key} kulcs értéke nem dictionary: {value}'
        required_keys = {'gesture', 'action', 'description', 'highlight'}
        missing_keys = required_keys - value.keys()
        assert not missing_keys, f'A(z) {key} kulcs dictionary értékéből hiányoznak a következő kulcsok: {missing_keys}'
        assert value['highlight'] == -1, f'A(z) {key} kulcs dictionary értékében a highlight kulcs értéke nem -1: {value["highlight"]}'

