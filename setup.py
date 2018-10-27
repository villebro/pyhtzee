from setuptools import find_packages, setup


setup(
    name='pyhtzee',
    version='0.9.0',
    description='Yahtzee game engine',
    author='Ville Brofeldt',
    author_email='ville.brofeldt@iki.fi',
    maintainer='Ville Brofeldt',
    maintainer_email='ville.brofeldt@iki.fi',
    url='https://github.com/villebro/pyhtzee',
    license='MIT',
    packages=find_packages(exclude='tests'),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)
