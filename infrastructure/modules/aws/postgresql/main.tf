variable "project" {
  description = "Project name"
}

variable "environment" {
  description = "Which environment (dev / prod / staging)"
}

variable "db_password" {
  description = "Password for database"
}

variable "instance_class" {
  description = "Instance class for the database"
}

variable "app_security_group" {
  description = "Security group of the app server (for ingress to DB)"
}

resource "aws_db_instance" "db" {
  engine                    = "postgres"
  allocated_storage         = 20
  storage_type              = "gp2"
  instance_class            = var.instance_class
  vpc_security_group_ids    = [aws_security_group.db.id]
  identifier_prefix         = "${var.environment}-"
  db_name                   = var.project
  username                  = var.project
  password                  = var.db_password
  final_snapshot_identifier = "${var.environment}-db-final-snapshot"
  backup_retention_period   = 20
  backup_window             = "04:00-05:00"
  maintenance_window        = "Mon:00:00-Mon:03:00"

  tags = {
    Name        = "${var.environment}-db"
    Environment = var.environment
  }
}

resource "aws_security_group" "db" {
  name = "${var.environment}-db"

  tags = {
    Name        = "${var.environment}-db-sg"
    Environment = var.environment
  }

  # PostgreSQL port from app server
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "TCP"
    security_groups = [var.app_security_group]
  }

  # Outbound internet access
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

output "db_address" {
  value = aws_db_instance.db.address
}

output "db_port" {
  value = aws_db_instance.db.port
}

output "db_arn" {
  value = aws_db_instance.db.arn
}
