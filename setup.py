from setuptools import setup, find_packages

setup(
    name='fastapi-restful-extension',
    version='0.3.0',
    author="Shumilo Maxim",
    author_email="shumilo.mk@gmail.com",
    description='Extension for make RESTful interfaces with FastAPI.',
    long_description="",
    install_requires=['fastapi~=0.78.0', 'setuptools~=62.3.2'],
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/maximshumilo/fastapi-restful-extension',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
