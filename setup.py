from setuptools import setup, find_packages

setup(
    name="aquamarine-nexus",
    version="0.1.0",
    description="Sovereign Pure-Mathematics & Theoretical Physics AI Engine",
    author="Soma Dutta",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "nexus-chat=aquamarine_nexus.core.sovereign_chat_cli:main",
        ],
    },
)
