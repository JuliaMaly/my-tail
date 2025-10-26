from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="my-tail",
    version="0.1.0",
    description="Simple replacement of unix tail (supports -n and -f) implemented with Click",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "click>=8.0"
    ],
    entry_points={
        "console_scripts": [
            "my-tail = my_tail.cli:main"
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)