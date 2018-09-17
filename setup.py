from setuptools import setup, find_packages
import sys

packages = find_packages("src")
if sys.version_info[0] == 2:
    packages = [p for p in packages if not p.startswith((
        "ipyjulia_hacks.ipy",
        "ipyjulia_hacks.py3",
    ))]

setup(
    name="ipyjulia_hacks",
    version="0.0.0",
    packages=packages,
    package_dir={"": "src"},
    package_data={"ipyjulia_hacks": ["**/*.jl"]},
    author="Takafumi Arakaki",
    author_email="aka.tkf@gmail.com",
    # url="https://github.com/tkf/ipyjulia_hacks",
    license="MIT",  # SPDX short identifier
    # description="ipyjulia_hacks - THIS DOES WHAT",
    long_description=open("README.rst").read(),
    # keywords="KEYWORD, KEYWORD, KEYWORD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        # see: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    install_requires=[
        "cached-property",
    ],
    # entry_points={
    #     "console_scripts": ["PROGRAM_NAME = ipyjulia_hacks.cli:main"],
    # },
)
