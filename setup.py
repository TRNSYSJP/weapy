# coding: utf-8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weapy", # Replace with your own username
    version="0.1.4",
    install_requires=[
        "numpy",
        "pandas",
        
    ],
    entry_points={
        'console_scripts': [
            # 'wea=weapy:main',
        ],
    },
    author="Yuichi Yasuda",
    author_email="yasuda@qcd.co.jp",
    description="Weather data reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuizi/weapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)