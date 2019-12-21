import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="insta_parser-wolfela", # Replace with your own username
    version="0.0.1",
    author="Lauren Wolfe",
    author_email="wolfela@uw.edu",
    description="Helper functions to make data normalization easier!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laurenwolfe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)