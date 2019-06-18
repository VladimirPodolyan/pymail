import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-mail",
    version="0.0.4",
    author="PVladimir",
    author_email="vladimir.podolyan64@gmail.com",
    description="Provides data from the gmail mailbox in a human readable type",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VladimirPodolyan/py-mail",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ],
)
