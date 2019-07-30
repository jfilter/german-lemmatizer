from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

classifiers = [
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "License :: OSI Approved :: MIT License",
    "Topic :: Utilities",
]

setup(
    name="german_lemmatizer",
    version="0.1.1",
    description="A Python package (using a Docker image under the hood) to lemmatize German texts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jfilter/german-lemmatizer",
    author="Johannes Filter",
    author_email="hi@jfilter.de",
    license="MIT",
    packages=["german_lemmatizer"],
    classifiers=classifiers,
    install_requires=["docker", "joblib", "tqdm"],
)

