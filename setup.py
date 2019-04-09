
from setuptools import setup

setup(
    name='db-status',
    author='Connor Mullett',
    install_requires = [
        'args',
        'Click',
        'clint',
        'psycopg2-binary'
    ],
    version='0.1.0',
    entry_points={
        'console_scripts': [
            'dbstat=db_status.main:main'
        ]
    }
)

