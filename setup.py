from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="logslice",
    version="0.1.0",
    author="logslice contributors",
    description="Extract and filter time-ranged slices from large log files without loading them into memory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/logslice",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.8",
    install_requires=[
        # no third-party runtime deps — stdlib only
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "logslice=logslice.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: System :: Logging",
        "Topic :: Utilities",
    ],
    keywords="log slice filter timestamp cli",
)
