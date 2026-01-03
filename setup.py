"""Setup configuration for Airbrowser."""

from setuptools import find_packages, setup


# Read the README file
def read_readme():
    with open("README.md", encoding="utf-8") as fh:
        return fh.read()


# Read requirements from requirements.txt
def read_requirements():
    with open("requirements.txt", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]


setup(
    name="airbrowser-mcp",
    version="1.11.0",
    author="Ivan Fokeev",
    author_email="vanya@vanya.cc",
    description="Airbrowser: AI Remote Browser - Undetectable Chrome runtime for AI agents",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ifokeev/airbrowser-mcp",
    project_urls={
        "Bug Tracker": "https://github.com/ifokeev/airbrowser-mcp/issues",
        "Source Code": "https://github.com/ifokeev/airbrowser-mcp",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "requests-mock>=1.10.0",
            "coverage>=7.0.0",
        ],
        "examples": [
            "aiohttp>=3.8.0",
            "asyncio",
        ],
    },
    entry_points={
        "console_scripts": [
            "airbrowser=airbrowser.server.api:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    keywords=[
        "selenium",
        "browser",
        "automation",
        "testing",
        "web-scraping",
        "chrome",
        "proxy",
        "undetected",
        "docker",
        "seleniumbase",
        "agent",
        "mcp",
    ],
    zip_safe=False,
)
