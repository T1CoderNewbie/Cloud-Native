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

output "route53_record_fqdn" {
  description = "Optional Route 53 record FQDN."
  value       = try(aws_route53_record.cloud_notes[0].fqdn, "")
}
