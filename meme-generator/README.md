# 😂 Meme Generator

A full-stack web application for creating and sharing hilarious memes!

## 🎯 Features

- 📸 **Image Upload** - Upload your own images or use popular templates
- ✍️ **Text Customization** - Add top and bottom text with customizable:
  - Font size
  - Text color
  - Outline/stroke color
- 🎨 **Live Preview** - See your meme as you create it
- 💾 **Save to Database** - All memes are stored in MongoDB
- 🖼️ **Gallery View** - Browse all created memes
- ⬇️ **Download** - Download your memes as PNG images
- 🗑️ **Delete** - Remove unwanted memes

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Axios** - HTTP client
- **CSS3** - Styling

### Backend
- **Express.js** - Web framework
- **Node.js** - Runtime environment
- **MongoDB** - Database
- **Mongoose** - ODM
- **Multer** - File upload middleware
- **Canvas** - Image manipulation

## 📦 Installation

### Prerequisites

- Node.js 16+
- npm or yarn
- MongoDB (local or Atlas)

### 1. Clone the repository

```bash
git clone <repository-url>
cd meme-generator
```

### 2. Setup Backend

```bash
cd backend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env with your MongoDB URI
# PORT=5000
# MONGODB_URI=mongodb://localhost:27017/meme-generator

# Start server
npm run dev
```

Backend will run on `http://localhost:5000`

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

## 🚀 Usage

1. **Upload an Image**
   - Click "Upload Image" or drag & drop an image file
   - Supported formats: JPG, PNG, GIF, WebP

2. **Add Text**
   - Enter a title for your meme (required)
   - Add optional top text
   - Add optional bottom text
   - Adjust font size, text color, and outline color

3. **Preview**
   - See a live preview of your meme as you type

4. **Create**
   - Click "Create Meme" button
   - Your meme will be generated and saved

5. **View Gallery**
   - Browse all created memes
   - Download or delete memes

## 📁 Project Structure

```
meme-generator/
├── backend/
│   ├── controllers/
│   │   └── memeController.js      # Meme business logic
│   ├── models/
│   │   └── Meme.js                # MongoDB schema
│   ├── routes/
│   │   └── memeRoutes.js          # API routes
│   ├── middleware/
│   │   └── upload.js              # Multer config
│   ├── uploads/                   # Uploaded images
│   ├── server.js                  # Express server
│   └── package.json
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── MemeEditor.tsx     # Meme creation UI
│   │   │   └── MemeGallery.tsx    # Gallery view
│   │   ├── services/
│   │   │   └── api.ts             # API client
│   │   ├── types/
│   │   │   └── index.ts           # TypeScript types
│   │   ├── styles/
│   │   │   ├── index.css          # Global styles
│   │   │   ├── App.css
│   │   │   ├── MemeEditor.css
│   │   │   └── MemeGallery.css
│   │   ├── App.tsx                # Main component
│   │   └── main.tsx               # Entry point
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── package.json
│
└── README.md
```

## 🔌 API Endpoints

### Memes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/memes` | Get all memes |
| GET | `/api/memes/:id` | Get single meme |
| POST | `/api/memes` | Create new meme |
| POST | `/api/memes/:id/generate` | Generate meme with text |
| PUT | `/api/memes/:id` | Update meme |
| DELETE | `/api/memes/:id` | Delete meme |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |

## 🎨 Customization

### Default Settings

You can modify default meme settings in:
- `backend/models/Meme.js` - Default values
- `frontend/src/components/MemeEditor.tsx` - Initial state

### Styling

All styles are in `frontend/src/styles/`:
- Modify CSS variables in `index.css` for theme colors
- Component-specific styles in respective CSS files

## 📝 Environment Variables

### Backend (.env)

```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/meme-generator
NODE_ENV=development
```

## 🔧 Development

### Backend Development

```bash
cd backend
npm run dev  # Uses nodemon for auto-reload
```

### Frontend Development

```bash
cd frontend
npm run dev  # Uses Vite HMR
```

### Building for Production

#### Frontend

```bash
cd frontend
npm run build
# Output: dist/
```

#### Backend

The backend doesn't need building, just ensure:
- Set `NODE_ENV=production` in .env
- Use `npm start` instead of `npm run dev`

## 🧪 Testing

Currently no tests are implemented. Future improvements:
- Unit tests with Jest
- Integration tests with Supertest
- E2E tests with Playwright

## 🚧 Future Enhancements

- [ ] User authentication
- [ ] Meme templates library
- [ ] Social sharing features
- [ ] Meme categories/tags
- [ ] Search and filter
- [ ] Likes and comments
- [ ] Image filters and effects
- [ ] Stickers and overlays
- [ ] GIF support
- [ ] Mobile app

## 🐛 Troubleshooting

### MongoDB Connection Error

```
Error: connect ECONNREFUSED 127.0.0.1:27017
```

**Solution**: Make sure MongoDB is running:
```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Or use MongoDB Atlas cloud database
```

### CORS Errors

**Solution**: Backend already has CORS enabled. Check if backend is running on port 5000.

### File Upload Fails

**Solution**:
- Check file size (max 10MB)
- Ensure `uploads/` directory exists in backend
- Check file permissions

### Canvas Module Error

```
Error: Cannot find module 'canvas'
```

**Solution**: Install canvas dependencies:

**macOS**:
```bash
brew install pkg-config cairo pango libpng jpeg giflib librsvg
```

**Ubuntu/Debian**:
```bash
sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev
```

## 📄 License

MIT License - feel free to use this project for learning or personal use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👨‍💻 Author

Created with ❤️ for meme lovers everywhere!

## 🙏 Acknowledgments

- Inspired by popular meme generators
- Built with modern web technologies
- Thanks to the open-source community

---

**Happy Meme Making! 😂🎉**
