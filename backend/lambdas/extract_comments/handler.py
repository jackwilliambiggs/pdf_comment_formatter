def lambda_handler(event, context):
    import json
    from pdf_parser import extract_comments_from_pdf

    # Get the PDF file from the event
    pdf_file = event['pdf_file']  # Assuming the PDF file is passed in the event

    # Extract comments from the PDF
    comments = extract_comments_from_pdf(pdf_file)

    # Return the comments as a JSON response
    return {
        'statusCode': 200,
        'body': json.dumps(comments)
    }