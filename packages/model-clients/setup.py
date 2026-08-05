from setuptools import setup, find_packages

setup(
    name="vorik-model-clients",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.24.0",
        "vorik-schemas",
    ],
)
