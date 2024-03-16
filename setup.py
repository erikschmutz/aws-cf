from setuptools import setup
from aws_cf.meta import VERSION

setup(
    name='aws-cf',
    version=VERSION,
    description='Simple way to deploy AWS stacks',
    long_description='Simple way to deploy AWS stacks',
    url='https://github.com/erikschmutz/aws-cf/',
    author='Erik Rehn',
    author_email='erik.rehn98@gmail.com',
    license='BSD 2-clause',
    packages=['aws_cf', 'aws_cf.utils', 'aws_cf.commands'],
    install_requires=['pydantic', 'boto3', 'pyaml'],
    entry_points={
        'console_scripts': [
            'aws-cf = aws_cf.__main__:main'
        ]
    },
    classifiers=[],
)
