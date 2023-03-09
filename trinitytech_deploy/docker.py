import random

from trinitytech_deploy import run, safe_kebab
from trinitytech_deploy.assets import get_assets_file_content, exec_assets_template


def generate_dockerfile(template_name: str, dockerfile_name: str = 'Dockerfile'):
    with open(dockerfile_name, mode='w') as dockerfile:
        dockerfile.write(get_assets_file_content(f'dockerfile/{template_name}.Dockerfile'))


def generate_dockerignore(lines: list[str], dockerignore_name: str = '.dockerignore'):
    with open(dockerignore_name, mode='w') as dockerignore:
        dockerignore.write('\n'.join(lines))


def docker_build(
        tags: list[str],
        dockerfile='Dockerfile',
        add_hosts: dict[str, str] = None,
        build_args: dict[str, str] = None,
        options: list[str] = None,
        context_path=None
):
    cmd = ['docker', 'build', '-f', dockerfile]
    if add_hosts is not None:
        for host, ip in add_hosts.items():
            cmd.extend(['--add-host', f'{host}:{ip}'])
    if build_args is not None:
        for key, value in build_args.items():
            cmd.extend(['--build-arg', f'{key}={value}'])
    for tag in tags:
        cmd.extend(['-t', tag])
    if options is not None:
        cmd.extend(options)
    if context_path is None:
        context_path = '.'
    cmd.append(context_path)

    run(cmd)


def transfer_docker_image(images: list[str], ssh_dest: str, ssh_port=22):
    random_name = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 10))
    run(['docker', 'save', '-o', f'/tmp/{random_name}.tar', *images])
    run([
        'rsync', '-P', '-av', '--delete', '-e', f'ssh -p {ssh_port}',
        f'/tmp/{random_name}.tar', f'{ssh_dest}:/tmp/{random_name}.tar'
    ])
    run(['rm', '-f', f'/tmp/{random_name}.tar'])
    run([
        'ssh', ssh_dest, '-p', ssh_port,
        'docker', 'load', '-i', f'/tmp/{random_name}.tar'
    ])
    run([
        'ssh', ssh_dest, '-p', ssh_port,
        'rm', '-f', f'/tmp/{random_name}.tar'
    ])


def generate_docker_compose(template_name: str, values: dict, service_name: str, ssh_dest: str, ssh_port=22):
    exec_assets_template(f'docker-compose/{template_name}.docker-compose.tmpl', 'docker-compose.yml', values)
    run(['ssh', ssh_dest, '-p', ssh_port, 'mkdir', '-p', f'~/services/{safe_kebab(service_name)}'])
    run([
        'rsync', '-P', '-av', '--delete', '-e', f'ssh -p {ssh_port}',
        'docker-compose.yml',
        f'{ssh_dest}:~/services/{safe_kebab(service_name)}'
    ])


def deploy_docker_stack(service_name: str, ssh_dest: str, ssh_port=22):
    kebab_service_name = safe_kebab(service_name)
    run([
        'ssh', ssh_dest, '-p', ssh_port,
        'docker', 'stack', 'down', kebab_service_name
    ])
    run([
        'ssh', ssh_dest, '-p', ssh_port,
        'docker', 'stack', 'up', '-c', f'~/services/{kebab_service_name}/docker-compose.yml', kebab_service_name
    ])
