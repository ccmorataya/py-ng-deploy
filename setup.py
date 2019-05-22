import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'readme.md').read_text()

# This call to setup() does all the work
setup(
    name='ng-py-deploy',
    version='0.0.1',
    description='Compile angular project and upload to sftp',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/ccmorataya/ng-py-deploy',
    author='Cristian Morataya',
    author_email='cris.morataya@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['upload', 'bld'],
    include_package_data=True,
    install_requires=['pysftp'],
)
