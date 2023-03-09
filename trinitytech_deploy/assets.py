import json
import pathlib
import tempfile

from trinitytech_deploy import run

ASSETS_PATH = pathlib.Path(__file__).parent / 'assets'


def get_assets_file(relative_path: str) -> pathlib.Path:
    return ASSETS_PATH / relative_path


def get_assets_file_content(relative_path: str) -> str:
    return get_assets_file(relative_path).read_text()


def copy_assets_file(relative_path: str, dest_path: str):
    with get_assets_file(relative_path).open() as src:
        with open(dest_path, 'w') as dest:
            dest.write(src.read())


def exec_assets_template(relative_path: str, output_path: str, values=None):
    # TODO: check `goet` is installed
    if values is None:
        values = dict()
    with tempfile.NamedTemporaryFile(prefix='/tmp/goet-value', suffix='.json', mode='w') as values_file:
        json.dump(values, values_file)
        values_file.flush()
        values_file.seek(0)
        run(['goet', '-t', get_assets_file(relative_path), '-o', output_path, '-f', values_file.name])
