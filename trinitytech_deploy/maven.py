import os

from trinitytech_deploy.os import HOME_PATH, run

MAVEN_CACHE_DIR_PATH = HOME_PATH / '.cache' / 'trinitytech-deploy' / 'maven-cache'
DEFAULT_MAVEN_IMAGE_TAG = 'maven:3.8.6-openjdk-8'


def maven_package_in_docker(cmd: str = 'mvn -Duser.home=/var/maven package -DskipTests -q'):
    os.makedirs(MAVEN_CACHE_DIR_PATH, exist_ok=True)
    run([
        'docker', 'run', '--rm',
        '-u', f'{os.getuid()}:{os.getgid()}',
        '-v', f'{os.getcwd()}:/app',
        '-w', '/app',
        '-e', 'MAVEN_CONFIG=/var/maven/.m2',
        '-v', f'{MAVEN_CACHE_DIR_PATH}:/var/maven/.m2',
        DEFAULT_MAVEN_IMAGE_TAG,
        'sh', '-c', cmd,
    ])
