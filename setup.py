from distutils.core import setup

setup(
    name='sloth-ci',
    version='0.2.8',
    author='Konstantin Molchanov',
    description='CI for humans',
    long_description='Sloth is a simple script to perform push-based actions.',
    author_email='moigagoo@myopera.com',
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
            ['sloth-ci-start = sloth_ci.api:main']
        }
    )
