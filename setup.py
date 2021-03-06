import pathlib
from setuptools import setup
import os


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="deltalake-db-projects",
    version="0.0.1",
    # version_config={
    #     # "template": "{tag}",
    #     # "dev_template": "{tag}.post{ccount}+git.{sha}",
    #     # "dirty_template": "{tag}.post{ccount}+git.{sha}.dirty",
    #     "template": "{tag}",
    #     "dev_template": "{tag}.dev{ccount}",
    #     "dirty_template": "{tag}.dev{ccount}.dirty",
    #     "starting_version": "0.0.1",
    #     "version_callback": None,
    #     "version_file": None,
    #     "count_commits_from_version_file": False,
    #     "branch_formatter": None,
    #     "sort_by": None,
    # },
    # setup_requires=['setuptools-git-versioning'],
    description="Projects for editing and building databricks databases",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://deltalake-db-projects.readthedocs.io/en/latest/",
    project_urls={
        'GitHub': 'https://github.com/semanticinsight/deltalake-db',
        'Documentation': 'https://deltalake-db-projects.readthedocs.io/en/latest/'
    },
    author="Shaun Ryan",
    author_email="shaun_chiburi@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["deltalake_dp"],
    install_requires=["pyyaml","jinja2","click"],
    zip_safe=False
)
