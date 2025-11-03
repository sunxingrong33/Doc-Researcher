import React, { useState } from 'react';
import MemeEditor from './components/MemeEditor';
import MemeGallery from './components/MemeGallery';
import './styles/App.css';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleMemeCreated = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>😂 Meme Generator</h1>
        <p className="subtitle">Create hilarious memes in seconds!</p>
      </header>

      <main className="app-main">
        <div className="editor-section">
          <MemeEditor onMemeCreated={handleMemeCreated} />
        </div>

        <div className="gallery-section">
          <MemeGallery refreshTrigger={refreshTrigger} />
        </div>
      </main>

      <footer className="app-footer">
        <p>Made with ❤️ using React + TypeScript + Express + MongoDB</p>
      </footer>
    </div>
  );
}

export default App;
