from utils import save_json, load_json

def test_save_load_json(tmp_path):
    file = tmp_path / "test.json"

    data = {"hello": "world"}

    save_json(data, file)

    loaded = load_json(file)

    assert loaded == data