#!/usr/bin/env python
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="growattRS232",
    version="1.0.0",
    description=(
        "Python wrapper for getting data asynchronously "
        "from Growatt inverters "
        "via serial usb RS232 connection and modbus RTU protocol."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ArdescoConsulting/growattRS232",
    author="Manuel Stevens",
    author_email="manuel.stevens@ardesco.be",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
    ],
    keywords="growatt rs232 modbus",
    packages=find_packages(),
    python_requires=">=3.6, <4",
    install_requires=["pymodbus"],
    include_package_data=True,
    # fmt: off
    project_urls={
        "Bug Reports":
        "https://github.com/ArdescoConsulting/growattRS232/issues",
        "Source":
        "https://github.com/ArdescoConsulting/growattRS232",
    },
    # fmt: on
)
