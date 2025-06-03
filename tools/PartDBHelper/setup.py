from setuptools import setup, find_packages

setup(
    name="partdb_flask_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.0.1",
        "requests==2.26.0",
    ],
    entry_points={
        "console_scripts": [
            "run_app=app:main",
        ],
    },
) 