output "eks_cluster_name" {
  description = "EKS cluster name."
  value       = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint."
  value       = module.eks.cluster_endpoint
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint."
  value       = aws_db_instance.postgres.address
}

output "redis_primary_endpoint" {
  description = "ElastiCache Redis primary endpoint."
  value       = aws_elasticache_replication_group.redis.primary_endpoint_address
}

output "s3_bucket_name" {
  description = "S3 bucket name used by the upload endpoint."
  value       = aws_s3_bucket.uploads.bucket
}

output "route53_record_fqdn" {
  description = "Optional Route 53 record FQDN."
  value       = try(aws_route53_record.cloud_notes[0].fqdn, "")
}

output "deployment_summary" {
  description = "Quick summary values to help wire the application into EKS."
  value = {
    environment          = var.environment
    aws_region           = var.aws_region
    kubernetes_namespace = "cloud-notes"
    eks_cluster_name     = module.eks.cluster_name
    rds_endpoint         = aws_db_instance.postgres.address
    redis_endpoint       = aws_elasticache_replication_group.redis.primary_endpoint_address
    s3_bucket_name       = aws_s3_bucket.uploads.bucket
  }
}
