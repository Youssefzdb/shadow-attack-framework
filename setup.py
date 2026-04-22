from setuptools import setup, find_packages
setup(
    name="shadow-attack-framework",
    version="1.0.0",
    author="Shadow Core",
    description="Advanced Network Attack Simulation & Penetration Testing Toolkit",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["colorama", "python-whois", "requests"],
    entry_points={"console_scripts": ["shadow-attack=main:main"]},
)
