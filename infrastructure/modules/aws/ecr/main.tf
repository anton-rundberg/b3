variable "project" {
  description = "Project name"
}

resource "aws_ecr_repository" "registry" {
  name = var.project
}

resource "aws_ecr_lifecycle_policy" "policy" {
  repository = aws_ecr_repository.registry.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 5,
            "description": "Only keep 5 latest untagged images",
            "selection": {
                "tagStatus": "untagged",
                "countType": "imageCountMoreThan",
                "countNumber": 5
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}

data "aws_iam_policy_document" "ecr_policy" {
  statement {
    actions = [ "ecr:GetAuthorizationToken" ]

    resources = [ "*" ]
  }

  statement {
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:GetRepositoryPolicy",
      "ecr:DescribeRepositories",
      "ecr:ListImages",
      "ecr:DescribeImages",
      "ecr:BatchGetImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:PutImage"
    ]

    resources = [ aws_ecr_repository.registry.arn ]
  }
}

resource "aws_iam_policy" "ecr_policy" {
  name        = "ecr-policy"
  path        = "/"
  policy      = data.aws_iam_policy_document.ecr_policy.json
  description = "S3 access policy for ECR accounts - Managed by Terraform"
}

resource "aws_iam_user" "ecr_user" {
  name = "ecr-user"
}

resource "aws_iam_access_key" "ecr_user" {
  user = aws_iam_user.ecr_user.name
}

resource "aws_iam_user_policy_attachment" "ecr_policy" {
  user = aws_iam_user.ecr_user.name
  policy_arn = aws_iam_policy.ecr_policy.arn
}

output "ecr_user" {
  value = aws_iam_user.ecr_user.name
}

output "registry_arn" {
  value = aws_ecr_repository.registry.arn
}
