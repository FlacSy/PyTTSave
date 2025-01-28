from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.readlines()

setup(
    name="PyTTSave",
    version="1.0.0",
    description="Wrapper for TTSave API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="FlacSy",
    author_email="flacsy.x@gmail.com",
    url="https://github.com/FlacSy/PyTTSave",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.10.0",
)