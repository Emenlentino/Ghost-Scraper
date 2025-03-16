# setup.py
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myproject",  # Replace with your actual package name.
    version="0.1.0",
    author="Emenlentino",
    author_email="emenlentino@gmail.com",
    description="A first world-class, production-ready scraping & data processing project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emenlentino/ghost-scraper-tools",  # Update your repo URL.
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.2.0",
        "beautifulsoup4>=4.9.0",
        "rich>=10.0.0",
        "tenacity>=8.0.0",
        "sentry-sdk>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "myproject=myproject.main:main",
        ],
    },
)
