import hashlib
import os
import re
import tempfile

from trinitytech_deploy.os import set_env, run


def safe_kebab(string: str) -> str:
    return re.compile(r'[^a-zA-Z0-9-]').sub('-', string)


def safe_snake(string: str) -> str:
    return safe_kebab(string).replace('-', '_')


def workspace() -> tempfile.TemporaryDirectory:
    temporary_directory = tempfile.TemporaryDirectory(prefix='/tmp/workspace-')
    set_env('WORKSPACE', temporary_directory.name)
    os.chdir(temporary_directory.name)
    return temporary_directory


def checkout(repo: str, branch='main'):
    run(['git', 'init'])
    run(['git', 'remote', 'add', 'origin', repo])
    run(['git', 'fetch', 'origin', branch])
    run(['git', 'checkout', branch])


def md5(filepath: str) -> str:
    return hashlib.md5(open(filepath, 'rb').read()).hexdigest()
