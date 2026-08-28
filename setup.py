from setuptools import setup, find_packages

setup(
    name="aquamarine-nexus",
    version="1.0.0",
    author="Aquamarine Hoshino",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "aquamarine-nexus=aquamarine_nexus.cli:main",
            "aqua=aquamarine_nexus.core.aqua_shell_editor:main",
        ],
    },
)
