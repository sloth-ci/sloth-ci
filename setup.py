from distutils.core import setup

from sloth import __title__, __version__, __author__, __license__

setup(
    name=__title__,
    version=__version__,
    author=__author__,
    description='CI for humans',
    long_description='CI is a simple script to perform push-based actions.',
    author_email='moigagoo@myopera.com',
    url='https://bitbucket.org/moigagoo/sloth',
    packages=['sloth'],
    package_dir={'sloth': 'sloth'},
    package_data={'sloth': ['server.conf', 'default.conf']},
    include_package_data = True,
    requires = ['CherryPy', 'requests', 'configs'],
    license=__license__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )
