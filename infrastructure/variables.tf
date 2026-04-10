variable "aws_region" {
  description = "The AWS region where the resources will be deployed"
  type        = string
  default     = "eu-west-2"
}

variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "api_gateway_stage" {
  description = "The stage name for the API Gateway"
  type        = string
  default     = "dev"
}