from setuptools import find_packages, setup

def read(filename):
    with open(filename, "r") as file:
        return file.read()

setup(
    name="dj_notification",
    version="1.0.0",
    packages=find_packages(),
    url="https://github.com/RadwanHegazy/dj_notification",
    license="MIT",
    description="Build your notification system fast and easy in drf",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Radwan Gaber Hijazi",
    python_requires=">=3.8",
    project_urls={
        "source": "https://github.com/RadwanHegazy/dj_notification"
    }
)