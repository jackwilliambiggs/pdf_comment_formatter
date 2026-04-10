import PyPDF2

def extract_comments_from_pdf(pdf_path):
    comments = []
    
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        for page in reader.pages:
            if '/Annots' in page:
                annotations = page['/Annots']
                for annotation in annotations:
                    comment = annotation.get_object()
                    if '/Contents' in comment:
                        comments.append(comment['/Contents'])
    
    return comments

def lambda_handler(event, context):
    pdf_path = event['pdf_path']  # Assuming the PDF path is passed in the event
    comments = extract_comments_from_pdf(pdf_path)
    
    return {
        'statusCode': 200,
        'body': {
            'comments': comments
        }
    }