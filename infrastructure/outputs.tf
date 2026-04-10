output "s3_bucket_name" {
  value = aws_s3_bucket.pdf_upload_bucket.bucket
}

output "extract_comments_lambda_function" {
  value = aws_lambda_function.extract_comments.arn
}

output "upload_pdf_lambda_function" {
  value = aws_lambda_function.upload_pdf.arn
}

output "api_gateway_endpoint" {
  value = aws_api_gateway_deployment.pdf_formatter_deployment.invoke_url
}