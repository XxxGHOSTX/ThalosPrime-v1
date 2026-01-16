"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

from setuptools import setup, find_packages

setup(
    name="thalos-prime",
    version="3.0.0",
    author="Tony Ray Macier III",
    description="Synthetic Biological Intelligence System",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.12",
    install_requires=[
        "Flask>=3.0.0",
        "Flask-CORS>=4.0.0",
        "python-dotenv>=1.0.0",
        "gunicorn>=21.0.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "thalos=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
)
