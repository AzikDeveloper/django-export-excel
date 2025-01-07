from setuptools import setup, find_packages
from os import path

# Read the contents of requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

setup(
    name='django_export_excel',
    version='1.0.4',
    description='Django package for exporting data to Excel file with included admin integration',
    author='Azizbek Xushnazarov',
    author_email='azikdevapps@gmail.com',
    url='https://github.com/AzikDeveloper/django-export-excel',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)