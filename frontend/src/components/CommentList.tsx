import React from 'react';

interface CommentListProps {
    comments: string[];
}

const CommentList: React.FC<CommentListProps> = ({ comments }) => {
    return (
        <div>
            <h2>Extracted Comments</h2>
            <ul>
                {comments.map((comment, index) => (
                    <li key={index}>{comment}</li>
                ))}
            </ul>
        </div>
    );
};

export default CommentList;