from setuptools import setup, find_packages

setup(
    name="cellular_automaton",
    version="0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "cellular_automaton=src.main:main",
        ],
    },
)
