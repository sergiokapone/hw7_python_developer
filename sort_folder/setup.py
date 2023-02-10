from setuptools import setup

from setuptools import setup, find_namespace_packages

setup(
    name='sort',
    version='1',
    description='Sorting files in folder',
    author='Sergiy Ponomarenko',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['sort = sort_folder.sort:run']}
)