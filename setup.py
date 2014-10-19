from distutils.core import setup

from os.path import join

import sloth_ci
from sloth_ci.utils import get_default_configs_path


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
        'awesome-slugify',
        'configs>=3.0.2'
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
    },
    data_files=[
        (get_default_configs_path(), ['server.conf']),
        (join(get_default_configs_path(), 'apps'), [])
    ]
)
