from setuptools import setup, find_packages

setup(
    name="clichess",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "clichess=src.main:main",
        ],
    },
    install_requires=[],  # Add any dependencies here
)
