import glob
import os

STDOUT = 2

def task_test():
    return {
        'actions': [
            ['python', '-m', 'pytest']
        ],
        'verbosity': STDOUT
    }


def task_coverage():
    return {
        'actions': [
            ['python', '-m', 'pytest', '--cov=src',
             '--cov-report=html', '--cov-branch']
        ],
        'verbosity': STDOUT
    }


### Bootstrap-only-section start

def replace_in_files(fpath_pattern: str, target: str, replacement: str):
    for fpath in glob.glob(fpath_pattern, recursive=True):
        replace_in_file(fpath, target, replacement)

def replace_in_file(fpath: str, target: str, replacement: str):
    with open(fpath, 'r') as f:
        content = f.read()
    content = content.replace(target, replacement)
    with open(fpath, 'w') as f:
        f.write(content)


def remove_section(fpath: str, section_name: str):
    with open(fpath, 'r') as f:
        lines = f.readlines()
    start_pattern = f'### {section_name} start'.lower()
    end_pattern = f'### {section_name} end'.lower()
    kept_lines = []
    in_section = False
    for line in lines:
        if line.lower().startswith(start_pattern):
            in_section = True
        elif line.lower().startswith(end_pattern):
            in_section = False
        elif not in_section: # never include section delimiters
            kept_lines.append(line)
    with open(fpath, 'w') as f:
        f.writelines(kept_lines)


def task_bootstrap():

    def rename(name: str):
        if '-' in name:
            raise AttributeError('Name cannot have dashes in it!')
        if not name:
            raise AttributeError('Needs to supply --name [name]')
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

    def update_dodofile():
        remove_section('./dodo.py', 'Bootstrap-only-section')

    return {
        'actions': [
            ['cp', 'artifacts/settings.toml', '.'],
            ['cp', 'artifacts/.secrets.toml', '.'],
            (rename, ),
            (update_dodofile, )
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

### Bootstrap-only-section end
