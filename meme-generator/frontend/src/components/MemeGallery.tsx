import React, { useEffect, useState } from 'react';
import { memeAPI } from '../services/api';
import { Meme } from '../types';
import '../styles/MemeGallery.css';

interface MemeGalleryProps {
  refreshTrigger: number;
}

const MemeGallery: React.FC<MemeGalleryProps> = ({ refreshTrigger }) => {
  const [memes, setMemes] = useState<Meme[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadMemes();
  }, [refreshTrigger]);

  const loadMemes = async () => {
    try {
      setIsLoading(true);
      setError('');
      const data = await memeAPI.getAllMemes();
      setMemes(data);
    } catch (err) {
      console.error('Error loading memes:', err);
      setError('Failed to load memes');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this meme?')) {
      return;
    }

    try {
      await memeAPI.deleteMeme(id);
      setMemes(memes.filter(meme => meme._id !== id));
    } catch (err) {
      console.error('Error deleting meme:', err);
      alert('Failed to delete meme');
    }
  };

  const handleDownload = (meme: Meme) => {
    const imageUrl = meme.generatedImageUrl || meme.imageUrl;
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `${meme.title}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (isLoading) {
    return (
      <div className="meme-gallery">
        <h2>🖼️ Meme Gallery</h2>
        <div className="loading">Loading memes...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="meme-gallery">
        <h2>🖼️ Meme Gallery</h2>
        <div className="error">{error}</div>
      </div>
    );
  }

  if (memes.length === 0) {
    return (
      <div className="meme-gallery">
        <h2>🖼️ Meme Gallery</h2>
        <div className="empty-state">
          <p>No memes yet!</p>
          <p className="hint">Create your first meme above 👆</p>
        </div>
      </div>
    );
  }

  return (
    <div className="meme-gallery">
      <h2>🖼️ Meme Gallery ({memes.length})</h2>

      <div className="memes-grid">
        {memes.map((meme) => (
          <div key={meme._id} className="meme-card">
            <div className="meme-image-container">
              <img
                src={meme.generatedImageUrl || meme.imageUrl}
                alt={meme.title}
                className="meme-image"
              />
            </div>

            <div className="meme-info">
              <h3 className="meme-title">{meme.title}</h3>

              {(meme.topText || meme.bottomText) && (
                <div className="meme-texts">
                  {meme.topText && (
                    <p className="meme-text">
                      <strong>Top:</strong> {meme.topText}
                    </p>
                  )}
                  {meme.bottomText && (
                    <p className="meme-text">
                      <strong>Bottom:</strong> {meme.bottomText}
                    </p>
                  )}
                </div>
              )}

              <p className="meme-date">
                {new Date(meme.createdAt).toLocaleDateString()}
              </p>

              <div className="meme-actions">
                <button
                  className="action-btn download-btn"
                  onClick={() => handleDownload(meme)}
                  title="Download"
                >
                  ⬇️ Download
                </button>
                <button
                  className="action-btn delete-btn"
                  onClick={() => handleDelete(meme._id)}
                  title="Delete"
                >
                  🗑️ Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MemeGallery;
