from setuptools import setup

import sloth_ci


try:
    readme = open('README.rst').read()
except:
    readme = sloth_ci.__long_description__


setup(
    name=sloth_ci.__title__,
    version=sloth_ci.__version__,
    author=sloth_ci.__author__,
    description=sloth_ci.__description__,
    long_description=readme,
    author_email=sloth_ci.__author_email__,
    url='https://bitbucket.org/moigagoo/sloth-ci',
    packages=[
        'sloth_ci'
    ],
    install_requires = [
        'CherryPy',
        'configs>=2.0.8'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts':
            ['sloth-ci = sloth_ci.api:main']
        }
    )
