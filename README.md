# `aws-cf`: Lightweight AWS CloudFormation Framework
The aws-cf library is a straightforward and minimal tool designed to simplify the deployment of AWS CloudFormation stacks. It offers a set of commands that make it easier to deploy, compare, and package your AWS infrastructure resources.

Being a superset of CloudFormation, aws-cf seamlessly integrates with any existing CloudFormation setup, making adoption smooth and hassle-free.

Key Commands:
```bash
aws-cf deploy   # Deploys the stacks defined in the services.yml file
aws-cf diff     # Checks for differences in the stacks listed in the services.yml file
aws-cf package  # Packages the stacks mentioned in the services.yml file
```
Getting Started
To begin, install the aws-cf library via pip:

```bash
pip3 install aws-cf
```

Initialize a new project by running:

```bash
aws-cf init
```
This will create a new project. You can now start by adding your first environment configuration.

## Sample Configuration (services.yml):

```yml
Environments:
  - name: prod
    profile: `<AWS_PROFILE>`
    region: `eu-central-1`
    artifacts: `<BUCKET_NAME_FOR_ARTIFACTS>`

Stacks:
  - path: `$root/aws/VPC.yml`
    name: `Network`

  - path: `$root/aws/API.yml`
    name: `API`
```
In this example configuration file, services.yml, environments and stacks are defined for deployment. Each environment specifies an AWS profile, region, and artifact bucket, while stacks are defined with their respective file paths and names.

To deploy these stacks, simply run the aws-cf deploy command. The utility will deploy each stack in the order specified, using the root directory as the base path.

## Why Use aws-cf Instead of More Opinionated Tools?
aws-cf provides a simple wrapper around CloudFormation, serving as an alternative to more opinionated frameworks like Terraform or AWS CDK. Unlike these tools, aws-cf does not alter the underlying CloudFormation, making it easy to stop using if needed without major changes to your infrastructure.

## Core Principles
Seamless Integration: aws-cf works with your existing CloudFormation templates without requiring any modifications.
Non-Intrusive: You can easily revert to writing CloudFormation directly and managing deployments with bash scripts, without any major refactors.
Minimal API: The core library remains lightweight, with additional features available through optional add-ons rather than baked into the core.