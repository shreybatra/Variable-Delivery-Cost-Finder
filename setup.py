#!/usr/bin/env python
import distutils.cmd
import subprocess


from setuptools import Command, setup


class Mongo(Command):
    description = 'Run an instance on Mongodb on the local host.'
    user_options = []
    # Override subclass
    def initialize_options(self):
       pass

    # Override subclass
    def finalize_options(self):
       pass

    def run(self):
        command='brew services start mongo;'
        subprocess.run(command, check=True, shell=True)


class Reset(Command):
    description = 'reset the project'
    user_options = []

    # Override subclass
    def initialize_options(self):
       pass

    # Override subclass
    def finalize_options(self):
       pass

    def run(self):
        command='rm requests.pickle;'
        command+='python3 remaster.py;'
        command+='python3 temp.py;'

        subprocess.run(command, check=True, shell=True)

setup(
    name='Variable-Delivery-Cost-Finder',
    description='Variable Delivery Cost Finder for any e-commerce based' \
    'on various parameters',
    url='https://github.com/shreybatra/Variable-Delivery-Cost-Finder',
    long_description=open('README.md').read(),
    install_requires=[open('requirements.txt').read()],
    cmdclass={
        'reset': Reset,
        'mongo': Mongo
    },
)
