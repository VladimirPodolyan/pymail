import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymail",
    version="0.0.1",
    author="PVladimir",
    author_email="vladimir.podolyan64@gmail.com",
    description="gmail client for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VladimirPodolyan/pymail",
    packages=setuptools.find_packages(),
    install_requires=['pytest>=4.4'],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
