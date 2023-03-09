import os
import tempfile

from trinitytech_deploy.os import HOME_PATH, run
from trinitytech_deploy.utils import md5

NODE_MODULES_CACHES_DIR_PATH = HOME_PATH / '.cache' / 'trinitytech-deploy' / 'node_modules-caches'
NODE_MODULES_CACHES_KEEP_DAYS = 30
DEFAULT_NODE_IMAGE_TAG = 'node:14.17.6'


def npm_install_in_docker(cmd: str = 'npm install', node_image_tag=DEFAULT_NODE_IMAGE_TAG):
    package_json_md5 = md5('package.json')
    if get_node_modules_cache(package_json_md5):
        return
    with tempfile.TemporaryDirectory(prefix='/tmp/npm-') as npm_tmp_dir:
        run([
            'docker', 'run', '--rm',
            '-u', f'{os.getuid()}:{os.getgid()}',
            '-v', f'{os.getcwd()}:/app',
            '-v', f'{npm_tmp_dir}:/home/node/.npm',
            '-w', '/app',
            node_image_tag,
            'sh', '-c', cmd,
        ])
    save_node_modules_cache(package_json_md5)


def npm_build_in_docker(cmd: str = 'npm run build', node_image_tag=DEFAULT_NODE_IMAGE_TAG):
    with tempfile.TemporaryDirectory(prefix='/tmp/npm-') as npm_tmp_dir:
        run([
            'docker', 'run', '--rm',
            '-u', f'{os.getuid()}:{os.getgid()}',
            '-v', f'{os.getcwd()}:/app',
            '-v', f'{npm_tmp_dir}:/home/node/.npm',
            '-w', '/app',
            node_image_tag,
            'sh', '-c', cmd,
        ])


def save_node_modules_cache(package_json_md5: str):
    if (node_modules_cache_path := NODE_MODULES_CACHES_DIR_PATH / '{}.tar'.format(package_json_md5)).exists():
        node_modules_cache_path.unlink()
    os.makedirs(NODE_MODULES_CACHES_DIR_PATH, exist_ok=True)
    run(['tar', 'czf', node_modules_cache_path, 'node_modules'])
    clear_node_modules_cache()


def get_node_modules_cache(package_json_md5: str) -> bool:
    if (node_modules_cache_path := NODE_MODULES_CACHES_DIR_PATH / '{}.tar'.format(package_json_md5)).exists():
        run(['tar', 'xzf', node_modules_cache_path])
        return True
    return False


def clear_node_modules_cache():
    run(['find', NODE_MODULES_CACHES_DIR_PATH, '-atime', f'+{NODE_MODULES_CACHES_KEEP_DAYS}', '-delete'])
