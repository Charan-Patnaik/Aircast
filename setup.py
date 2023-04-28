from setuptools import setup, find_packages

setup(
    name='my_cli_app',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'my-cli-app=cli.main:app'
        ]
    },
    install_requires=[
        'typer',
        # Other dependencies
    ],
    author='Aircast',
    description='My Typer CLI application',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
