from setuptools import setup, find_packages

setup(
    name="iron_ledger",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "iron-ledger=cli:main",
        ],
    },
)
