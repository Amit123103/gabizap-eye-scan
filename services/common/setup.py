from setuptools import setup, find_packages

setup(
    name="gabizap-common",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "loguru",
        "prometheus-client",
        "opentelemetry-api",
        "opentelemetry-sdk",
    ],
)
