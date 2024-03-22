# -*- coding=utf-8 -*-
import sys
import os
import logging
import setuptools

long_description = ""
with open("README.md", "r") as fd:
    for line in fd:
        # remove github badges
        if not line.startswith("[!["):
            long_description += line

def package_to_path(package):
    """
    Convert a package (as found by setuptools.find_packages)
    e.g. "foo.bar" to usable path
    e.g. "foo/bar"
    No idea if this works on windows
    """
    return package.replace('.', '/')

def find_subdirectories(package):
    """
    Get the subdirectories within a package
    This will include resources (non-submodules) and submodules
    """
    try:
        subdirectories = next(os.walk(package_to_path(package)))[1]
    except StopIteration:
        subdirectories = []
    return subdirectories

def subdir_findall(dir, subdir):
    """
    Find all files in a subdirectory and return paths relative to dir
    This is similar to (and uses) setuptools.findall
    However, the paths returned are in the form needed for package_data
    """
    strip_n = len(dir.split('/'))
    path = '/'.join((dir, subdir))
    return ['/'.join(s.split('/')[strip_n:]) for s in setuptools.findall(path)]

def find_package_data(packages):
    """
    For a list of packages, find the package_data
    This function scans the subdirectories of a package and considers all
    non-submodule subdirectories as resources, including them in
    the package_data
    Returns a dictionary suitable for setup(package_data=<result>)
    """
    skip_tests = True
    package_data = {}
    for package in packages:
        package_data[package] = []
        for subdir in find_subdirectories(package):
            if '.'.join((package, subdir)) in packages:  # skip submodules
                logging.debug("skipping submodule %s/%s" % (package, subdir))
                continue
            if skip_tests and (subdir == 'tests'):  # skip tests
                logging.debug("skipping tests %s/%s" % (package, subdir))
                continue
            package_data[package] += subdir_findall(package_to_path(package), subdir)
    return package_data

# ----------- Override defaults here ----------------

packages = None
package_name = None
package_data = None

if packages is None:
    packages = setuptools.find_packages()

if len(packages) == 0:
    raise Exception("No valid packages found")

if package_name is None:
    package_name = packages[0]

if package_data is None:
    package_data = find_package_data(packages)

setuptools.setup(
    name="paddy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.2.2b2",
    author="Armen Beck",
    author_email="armengbeck@gmail.com",
    description="Optimize hyperparameters using the Paddy field algorithm",
    keywords="paddyfield optimization hyperparameter model selection",
    url="http://github.com/chopralab/paddy",
    packages=packages,
    zip_safe=False,
    install_requires=['scipy', 'future', 'numpy', 'matplotlib'],
    tests_require=['pandas'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
    ]
)
