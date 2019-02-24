import re
import setuptools


version = re.search(
    r'^__version__\s*=\s*\'(.*)\'',
    open('__init__.py').read(), re.M).group(1)


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='awsip',
    version=version,
    author='Rana Awais',
    author_email='rana.awais@ebryx.com',
    description='A simple package to check if ip address / range '
                'belongs to AWS.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/EbryxLabs/awsip',
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    entry_points={'console_scripts': ['awsip = awsip.__main__:main']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
