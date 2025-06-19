from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="personal-finance-manager",
    version="0.2.0",
    author="Mohit Saharan",
    author_email="mohit@msaharan.com",
    description="A sophisticated Python-based personal finance management application that helps you track and manage your financial portfolio with advanced features for investments, inventory, and expenses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msaharan/personal_finance",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "personal-finance-manager=main:main",
        ],
    },
) 