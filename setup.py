from distutils.core import setup

setup(
    name='Picatcha',
    version='0.1',
    author='Picatcha',
    author_email='contact@picatcha.com',
    packages=['picatcha'],
    url='http://pypi.python.org/pypi/Picatcha/',
    license='The MIT License',
    description='Python library for Picatcha',
    long_description=open('README.txt').read(),
    requires=['simplejson'],
)
