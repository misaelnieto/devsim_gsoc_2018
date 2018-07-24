from setuptools import setup


setup(
    name='devsim',
    packages=['devsim', 'tracey'],
    version='0.0.1',
    description='DEVSIM TCAD Simulator',
    url='https://devsim.org',
    license='Apache 2.0',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Juan Sanchez',
    author_email='info@devsim.com',
    include_package_data=True,
    project_urls={
        'Documentation': 'https://devsim.org/',
        'Source': 'https://github.com/devsim/devsim',
        'Tracker': 'https://github.com/devsim/devsim/issues',
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords='TCAD semiconductors',
    python_requires='>=3',
    install_requires=[
        'numpy'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
)
