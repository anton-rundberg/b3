# Getting started

Our infrastructure is managed using Terraform. This documentation is for App
Shacks b3. Feel free to edit it with any project-specific details.


## AWS

Each project (or project environment) should have its AWS infrastructure in a
project-specific AWS Organization sub-account. Ask your project leader to set
it up for you if it is not already done.

This also means that, in order to manage infrastructure, your IAM account
needs to have the AssumeRole policy attached on the root account.

Each resource then needs to be set up with the AWS provider and set to assume
a role (e.g. OrganizationAccountAccessRole) on the sub-account. Example:

```
provider "aws" {
  region = "eu-north-1"
  version = "~> 2.7"

  assume_role {
    role_arn     = "arn:aws:iam::SUBACCOUNT_ID:role/ROLE_NAME"
    session_name = "terraform-session"
  }
}
```

After setting up the shared-terraform-state (see Modules below) you also need
to use it in all other resources.

```
terraform {
  backend "s3" {
    bucket         = "PROJECTNAME-terraform-state"
    dynamodb_table = "terraform-state-lock-dynamo"
    encrypt        = true
    region         = "eu-north-1"
    key            = "ENVIRONMENT.RESOURCE.terraform.tfstate"
    role_arn       = "arn:aws:iam::SUBACCOUNT_ID:role/ROLE_NAME"
  }
}
```


# Modules

Use the standardised modules to create new resources whenever possible.

## AWS

### api

The docker host / application server.

Consists of an EC2 instance with a static IP, security group and SSH access.

### ecr

Docker image registry.

Consists of a registry, a policy for removal of old images from the registry
and an IAM user with a policy attached to only allow it to use said registry.
The user is intended to be used by CI to push built images to the registry.

### postgresql

Database.

Depends on the api security group so must be created after.

Consists of a RDS instance with a security group attached which only allows
ingress from the api application server.

### s3

Media storage.

Consists of an S3 bucket for media storage and an IAM user with a policy which
only is allowed access to said S3 bucket. The IAM user is intended to be used
by the application when uploading media.

### shared-terraform-state

The purpose of this module is to store the Terraform state remotely and shared
for all project participants. For chicken and egg reasons this state can't be
stored remotely.

The module consists of a S3 bucket for storing the state and a DynamoDB table
used as a mutex so that only one user can modify the infrastructure at a time.
If a failure occurs while modifying the infrastructure, a manual unlock of
this mutex might be needed.
