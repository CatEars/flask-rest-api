def task_bootstrap():

    def rename(name: str):
        print(f'Renaming repository to "{name}"')

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
        'verbosity': 2
    }
