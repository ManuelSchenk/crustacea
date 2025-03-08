from setuptools import setup

setup(
    name="crustacea",
    version="1.1.0",
    description="",
    author="Manuel Schenk",
    author_email="manuel.schenk.87@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    install_requires=[
        "textual[syntax]~=2.1.1",
        "icecream>=2.1.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["crustacea"], 
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "crustacea=crustacea.main:main",  
        ],
    }
)
