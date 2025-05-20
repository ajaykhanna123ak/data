from setuptools import setup, find_packages

def load_requirements(filename="requirements.txt"):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="mymodule",
    version="0.1.0",
    description="A simple greeting module",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    install_requires=load_requirements(),
    python_requires=">=3.6",
)

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

python -m build
