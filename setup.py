from setuptools import setup

setup(
    name="bitbucket-cli",
    version="0.1",
    description="Atlassian Bitbucket Server command line interface",
    url="https://github.com/sbmueller/bitbucket-cli",
    author="Sebastian Müller",
    author_email="gsenpo@gmail.com",
    license="MIT",
    packages=["bitbucket_cli"],
    zip_safe=False,
    scripts=["bin/bitbucket"],
)
