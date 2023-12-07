# `aws-cf`: Simplifying AWS CloudFormation Deployment

The **aws-cf** utility library is a simple and minimal tool designed to streamline the deployment of AWS CloudFormation stacks. It provides a set of commands that make deploying, comparing changes, and packaging artifacts for your AWS infrastructure easier.

Usage:

```bash
aws-cf deploy services.yml
aws-cf diff services.yml
aws-cf package services.yml
```

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