resource "aws_lambda_function" "extract_comments" {
  function_name    = "extract_comments"
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  role             = aws_iam_role.lambda_exec.arn
  filename         = "${path.module}/../build/extract_comments.zip"
  source_code_hash = filebase64sha256("${path.module}/../build/extract_comments.zip")
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.pdf_upload_bucket.bucket
    }
  }
}

resource "aws_lambda_function" "upload_pdf" {
  function_name    = "upload_pdf"
  handler          = "handler.lambda_handler"
  runtime          = "python3.12"
  role             = aws_iam_role.lambda_exec.arn
  filename         = "${path.module}/../build/upload_pdf.zip"
  source_code_hash = filebase64sha256("${path.module}/../build/upload_pdf.zip")
  timeout          = 30
  memory_size      = 128

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.pdf_upload_bucket.bucket
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Effect = "Allow"
        Sid    = ""
      },
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_policy" {
  name       = "lambda_policy_attachment"
  roles      = [aws_iam_role.lambda_exec.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy_attachment" "s3_policy" {
  name       = "s3_policy_attachment"
  roles      = [aws_iam_role.lambda_exec.name]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}