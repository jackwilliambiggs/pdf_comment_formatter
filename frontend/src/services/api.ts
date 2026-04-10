import axios from 'axios';

const API_BASE_URL = 'https://your-api-gateway-url.amazonaws.com/prod'; // Replace with your actual API Gateway URL

export const uploadPdf = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error uploading PDF:', error);
        throw error;
    }
};

export const extractComments = async (pdfId: string) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/extract_comments/${pdfId}`);
        return response.data;
    } catch (error) {
        console.error('Error extracting comments:', error);
        throw error;
    }
};