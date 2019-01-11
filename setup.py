import io

from setuptools import find_packages, setup

with io.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyhtzee',
    version='1.2.1',
    description='Yahtzee game engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
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
