import os
import pathlib
import subprocess

HOME_PATH = pathlib.Path.home()


def set_env(key: str, value: str):
    os.environ[key] = value


def get_env(key: str, default=''):
    return os.environ.get(key, default)


def run(cmd: list[str], cwd=None, env=None):
    cmd = [str(c) for c in cmd]
    print('\n\033[1;32m$ ' + ' '.join(cmd) + '\033[0m\n')
    subprocess.run(cmd, cwd=cwd, env=env, check=True)
