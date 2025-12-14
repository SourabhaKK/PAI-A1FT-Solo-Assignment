"""
Setup script for PAI Assignment
"""

from setuptools import setup, find_packages

setup(
    name="pai-assignment",
    version="1.0.0",
    author="Sourabha K Kallapur",
    description="Programming for AI Assignment - Health Dashboard and Basket Analysis",
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'pandas>=2.0.3',
        'numpy>=1.24.3',
        'matplotlib>=3.7.2',
        'requests>=2.31.0',
        'pytest>=7.4.0',
        'pytest-cov>=4.1.0',
        'colorama>=0.4.6',
        'pypdf>=6.4.1'
    ],
)
