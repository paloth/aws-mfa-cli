from setuptools import setup

setup(
    name="aws-key-management",
    version="0.1",
    py_module=["mfa"],
    install_requires=["Click", "boto3", "botocore"],
    entry_points="""
    [console_scripts]
    akm=src.main:run
    """,
)
