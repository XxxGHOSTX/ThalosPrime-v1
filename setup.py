"""
© 2026 Tony Ray Macier III. All rights reserved.

Thalos Prime™ is a proprietary system.
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

# Read version from VERSION file
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            return f.read().strip()
    return '1.0.0'

setup(
    name='thalos-prime',
    version=get_version(),
    description='Synthetic Biological Intelligence System',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Tony Ray Macier III',
    author_email='contact@example.com',
    url='https://github.com/XxxGHOSTX/ThalosPrime-v1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    install_requires=[
        'Flask>=3.0.0',
        'Flask-CORS>=4.0.0',
        'python-dotenv>=1.0.0',
        'gunicorn>=21.0.0',
        'numpy>=1.24.0',
        'scipy>=1.10.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'pytest-asyncio>=0.21.0',
            'black>=23.7.0',
            'isort>=5.12.0',
            'mypy>=1.5.0',
            'flake8>=6.1.0',
            'pylint>=2.17.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'thalos=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    include_package_data=True,
    zip_safe=False,
)
