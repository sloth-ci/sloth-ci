from distutils.core import setup

import sloth

setup(
    requires = ['CherryPy', 'requests', 'configs'],
    name=sloth.__title__,
    version=sloth.__version__,
    author=sloth.__author__,
    description='CI for humans',
    long_description='CI is a simple script to perform push-based actions.',
    author_email='moigagoo@myopera.com',
    url='https://bitbucket.org/moigagoo/sloth',
    packages=['sloth'],
    package_dir={'sloth': 'sloth'},
    package_data={'sloth': ['server.conf', 'default.conf']},
    include_package_data = True,
    license=sloth.__license__,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )
