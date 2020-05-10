from setuptools import setup, find_packages


NAME = "wordyapi"
VERSION = "0.0.1"


def get_requirements():
    with open(file="requirements.txt", mode="r") as file:
        return [line.strip() for line in file.readlines()]


setup(
    name=NAME,
    version=VERSION,
    include_package_data=True,
    packages=find_packages(exclude=["tests"]),
    install_requires=get_requirements(),
    dependency_links=[
        "https://github.com/davidesarra/wordy.git@70c1a49e2553b959105f2ba93f9c0b5b3761f24c#subdirectory=wordylib"
    ],
)
