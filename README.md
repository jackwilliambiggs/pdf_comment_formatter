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
The infrastructure is defined using Terraform. It includes resources for S3, Lambda functions, and API Gateway.

### Setup
1. Navigate to the `infrastructure` directory.
2. Initialize Terraform:
   ```
   terraform init
   ```
3. Apply the Terraform configuration:
   ```
   terraform apply
   ```

## Usage
1. Open the application in your web browser.
2. Use the upload feature to select and upload a PDF file.
3. View the extracted comments displayed on the page.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.