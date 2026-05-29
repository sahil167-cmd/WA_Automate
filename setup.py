from setuptools import setup, find_packages

setup(
    name="wa_automate",
    version="0.1.0",
    description="Professional WhatsApp Automation tool using Selenium and Chrome Web Driver.",
    author="sahil167-cmd",
    author_email="borhadesahil167@gmail.com",
    url="https://github.com/sahil167-cmd/WA_Automate",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "selenium>=4.10.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "wa-automate=automate:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
