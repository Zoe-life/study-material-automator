"""Setup script for Study Material Automator"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="study-material-automator",
    version="0.1.0",
    author="Zoe-life",
    description="Automated system to convert educational content into structured study materials",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zoe-life/study-material-automator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.10.0",
        "opencv-python>=4.8.0",
        "moviepy>=1.0.3",
        "yt-dlp>=2023.11.0",
        "openai>=1.3.0",
        "tiktoken>=0.5.0",
        "Pillow>=10.0.0",
        "matplotlib>=3.8.0",
        "graphviz>=0.20.1",
        "numpy>=1.24.0",
        "pandas>=2.1.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "pyyaml>=6.0.1",
    ],
    entry_points={
        "console_scripts": [
            "study-automator=main:main",
        ],
    },
)
