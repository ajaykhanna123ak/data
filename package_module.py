from setuptools import setup, find_packages

setup(
    name="mymodule",
    version="0.1.0",
    description="A simple greeting module",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    install_requires=[],  # List dependencies here
    python_requires=">=3.6",
)

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

python -m build
