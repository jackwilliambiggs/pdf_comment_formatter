export interface Comment {
    id: string;
    text: string;
    pageNumber: number;
}

export interface UploadedFile {
    name: string;
    size: number;
    type: string;
}