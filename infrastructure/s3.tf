resource "aws_s3_bucket" "pdf_upload_bucket" {
  bucket = "pdf-comment-formatter-uploads-${var.environment}"

  tags = {
    Name        = "PDF Upload Bucket"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_public_access_block" "pdf_upload_bucket" {
  bucket = aws_s3_bucket.pdf_upload_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "pdf_upload_bucket_policy" {
  bucket = aws_s3_bucket.pdf_upload_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { AWS = aws_iam_role.lambda_exec.arn }
        Action    = ["s3:PutObject", "s3:GetObject"]
        Resource  = "${aws_s3_bucket.pdf_upload_bucket.arn}/*"
      }
    ]
  })
}