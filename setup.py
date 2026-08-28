from setuptools import setup, find_packages

setup(
    name="aquamarine-nexus",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "aquamarine-nexus=aquamarine_nexus.cli:main",
            "aqua=aquamarine_nexus.core.aqua_shell_editor:main",
        ],
    },
)
