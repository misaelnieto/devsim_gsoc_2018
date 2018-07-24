from distutils.core import setup


setup(
    name='devsim',
    packages=['devsim', 'tracey'],
    version='0.1dev',
    description='DEVSIM TCAD Simulator',
    url = 'https://devsim.org',
    license='Apache 2.0',
    long_description=open('README.md').read(),
    author='Juan Sanchez',
    author_email='info@devsim.com',
)