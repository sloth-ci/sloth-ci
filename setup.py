from setuptools import setup

from os.path import join

import sloth_ci


try:
    long_description = open('README.rst').read()
except:
    long_description = sloth_ci.__long_description__


setup(
    name=sloth_ci.__title__,
    version=sloth_ci.__version__,
    author=sloth_ci.__author__,
    description=sloth_ci.__description__,
    long_description=long_description,
    author_email=sloth_ci.__author_email__,
    url='https://bitbucket.org/moigagoo/sloth-ci',
    packages=['sloth_ci'],
    install_requires = [
        'CherryPy',
        'Routes',
        'awesome-slugify',
        'PyYAML',
        'docopt'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Framework :: CherryPy'],
    entry_points={
        'console_scripts':
            ['sloth-ci = sloth_ci.cli:main']
    }
)
