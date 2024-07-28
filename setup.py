from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'IonQ QPU Batch Submission package via Pennylane'
LONG_DESCRIPTION = 'This package allows for batch submission of quantum circuits to IonQ QPUs and noisy simulators.'

# Setting up
setup(
    name="ionq_direct",
    version=VERSION,
    author="Dhruv Srinivasan",
    author_email="<dhruvs@terpmail.umd.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pennylane', 'json', 'ionizer'],
    keywords=['python', 'quantum', 'pennylane', 'IonQ', 'noisy', 'circuits'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3"
    ]
)