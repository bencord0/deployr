from setuptools import find_packages, setup

setup(
    name="deployr",
    version="0.1.0",
    author="Ben Cordero <bencord0@condi.me>",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
    ],
    tests_require=[
        "pytest",
        "flake8",
    ],
    entry_points={
        "console_scripts": [
            "deployr = deployr:main",
        ]
    },
)
