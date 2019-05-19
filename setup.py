from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='thameswater',
    version='0.5',
    long_description=readme(),
    description='An application for dowloading daily water usage data from Thames Water (UK).',
    author='Paul D.Smith',
    author_email='paul@pauldsmith.org.uk',
    url='https://github.com/papadeltasierrra/thameswater',
    packages=['thameswater'],
    install_requires=[
        'selenium'
    ],
    entry_points = {
        'console_scripts': ['thameswater=thameswater.thameswater:main'],
    },
    include_package_data=True
)
