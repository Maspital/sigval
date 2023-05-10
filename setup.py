from setuptools import setup, find_packages

setup(
    name="sigval",
    version="1.0.0",
    packages=find_packages("src", exclude=["*tests"]),
    package_dir={"": "src"},
    install_requires=[
        "pyyaml",
        "Click",
        "tox",
    ],
    entry_points={
        'console_scripts': [
            'sigval = console:cli',
        ]
    }
)
