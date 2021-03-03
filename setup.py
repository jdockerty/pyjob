from setuptools import setup, find_packages

setup(
    name="pyjob",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'loguru',
        'pyjob',
    ],
    entry_points="""
    [console_scripts]
    pyjob=pyjob.cli.main:cli
    """
)