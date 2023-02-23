from setuptools import setup, find_packages

setup(
    name="sigma-mapping-validator",
    version="1.0.0",
    packages=find_packages("src", exclude=["*tests"]),
    package_dir={"": "src"},
    install_requires=[
        "pyyaml",
        "Click",
    ],
    entry_points={
        'console_scripts': [
            'sigval = console:cli',
        ]
    }
)
