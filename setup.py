from setuptools import find_packages, setup

with open("README.rst") as f:
    readme = f.read()
with open("HISTORY.rst") as f:
    history = f.read()

setup(
    name="anthem",
    version="0.8.0",
    description="Make your Odoo scripts sing.",
    long_description=readme + "\n\n" + history,
    author="Camptocamp",
    author_email="info@camptocamp.com",
    url="https://github.com/camptocamp/anthem",
    license="LGPLv3+",
    packages=find_packages(exclude=("tests", "docs")),
    entry_points={"console_scripts": ["anthem = anthem.cli:main"]},
    install_requires=["future", "unicodecsv"],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ),
)
