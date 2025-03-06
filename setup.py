from setuptools import setup, find_packages

setup(
    name="osdu_ingestor",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description="A small example package",
    author="An Nguyen",
    author_email="nguyentienan1322@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)