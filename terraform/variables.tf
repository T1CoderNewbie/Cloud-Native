variable "project_name" {
  description = "Project name prefix."
  type        = string
  default     = "cloud-notes"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
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
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDR blocks."
  type        = list(string)
  default     = ["10.0.0.0/24", "10.0.1.0/24"]
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDR blocks."
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.11.0/24"]
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
