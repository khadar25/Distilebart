import pathlib
from setuptools import setup
from setuptools import find_packages
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="TextSumarization_DistilBertModel",
    version="1.0.0",
    description="It uses to summaries the Text using pretrained models of Bart and In this package DistilBertModel ass Default model to Sumarize the Text",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/khadar25/Distilebart",
    author="Khadar vali",
    author_email="khadarv8977@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
