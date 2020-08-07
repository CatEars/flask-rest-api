import glob
import os

STDOUT = 2

def replace_in_files(fpath_pattern: str, target: str, replacement: str):
    for fpath in glob.glob(fpath_pattern, recursive=True):
        replace_in_file(fpath, target, replacement)

def replace_in_file(fpath: str, target: str, replacement: str):
    with open(fpath, 'r') as f:
        content = f.read()
    content = content.replace(target, replacement)
    with open(fpath, 'w') as f:
        f.write(content)


def task_test():
    return {
        'actions': [
            ['python', '-m', 'pytest']
        ],
        'verbosity': STDOUT
    }


def task_bootstrap():

    def rename(name: str):
        if '-' in name:
            raise AttributeError('Name cannot have dashes in it!')
        print(f'Renaming repository to "{name}"')
        original_name = 'src'
        new_name = name
        replace_in_file('./docker-compose.yml',
                        './{0}:/app/{0}'.format(original_name),
                        './{0}:/app/{0}'.format(new_name))
        replace_in_file('./pyproject.toml',
                        'flask-rest-api-template',
                        new_name)
        replace_in_files('./tests/**/*.py',
                         'from {} import'.format(original_name),
                         'from {} import'.format(new_name))
        os.rename(original_name, new_name)

    return {
        'actions': [
            ['cp', 'artifacts/settings.toml', '.'],
            ['cp', 'artifacts/.secrets.toml', '.'],
            (rename, )
        ],
        'params': [
            {
                'name': 'name',
                'long': 'name',
                'default': ''
            }
        ],
        'verbosity': STDOUT
    }
