import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import CommentList from './components/CommentList';
import Header from './components/Header';
import './styles/App.css';

const App: React.FC = () => {
    const [comments, setComments] = useState<string[]>([]);

    const handleCommentsUpdate = (newComments: string[]) => {
        setComments(newComments);
    };

    return (
        <div className="App">
            <Header />
            <FileUpload onCommentsUpdate={handleCommentsUpdate} />
            <CommentList comments={comments} />
        </div>
    );
};

export default App;