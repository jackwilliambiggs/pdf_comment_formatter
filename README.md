# PDF Comment Formatter

## Overview
The PDF Comment Formatter is a web application that allows users to upload PDF files containing comments and extract those comments for viewing. The application is built using React for the front end and AWS Lambda for the backend processing.

## Project Structure
The project is organized into three main directories:

- **frontend**: Contains the React application for user interaction.
- **backend**: Contains AWS Lambda functions for handling PDF uploads and comment extraction.
- **infrastructure**: Contains Terraform scripts for deploying the application infrastructure on AWS.

## Frontend
The frontend is built with React and TypeScript. It includes the following key components:

- **FileUpload**: A component for uploading PDF files.
- **CommentList**: A component for displaying extracted comments.
- **Header**: A component for the application header.

### Setup
1. Navigate to the `frontend` directory.
2. Install dependencies using npm:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```

## Backend
The backend consists of two main Lambda functions:

- **upload_pdf**: Handles the uploading of PDF files to an S3 bucket.
- **extract_comments**: Extracts comments from the uploaded PDF files.

### Setup
1. Navigate to the `backend` directory.
2. Install dependencies for each Lambda function:
   ```
   cd lambdas/extract_comments
   pip install -r requirements.txt
   cd ../upload_pdf
   pip install -r requirements.txt
   ```
3. Deploy the backend using AWS SAM:
   ```
   sam build
   sam deploy --guided
   ```

## Infrastructure
The infrastructure is defined using Terraform. It includes resources for S3, Lambda functions, and API Gateway. Terraform state is stored remotely in S3 with DynamoDB locking.

### AWS Setup (First Time)

1. **Configure the AWS CLI** with your personal account credentials:
   ```bash
   aws configure
   ```
   You'll need your **Access Key ID** and **Secret Access Key** from the AWS Console → IAM → Users → Security credentials.

2. **Create the Terraform state backend resources**:
   ```bash
   aws s3api create-bucket \
     --bucket pdf-comment-formatter-tfstate \
     --region eu-west-2 \
     --create-bucket-configuration LocationConstraint=eu-west-2

   aws s3api put-bucket-versioning \
     --bucket pdf-comment-formatter-tfstate \
     --versioning-configuration Status=Enabled

   aws dynamodb create-table \
     --table-name pdf-comment-formatter-tflock \
     --attribute-definitions AttributeName=LockID,AttributeType=S \
     --key-schema AttributeName=LockID,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST \
     --region eu-west-2
   ```

3. **Set up GitHub Actions secrets** for CI/CD. In your GitHub repo go to **Settings → Secrets and variables → Actions** and add:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### Deploy Locally
1. Navigate to the `infrastructure` directory.
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Preview the changes:
   ```bash
   terraform plan
   ```
4. Apply the Terraform configuration:
   ```bash
   terraform apply
   ```

### Deploy via CI/CD
Pushes to `main` automatically trigger the GitHub Actions pipeline which:
1. Packages the Lambda functions
2. Runs `terraform plan`
3. Applies changes (gated behind a `production` environment approval)

## Usage
1. Open the application in your web browser.
2. Use the upload feature to select and upload a PDF file.
3. View the extracted comments displayed on the page.

## Progress

### Done
- Project restructured into `frontend/`, `backend/`, `infrastructure/` directories (branch: `web_app`)
- Terraform infrastructure defined: S3 bucket, Lambda functions, API Gateway, IAM roles
- Remote Terraform state configured (S3 + DynamoDB locking)
- GitHub Actions CI/CD pipeline created (build Lambdas → plan → apply)
- S3 bucket policy locked down (no public access, scoped to Lambda role only)
- Lambda runtime updated to Python 3.12
- Deployment instructions added to README

### Next Steps
- [ ] Install Node.js (requested for work laptop) — needed to run/build the React frontend
- [ ] Add S3 + CloudFront Terraform config for publicly hosting the frontend
- [ ] Update CI pipeline to build and deploy the React app
- [ ] Configure AWS CLI and create Terraform state backend resources
- [ ] Run first `terraform plan` / `terraform apply` locally to validate
- [ ] Wire up the frontend API service to the deployed API Gateway endpoint
- [ ] Implement the Lambda function logic (upload to S3, extract comments from PDF)

## License
This project is licensed under the MIT License. See the LICENSE file for more details.