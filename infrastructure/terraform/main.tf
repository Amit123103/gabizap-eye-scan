provider "aws" {
  region = "us-east-1"
  alias  = "us"
}

provider "aws" {
  region = "eu-west-1"
  alias  = "eu"
}

# ---------------------------------------------------------------------------
# GLOBAL TRAFFIC MANAGER (Route53)
# ---------------------------------------------------------------------------
resource "aws_route53_health_check" "primary" {
  fqdn              = "api.gabizap.com"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = "3"
  request_interval  = "30"
}

# ---------------------------------------------------------------------------
# US REGION (Primary)
# ---------------------------------------------------------------------------
module "vpc_us" {
  source = "terraform-aws-modules/vpc/aws"
  providers = { aws = aws.us }
  
  name = "gabizap-vpc-us"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

module "eks_us" {
  source = "terraform-aws-modules/eks/aws"
  providers = { aws = aws.us }
  
  cluster_name    = "gabizap-cluster-us"
  cluster_version = "1.27"
  vpc_id          = module.vpc_us.vpc_id
  subnet_ids      = module.vpc_us.private_subnets
  
  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 1
      max_size     = 10
      instance_types = ["t3.medium"]
    }
    gpu_nodes = {
      desired_size = 1
      min_size     = 0
      max_size     = 5
      instance_types = ["g4dn.xlarge"] # For Iris/Hand processing
      labels = {
        role = "ai-inference"
      }
    }
  }
}

# ---------------------------------------------------------------------------
# EU REGION (Failover / Active)
# ---------------------------------------------------------------------------
module "vpc_eu" {
  source = "terraform-aws-modules/vpc/aws"
  providers = { aws = aws.eu }
  name = "gabizap-vpc-eu"
  cidr = "10.1.0.0/16" # Different CIDR
  # ... subnets setup similar to US
}

module "eks_eu" {
  source = "terraform-aws-modules/eks/aws"
  providers = { aws = aws.eu }
  cluster_name = "gabizap-cluster-eu"
  # ... configuration similar to US
}

# ---------------------------------------------------------------------------
# DATA REPLICATION (RDS Global Database)
# ---------------------------------------------------------------------------
resource "aws_rds_global_cluster" "gabizap_global" {
  global_cluster_identifier = "gabizap-global-db"
  engine                    = "aurora-postgresql"
  engine_version            = "14.5"
  database_name             = "gabizap_db"
}
