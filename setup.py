from os import path

from setuptools import setup, find_packages


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


setup(
    name='fastapi-restful-extension',
    version='0.3.1',
    author='Shumilo Maxim',
    author_email='shumilo.mk@gmail.com',
    description='Extension for make RESTful interfaces with FastAPI.',
    long_description_content_type="text/markdown",
    long_description=read('README.md'),
    install_requires=['fastapi~=0.78.0', 'setuptools'],
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/maximshumilo/fastapi-restful-extension',
    download_url='https://github.com/maximshumilo/fastapi-restful-extension/archive/refs/tags/v0.3.0.tar.gz',
    classifiers=[
        "Framework :: FastAPI",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords=['fastapi', 'api', 'rest-api', 'async'],
    project_urls={
        'Documentation': 'https://maximshumilo.github.io/fastapi-restful-extension/',
    }
)
