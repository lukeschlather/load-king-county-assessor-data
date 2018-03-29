import os
from setuptools import setup, find_packages

setup(
    name='assessor',
    description='Processess data from the King County, WA assessor.',
    install_requires=('pytest'),
    entry_points={
        'console_scripts': [
            'create-sqlite-database = lib.load_square_footage:main'
        ]
    },
)
