from setuptools import setup

import myextension as ext


package = 'sloth_ci.ext'

setup(
    name=ext.__title__,
    version=ext.__version__,
    author=ext.__author__,
    description=ext.__description__,
    long_description=ext.__doc__,
    author_email=ext.__author_email__,
    url='https://bitbucket.org/moigagoo/sloth-ci-extensions',
    py_modules=['%s.%s' % (package, ext.__name__)],
    packages=[package],
    package_dir={package: '.'},
    install_requires = [
        'sloth-ci>=2.0.1'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
)
