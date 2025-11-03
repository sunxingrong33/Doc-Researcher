# 🚀 Quick Start Guide

Get your Meme Generator up and running in minutes!

## Prerequisites

1. **Node.js** (v16 or higher)
   ```bash
   node --version
   ```

2. **MongoDB** (local installation or MongoDB Atlas)
   - Local: https://www.mongodb.com/try/download/community
   - Cloud: https://www.mongodb.com/cloud/atlas

3. **npm** or **yarn**
   ```bash
   npm --version
   ```

## Installation

### Option 1: Automatic Setup (Recommended)

```bash
# Run the setup script
./start.sh

# Then start backend (Terminal 1)
cd backend
npm run dev

# Then start frontend (Terminal 2)
cd frontend
npm run dev
```

### Option 2: Manual Setup

#### Step 1: Install Dependencies

```bash
# Install root dependencies (for concurrent running)
npm install

# Or install separately
npm run install-all
```

#### Step 2: Configure Backend

```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/meme-generator
NODE_ENV=development
```

#### Step 3: Start Development Servers

**Option A: Run both together**
```bash
# From root directory
npm run dev
```

**Option B: Run separately**

Terminal 1 (Backend):
```bash
cd backend
npm run dev
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

## Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/api/health

## First Steps

1. **Upload an Image**
   - Click the upload area or drag & drop an image
   - Supported: JPG, PNG, GIF, WebP (max 10MB)

2. **Create Your First Meme**
   - Enter a title
   - Add top/bottom text (optional)
   - Customize colors and font size
   - Click "Create Meme"

3. **View Gallery**
   - See all your created memes
   - Download or delete memes

## Common Issues

### MongoDB Not Running

```bash
# macOS
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Windows
net start MongoDB
```

### Port Already in Use

If port 3000 or 5000 is occupied:

**Backend**: Change PORT in `backend/.env`
**Frontend**: Change port in `frontend/vite.config.ts`

### Canvas Installation Issues

**macOS**:
```bash
brew install pkg-config cairo pango libpng jpeg giflib librsvg
cd backend
npm install
```

**Linux**:
```bash
sudo apt-get install build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev
cd backend
npm install
```

## Testing the API

```bash
# Health check
curl http://localhost:5000/api/health

# Get all memes
curl http://localhost:5000/api/memes
```

## Project Structure

```
meme-generator/
├── backend/          # Express API
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── middleware/
│   └── uploads/
│
├── frontend/         # React App
│   └── src/
│       ├── components/
│       ├── services/
│       ├── types/
│       └── styles/
│
└── README.md
```

## Development Tips

- **Hot Reload**: Both servers support hot reload
- **API Proxy**: Frontend proxies `/api` to backend
- **TypeScript**: Frontend uses TypeScript for type safety
- **ES6+**: Backend uses modern JavaScript

## Next Steps

- Read the full [README.md](./README.md)
- Explore the API endpoints
- Customize the styling
- Add new features

## Need Help?

- Check the [README.md](./README.md) for detailed documentation
- Review the troubleshooting section
- Inspect browser console for frontend errors
- Check backend terminal for API errors

---

**Happy Meme Making! 😂**
