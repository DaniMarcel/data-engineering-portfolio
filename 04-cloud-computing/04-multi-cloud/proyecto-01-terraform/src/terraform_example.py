"""Terraform Infrastructure as Code Example"""

# main.tf equivalent in documentation format

terraform_config = """
# AWS S3 Bucket
resource "aws_s3_bucket" "data_lake" {
  bucket = "my-data-lake-${var.environment}"
  
  tags = {
    Name        = "Data Lake"
    Environment = var.environment
  }
}

# AWS Lambda Function
resource "aws_lambda_function" "etl_processor" {
  filename      = "lambda.zip"
  function_name = "etl-processor-${var.environment}"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
}

# GCP BigQuery Dataset
resource "google_bigquery_dataset" "analytics" {
  dataset_id = "analytics_${var.environment}"
  location   = "US"
}

# Variables
variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "dev"
}
"""

# Python script to demonstrate Terraform concepts
print("🏗️  TERRAFORM INFRASTRUCTURE AS CODE\n")
print("This example shows multi-cloud IaC configuration\n")
print(terraform_config)

print("\n📝 Terraform Commands:")
print("  terraform init    - Initialize")
print("  terraform plan    - Preview changes")
print("  terraform apply   - Apply changes")
print("  terraform destroy - Destroy infrastructure")

print("\n✅ Multi-cloud infrastructure defined!")
print("\nProviders: AWS, GCP, Azure")
