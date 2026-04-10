resource "aws_api_gateway_rest_api" "pdf_formatter_api" {
  name        = "PDFFormatterAPI"
  description = "API for uploading PDFs and extracting comments"
}

resource "aws_api_gateway_resource" "upload_pdf" {
  rest_api_id = aws_api_gateway_rest_api.pdf_formatter_api.id
  parent_id   = aws_api_gateway_rest_api.pdf_formatter_api.root_resource_id
  path_part   = "upload"
}

resource "aws_api_gateway_resource" "extract_comments" {
  rest_api_id = aws_api_gateway_rest_api.pdf_formatter_api.id
  parent_id   = aws_api_gateway_resource.upload_pdf.id
  path_part   = "comments"
}

resource "aws_api_gateway_method" "upload_pdf_method" {
  rest_api_id   = aws_api_gateway_rest_api.pdf_formatter_api.id
  resource_id   = aws_api_gateway_resource.upload_pdf.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "extract_comments_method" {
  rest_api_id   = aws_api_gateway_rest_api.pdf_formatter_api.id
  resource_id   = aws_api_gateway_resource.extract_comments.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "upload_pdf_integration" {
  rest_api_id             = aws_api_gateway_rest_api.pdf_formatter_api.id
  resource_id             = aws_api_gateway_resource.upload_pdf.id
  http_method             = aws_api_gateway_method.upload_pdf_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.upload_pdf.invoke_arn
}

resource "aws_api_gateway_integration" "extract_comments_integration" {
  rest_api_id             = aws_api_gateway_rest_api.pdf_formatter_api.id
  resource_id             = aws_api_gateway_resource.extract_comments.id
  http_method             = aws_api_gateway_method.extract_comments_method.http_method
  integration_http_method = "GET"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.extract_comments.invoke_arn
}

resource "aws_api_gateway_deployment" "pdf_formatter_deployment" {
  rest_api_id = aws_api_gateway_rest_api.pdf_formatter_api.id
  stage_name  = "prod"
}