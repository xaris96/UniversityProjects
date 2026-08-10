"""Setup configuration for the Mars Mission application."""
from setuptools import setup, find_packages

setup(
    name="mars_mission",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask==3.1.0",
        "pytest==8.3.5",
        "Werkzeug==3.1.3",
        "pytest-cov==6.0.0",
        "pytest-flask==1.3.0",
        "pylint==3.3.6",
        "astroid==3.3.9",
        "flask-cors==4.0.0",
        "python-dotenv==1.0.0"
    ],
    entry_points={
        'console_scripts': [
            'mars-mission=app:main',
        ],
    },
)
