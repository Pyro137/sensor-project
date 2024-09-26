from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    """
    This function will return the list of requirements
    """
    with open("requirements.txt") as f:
        requirements_list = f.readlines()
        requirements_list = [req.replace("\n", "") for req in requirements_list]
        if "-e ." in requirements_list:
            requirements_list.remove("-e .")
        return requirements_list


setup(
    name='sensor',
    version='0.1',
    packages=find_packages(),
    install_requires=get_requirements(),
    
)

