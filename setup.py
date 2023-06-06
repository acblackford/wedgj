import setuptools

with open("README.txt", "r") as fn:
    long_description = fn.read()

setuptools.setup(
    name="wedgj",
    version="1.1.0",
    author="Andrew Blackford of UAH, Huntsville, Alabama",
    author_email="acblackford@hotmail.com",
    description="A comprehensive python package containing useful functions for reading in and displaying publicly available severe weather-related data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acblackford/wedgj",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires='>=3.0',
)
