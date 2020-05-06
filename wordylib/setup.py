from setuptools import setup, find_packages


NAME = "wordylib"
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
)
