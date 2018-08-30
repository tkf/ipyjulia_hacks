from setuptools import setup, find_packages

setup(
    name="ipyjulia_hacks",
    version="0.0.0",
    packages=find_packages("src"),
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
