import React, { useState } from 'react';
import { memeAPI } from '../services/api';
import { CreateMemeData } from '../types';
import '../styles/MemeEditor.css';

interface MemeEditorProps {
  onMemeCreated: () => void;
}

const MemeEditor: React.FC<MemeEditorProps> = ({ onMemeCreated }) => {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [title, setTitle] = useState('');
  const [topText, setTopText] = useState('');
  const [bottomText, setBottomText] = useState('');
  const [fontSize, setFontSize] = useState(48);
  const [textColor, setTextColor] = useState('#FFFFFF');
  const [strokeColor, setStrokeColor] = useState('#000000');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedImage(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedImage) {
      setMessage('Please select an image');
      return;
    }

    if (!title.trim()) {
      setMessage('Please enter a title');
      return;
    }

    setIsLoading(true);
    setMessage('');

    try {
      const memeData: CreateMemeData = {
        title,
        topText,
        bottomText,
        fontSize,
        textColor,
        strokeColor,
        image: selectedImage
      };

      const meme = await memeAPI.createMeme(memeData);

      // Generate the meme with text
      await memeAPI.generateMeme(meme._id);

      setMessage('Meme created successfully!');

      // Reset form
      setSelectedImage(null);
      setPreviewUrl('');
      setTitle('');
      setTopText('');
      setBottomText('');
      setFontSize(48);
      setTextColor('#FFFFFF');
      setStrokeColor('#000000');

      // Notify parent
      onMemeCreated();

      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      console.error('Error creating meme:', error);
      setMessage('Error creating meme. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="meme-editor">
      <h2>🎨 Create Meme</h2>

      <form onSubmit={handleSubmit} className="editor-form">
        {/* Image Upload */}
        <div className="form-group">
          <label htmlFor="image">Upload Image</label>
          <input
            type="file"
            id="image"
            accept="image/*"
            onChange={handleImageSelect}
            disabled={isLoading}
          />
        </div>

        {/* Image Preview */}
        {previewUrl && (
          <div className="image-preview">
            <img src={previewUrl} alt="Preview" />
            {topText && (
              <div
                className="preview-text preview-text-top"
                style={{
                  fontSize: `${fontSize * 0.5}px`,
                  color: textColor,
                  WebkitTextStroke: `${fontSize * 0.01}px ${strokeColor}`
                }}
              >
                {topText.toUpperCase()}
              </div>
            )}
            {bottomText && (
              <div
                className="preview-text preview-text-bottom"
                style={{
                  fontSize: `${fontSize * 0.5}px`,
                  color: textColor,
                  WebkitTextStroke: `${fontSize * 0.01}px ${strokeColor}`
                }}
              >
                {bottomText.toUpperCase()}
              </div>
            )}
          </div>
        )}

        {/* Title */}
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter meme title"
            disabled={isLoading}
            required
          />
        </div>

        {/* Top Text */}
        <div className="form-group">
          <label htmlFor="topText">Top Text</label>
          <input
            type="text"
            id="topText"
            value={topText}
            onChange={(e) => setTopText(e.target.value)}
            placeholder="Enter top text"
            disabled={isLoading}
          />
        </div>

        {/* Bottom Text */}
        <div className="form-group">
          <label htmlFor="bottomText">Bottom Text</label>
          <input
            type="text"
            id="bottomText"
            value={bottomText}
            onChange={(e) => setBottomText(e.target.value)}
            placeholder="Enter bottom text"
            disabled={isLoading}
          />
        </div>

        {/* Font Size */}
        <div className="form-group">
          <label htmlFor="fontSize">Font Size: {fontSize}px</label>
          <input
            type="range"
            id="fontSize"
            min="24"
            max="96"
            value={fontSize}
            onChange={(e) => setFontSize(Number(e.target.value))}
            disabled={isLoading}
          />
        </div>

        {/* Text Color */}
        <div className="form-group color-group">
          <div>
            <label htmlFor="textColor">Text Color</label>
            <input
              type="color"
              id="textColor"
              value={textColor}
              onChange={(e) => setTextColor(e.target.value)}
              disabled={isLoading}
            />
          </div>

          {/* Stroke Color */}
          <div>
            <label htmlFor="strokeColor">Outline Color</label>
            <input
              type="color"
              id="strokeColor"
              value={strokeColor}
              onChange={(e) => setStrokeColor(e.target.value)}
              disabled={isLoading}
            />
          </div>
        </div>

        {/* Message */}
        {message && (
          <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
            {message}
          </div>
        )}

        {/* Submit Button */}
        <button type="submit" disabled={isLoading} className="submit-button">
          {isLoading ? '🔄 Creating...' : '🚀 Create Meme'}
        </button>
      </form>
    </div>
  );
};

export default MemeEditor;
