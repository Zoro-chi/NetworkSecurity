"""
The setup.py file is an essential part of packaging and distributing python projects.
It is used by setuptools to package projects into distributable archives, such as .tar.gz, .egg, and .whl.
"""

from setuptools import setup, find_packages
from typing import List


def get_requirements() -> List[str]:
    """
    This function reads the requirements.txt file and returns a list of requirements.
    """

    requirements_list = []

    try:
        with open("requirements.txt", "r") as f:
            # Read lines from the file
            requirements = f.readlines()
            # Process each line
            for requirement in requirements:
                # Remove leading/trailing whitespaces
                requirement = requirement.strip()
                # Ignore empty lines, comments and -e .
                if requirement and requirement != "-e .":
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")

    return requirements_list


print(get_requirements())

setup(
    name="Network_Security_Package",
    version="0.0.1",
    author="Zoro-chi",
    author_email="jagbetuyi001@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
