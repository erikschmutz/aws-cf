# `aws-cf`: Unoptionated AWS CloudFormation Framework

The **aws-cf** utility library is a simple and minimal tool designed to streamline the deployment of AWS CloudFormation stacks. It provides a set of commands that make deploying, comparing changes, and packaging artifacts for your AWS infrastructure easier.

It is a superset of cloudformation meaning that any existing cloudformation should be able to be integrated with the framework.

Usage:

```bash
aws-cf deploy # will deploy stacks in the services.yml file
aws-cf diff # will check for differences the stacks in the services.yml file
aws-cf package # will package the stacks in the services.yml file
```

## Getting started 
Start by installing the pip dependency 

```bash
pip3 install aws-cf
```

Then you can setup a new project by running
```bash
aws-cf init
```

This will initailise an empty project. You can now add your first environment.

## Example Configuration (services.yml):
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

This example configuration file, services.yml, defines environments and stacks to deploy. Each environment specifies the AWS profile, region, and artifact bucket. Stacks are defined with their respective paths and names.

To deploy these stacks, use the aws-cf deploy command, providing the configuration file as an argument. The utility will deploy each stack in the specified order, starting with the root directory as the base.

## Core priciples

1. Unlike many frameworks outthere, `aws-cf` should be able to integrate with existing cloudformation without needing any changes to the underlying code.
2. It should be possible without any refactors to the underlying code to remove the `aws-cf` and go back to writing cloudformation directly along with bash scripts.
3. It should be a minimal API, additional features should be part of add-ons instead of the core library.

## When to use this framework compared to more opinioate