#!/usr/bin/env python

import os
import subprocess
import sys

# Required third-party imports, must be specified in pyproject.toml.
import packaging.version
from setuptools import setup


def process_options():
    """
    Determine all runtime options, returning a dictionary of the results.  The
    keys are:
        'rootdir': str
            The root directory of the setup.  Almost certainly the directory
            that this setup.py file is contained in.
        'release': bool
            Is this a release build (True) or a local development build (False)
    """
    options = {}
    options['rootdir'] = os.path.dirname(os.path.abspath(__file__))
    options = _determine_version(options)
    return options


def _determine_version(options):
    """
    Adds the 'short_version', 'version' and 'release' options.

    Read from the VERSION file to discover the version.  This should be a
    single line file containing valid Python package public identifier (see PEP
    440), for example
      4.5.2rc2
      5.0.0
      5.1.1a1
    We do that here rather than in setup.cfg so we can apply the local
    versioning number as well.
    """
    version_filename = os.path.join(options['rootdir'], 'VERSION')
    with open(version_filename, "r") as version_file:
        version_string = version_file.read().strip()
    version = packaging.version.parse(version_string)
    if isinstance(version, packaging.version.LegacyVersion):
        raise ValueError("invalid version: " + version_string)
    options['short_version'] = str(version.public)
    options['release'] = not version.is_devrelease
    if not options['release']:
        # Put the version string into canonical form, if it wasn't already.
        version_string = str(version)
        version_string += "+"
        try:
            git_out = subprocess.run(
                ('git', 'rev-parse', '--verify', '--short=7', 'HEAD'),
                check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            git_hash = git_out.stdout.decode(sys.stdout.encoding).strip()
            version_string += git_hash or "nogit"
        # CalledProcessError is for if the git command fails for internal
        # reasons (e.g. we're not in a git repository), OSError is for if
        # something goes wrong when trying to run git (e.g. it's not installed,
        # or a permission error).
        except (subprocess.CalledProcessError, OSError):
            version_string += "nogit"
    options['version'] = version_string
    return options


def create_version_py_file(options):
    """
    Generate and write out the file qutip/version.py, which is used to produce
    the '__version__' information for the module.  This function will overwrite
    an existing file at that location.
    """
    filename = os.path.join(
        options['rootdir'], 'src', 'qutip_qip', 'version.py')
    content = "\n".join([
        "# This file is automatically generated by qutip-qip's setup.py.",
        f"short_version = '{options['short_version']}'",
        f"version = '{options['version']}'",
        f"release = {options['release']}",
    ])
    with open(filename, 'w') as file:
        print(content, file=file)


if __name__ == "__main__":
    options = process_options()
    create_version_py_file(options)
    # Most of the kwargs to setup are defined in setup.cfg; the only ones we
    # keep here are ones that we have done some compile-time processing on.
    setup(
        version=options['version'],
        extras_require={
            'qiskit': ['qiskit>=0.36.2']
        }
    )
