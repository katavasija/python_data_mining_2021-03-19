from pathlib import Path
import json


def get_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    if not save_path.exists():
        save_path.mkdir()
    return save_path


def save_json(data: dict, file_path: Path):
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')


def is_file(file_path: Path):
    return file_path.exists() and file_path.is_file()


def load_json(file_path: Path):
    if file_path.is_file():
        return json.load(file_path.open('r', encoding='utf-8'))
    else:
        raise Exception(f'Wrong file {file_path.__str__()}')