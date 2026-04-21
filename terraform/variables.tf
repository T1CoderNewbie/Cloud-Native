variable "project_name" {
  description = "Project name prefix."
  type        = string
  default     = "cloud-notes"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be one of: dev, staging, prod."
  }
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "ap-southeast-1"
}

variable "cluster_name" {
  description = "EKS cluster name."
  type        = string
  default     = "cloud-notes-eks"
}

variable "kubernetes_version" {
  description = "EKS Kubernetes version."
  type        = string
  default     = "1.30"

  validation {
    condition     = can(regex("^[0-9]+\\.[0-9]+$", var.kubernetes_version))
    error_message = "kubernetes_version must use the major.minor format, for example 1.30."
  }
}

variable "vpc_cidr" {
  description = "VPC CIDR."
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones used by the VPC."
  type        = list(string)
  default     = ["ap-southeast-1a", "ap-southeast-1b"]

  validation {
    condition     = length(var.availability_zones) >= 2
    error_message = "availability_zones must contain at least two AZs for a resilient EKS deployment."
  }
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDR blocks."
  type        = list(string)
  default     = ["10.0.0.0/24", "10.0.1.0/24"]

  validation {
    condition     = length(var.public_subnet_cidrs) >= 2
    error_message = "public_subnet_cidrs must contain at least two subnet CIDRs."
  }
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDR blocks."
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]

  validation {
    condition     = length(var.private_subnet_cidrs) >= 2
    error_message = "private_subnet_cidrs must contain at least two subnet CIDRs."
  }
}

variable "node_instance_type" {
  description = "EC2 instance type for EKS managed node group."
  type        = string
  default     = "t3.medium"
}

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "cloudnotes"
}

variable "db_username" {
  description = "PostgreSQL username."
  type        = string
  default     = "cloudnotes"
}

variable "db_password" {
  description = "PostgreSQL password."
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.db_password) >= 12 && var.db_password != "replace-me"
    error_message = "db_password must be at least 12 characters and should not use the placeholder value."
  }
}

variable "db_instance_class" {
  description = "RDS instance class."
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Initial RDS storage in GB."
  type        = number
  default     = 20
}

variable "redis_node_type" {
  description = "ElastiCache Redis node type."
  type        = string
  default     = "cache.t4g.micro"
}

variable "route53_zone_id" {
  description = "Optional Route 53 hosted zone ID."
  type        = string
  default     = ""

  validation {
    condition     = var.route53_zone_id == "" || can(regex("^Z[A-Z0-9]+$", var.route53_zone_id))
    error_message = "route53_zone_id must be blank or look like an AWS hosted zone ID starting with Z."
  }
}

variable "route53_record_name" {
  description = "Optional Route 53 record name."
  type        = string
  default     = ""
}

variable "load_balancer_dns_name" {
  description = "Istio ingress load balancer DNS name after deployment."
  type        = string
  default     = ""
}

variable "load_balancer_zone_id" {
  description = "Hosted zone ID of the AWS load balancer."
  type        = string
  default     = ""
}
