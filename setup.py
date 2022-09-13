import setuptools

setuptools.setup(
    name="aiotiktok",
    version="1.2",
    author="sheldy",
    description="Tool for parse tiktok data",
    url="https://github.com/sheldygg/aiotiktok",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'aiohttp'
    ],
)
