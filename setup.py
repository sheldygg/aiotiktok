import setuptools


def get_description():
    with open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()

    
    
    
setuptools.setup(
    name="aiotiktok",
    version="1.6.2",
    license='MIT',
    author="sheldy",
    description="Tool for parse tiktok data",
    url="https://github.com/sheldygg/aiotiktok",
    packages=setuptools.find_packages(),
    long_description=get_description(),
    long_description_content_type='text/markdown',
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
