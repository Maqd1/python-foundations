from setuptools import find_packages, setup


setup(
    name="school-management-system",
    version="1.0.0",
    description="A Python-based school management system",
    packages=find_packages(),
    install_requires=[
        "reportlab",
    ],
)
