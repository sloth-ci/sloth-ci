from distutils.core import setup

import sloth_ci


try:
    readme = open('README.rst').read()
except:
    readme = 'Sloth CI: CI for Humans.'


setup(
    name=sloth_ci.__title__,
    version=sloth_ci.__version__,
    author=sloth_ci.__author__,
    description='CI for humans',
    long_description=readme,
    author_email='moigagoo@live.com',
    url='https://bitbucket.org/moigagoo/sloth-ci',
    packages=[
        'sloth_ci',
        'sloth_ci.validators'
    ],
    install_requires = [
        'CherryPy',
        'configs>=2.0.7'
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
