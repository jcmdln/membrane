from setuptools import (find_packages, setup)


def Open(File):
    with open(File) as f:
        return f.read()


setup(
    name="membrane",
    version="0.1.0",
    description="",
    long_description=Open("README.md"),
    license=Open("LICENSE.md"),
    url="https://github.com/jcmdln/membrane",
    author="Johnathan C. Maudlin",

    install_requires=[
        "click",
        "requests",
    ],

    # pip install --upgrade -e .[devel]
    extras_require={
        "devel": {
            "autopep8",
            "flake8",
        },
    },

    packages=find_packages(
        exclude=[
            "docs",
            "tests"
        ]
    ),

    entry_points={
        "console_scripts": [
            "membrane = src.main:main",
        ],
    },
)
