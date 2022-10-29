from setuptools import setup, find_packages


setup(
    name='pzem-read',
    version='0.1.0',
    description='read from PZEM-0xx Energy Meter Modules',
    long_description=open("README.md").read(),
    url='',
    author='Daniel Hiepler',
    author_email='d-pzem@coderdu.de',
    license='unlicense',
    keywords='pzem energy meter rs485 serial json',
    py_modules=['pzem'],
    install_requires=[
        'click',
        'minimalmodbus'
    ],
    #packages=find_packages(exclude=['tests*']),
    entry_points={
        'console_scripts': [
            'pzem=pzem.cat:read_pzem',
        ]
    }
)
