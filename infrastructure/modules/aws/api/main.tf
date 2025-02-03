variable "environment" {
  description = "Which environment (dev / prod / staging)"
}

variable "ec2_instance_type" {
  description = "Instance type"
}

variable "public_ssh_key" {
  description = "Publich RSA key used for SSH access to server"
}

variable "ami" {
  description = "AMI image to start with - see https://cloud-images.ubuntu.com/locator/ec2/"
}

resource "aws_key_pair" "app" {
  key_name_prefix = "${var.environment}-app-"
  public_key      = var.public_ssh_key
}

resource "aws_instance" "app" {
  ami                    = var.ami
  instance_type          = var.ec2_instance_type
  key_name               = aws_key_pair.app.key_name
  vpc_security_group_ids = [aws_security_group.app.id]

  root_block_device {
    volume_size = 20
  }

  tags = {
    Name        = "${var.environment} application server"
    Environment = var.environment
  }
}

resource "aws_security_group" "app" {
  name = "${var.environment}-app"

  tags = {
    Name        = "${var.environment}-app-sg"
    Environment = var.environment
  }

  # SSH
  ingress {
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  # HTTP
  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  # HTTPS
  ingress {
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
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

resource "aws_eip" "ip" {
  instance = aws_instance.app.id

  tags = {
    Name        = "${var.environment}-ip"
    Environment = var.environment
  }
}

output "ip" {
  value = aws_eip.ip.public_ip
}

output "app_sg" {
  value = aws_security_group.app.id
}
