# setup.py per SuperAgent
from setuptools import setup, find_packages

setup(
    name="SuperAgent",
    version="1.0.0",
    description="Ecosistema AI avanzato per orchestrazione, sicurezza, compressione e automazione.",
    author="SuperAgent Team",
    packages=find_packages(),
    install_requires=[
        "flask",
        "pyjwt",
        "requests",
        "plyer",
        "torch",
        "numpy",
        "scipy",
        "matplotlib",
        "PyQt5",
        "bz2file",
        "zstandard"
    ],
    python_requires='>=3.11,<3.15',
    entry_points={
        "console_scripts": [
            "superagent=run_super_agent:main"
        ]
    },
    include_package_data=True,
)
