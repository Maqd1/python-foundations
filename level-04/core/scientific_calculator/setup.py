from setuptools import find_packages, setup

setup(
    name="scientific-calculator",
    version="2.0.0",
    description="A scientific calculator package with history, config, and a plugin system.",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "calc-cli=cli:main",
        ],
    },
)
