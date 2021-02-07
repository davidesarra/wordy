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
        "https://github.com/davidesarra/wordy.git@732c1a839ec49b56c8b55b9021a7fe811b4aa740#subdirectory=wordylib"
    ],
)
