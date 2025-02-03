variable "environment" {
  description = "Which environment (dev / prod / staging)"
}

variable "project" {
  description = "Project name"
}

resource "aws_s3_bucket" "media" {
  bucket = "${var.project}-${var.environment}-media"

  tags = {
    Name        = "${var.environment} media storage"
    Environment = var.environment
  }
}

data "aws_iam_policy_document" "s3" {
  statement {
    actions = [
      "s3:ListBucket",
      "s3:GetBucketLocation",
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.media.id}",
    ]
  }

  statement {
    actions = [
      "s3:PutObject",
      "s3:PutObjectAcl",
      "s3:GetObject",
      "s3:GetObjectAcl",
      "s3:DeleteObject",
    ]

    resources = [
      "arn:aws:s3:::${aws_s3_bucket.media.id}/*",
    ]
  }
}

resource "aws_iam_policy" "s3" {
  name        = "${var.environment}-s3-policy"
  path        = "/"
  policy      = data.aws_iam_policy_document.s3.json
  description = "S3 access policy for ${var.project}-${var.environment} - Managed by Terraform"
}

resource "aws_iam_user" "s3" {
  name = "${var.environment}-s3-user"
}

resource "aws_iam_user_policy_attachment" "s3" {
  user       = aws_iam_user.s3.name
  policy_arn = aws_iam_policy.s3.arn
}

resource "aws_iam_access_key" "s3" {
  user = aws_iam_user.s3.name
}

output "s3_region" {
  value = aws_s3_bucket.media.region
}

output "s3_media_bucket_name" {
  value = aws_s3_bucket.media.bucket
}

output "s3_id" {
  value = aws_iam_access_key.s3.id
}

output "s3_secret" {
  value = aws_iam_access_key.s3.secret
}
