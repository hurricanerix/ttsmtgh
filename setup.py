from setuptools import setup, find_packages

from ttsmtgh import version

name = "ttsmtgh"

setup(
    name=name,
    version=version,
    author="Richard Hawkins",
    author_email="hurricanerix@gmail.com",
    description="ttsmtgh",
    license="Apache License, (2.0)",
    keywords="tts mtg tool",
    url="http://github.com/hurricanerix/ttsmtgh",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        ],
    install_requires=[],
    )
