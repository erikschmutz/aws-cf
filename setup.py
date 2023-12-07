from setuptools import setup

setup(
    name='aws-cf',
    version='0.0.4',    
    description='Simple way to deploy AWS stacks',
    long_description='Simple way to deploy AWS stacks',
    url='https://github.com/erikschmutz/aws-cf/',
    author='Erik Rehn',
    author_email='erik.rehn98@gmail.com',
    license='BSD 2-clause',
    packages=['src'],
    install_requires=['pydantic', 'boto3'],

    classifiers=[],
)