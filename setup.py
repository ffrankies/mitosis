"""Setup script for the mitosis library.
"""
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="mitosis",
    version="0.0.0",
    author="ffrankies",
    author_email="wanyef@mail.gvsu.edu",
    description="Python3 implementation of a simple genetic algorithm",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/ffrankies/mitosis",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Ubuntu",
    ),
)
