from setuptools import setup, find_packages

setup(
    name="vorik-database",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=2.0.0",
        "asyncpg>=0.28.0",
        "pgvector>=0.2.0",
        "vorik-schemas",
    ],
)
