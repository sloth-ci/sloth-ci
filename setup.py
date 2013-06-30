from distutils.core import setup

setup(
    name='sloth-ci',
    version='0.1.5',
    author='Konstantin Molchanov',
    description='CI for humans',
    long_description='CI is a simple script to perform push-based actions.',
    author_email='moigagoo@myopera.com',
    url='https://bitbucket.org/moigagoo/sloth',
    packages=['sloth'],
    package_dir={'sloth': 'sloth'},
    package_data={'sloth': ['server.conf', 'default.conf']},
    include_package_data = True,
    install_requires = ['CherryPy', 'requests', 'configs'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )
