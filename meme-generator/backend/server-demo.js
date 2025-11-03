/**
 * Meme Generator Demo Server
 * 演示版本 - 不需要 MongoDB 和 Canvas
 * 使用内存存储数据
 */

const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 5000;

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 静态文件服务
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// 确保uploads目录存在
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// 内存数据存储
let memesDB = [];
let idCounter = 1;

// 配置文件上传
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadsDir);
  },
  filename: function (req, file, cb) {
    const uniqueName = `${uuidv4()}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  }
});

const fileFilter = (req, file, cb) => {
  const allowedTypes = /jpeg|jpg|png|gif|webp/;
  const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
  const mimetype = allowedTypes.test(file.mimetype);

  if (extname && mimetype) {
    cb(null, true);
  } else {
    cb(new Error('Only image files are allowed!'), false);
  }
};

const upload = multer({
  storage: storage,
  limits: { fileSize: 10 * 1024 * 1024 },
  fileFilter: fileFilter
});

// ===== API 路由 =====

// 健康检查
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Meme Generator Demo API',
    mode: 'demo (in-memory storage)',
    timestamp: new Date().toISOString(),
    totalMemes: memesDB.length
  });
});

// 获取所有 memes
app.get('/api/memes', (req, res) => {
  res.json(memesDB.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt)));
});

// 获取单个 meme
app.get('/api/memes/:id', (req, res) => {
  const meme = memesDB.find(m => m._id === req.params.id);
  if (!meme) {
    return res.status(404).json({ message: 'Meme not found' });
  }
  res.json(meme);
});

// 创建新 meme
app.post('/api/memes', upload.single('image'), (req, res) => {
  try {
    const { title, topText, bottomText, fontSize, textColor, strokeColor } = req.body;

    if (!req.file) {
      return res.status(400).json({ message: 'Image file is required' });
    }

    const imageUrl = `/uploads/${req.file.filename}`;

    const newMeme = {
      _id: `meme_${idCounter++}`,
      title: title || 'Untitled Meme',
      imageUrl,
      topText: topText || '',
      bottomText: bottomText || '',
      fontSize: parseInt(fontSize) || 48,
      textColor: textColor || '#FFFFFF',
      strokeColor: strokeColor || '#000000',
      generatedImageUrl: null,
      createdAt: new Date().toISOString()
    };

    memesDB.push(newMeme);
    res.status(201).json(newMeme);
  } catch (error) {
    res.status(500).json({ message: 'Error creating meme', error: error.message });
  }
});

// 生成 meme (演示版 - 只返回原图，说明文字信息)
app.post('/api/memes/:id/generate', (req, res) => {
  try {
    const meme = memesDB.find(m => m._id === req.params.id);

    if (!meme) {
      return res.status(404).json({ message: 'Meme not found' });
    }

    // 演示模式：直接使用原图作为生成的图
    // 实际应用中会使用Canvas API在服务器端生成带文字的图片
    meme.generatedImageUrl = meme.imageUrl;

    console.log(`[DEMO] Generated meme: ${meme.title}`);
    console.log(`  Top Text: "${meme.topText}"`);
    console.log(`  Bottom Text: "${meme.bottomText}"`);
    console.log(`  Font Size: ${meme.fontSize}px`);
    console.log(`  Colors: ${meme.textColor} / ${meme.strokeColor}`);

    res.json(meme);
  } catch (error) {
    res.status(500).json({ message: 'Error generating meme', error: error.message });
  }
});

// 更新 meme
app.put('/api/memes/:id', (req, res) => {
  try {
    const memeIndex = memesDB.findIndex(m => m._id === req.params.id);

    if (memeIndex === -1) {
      return res.status(404).json({ message: 'Meme not found' });
    }

    memesDB[memeIndex] = {
      ...memesDB[memeIndex],
      ...req.body,
      _id: req.params.id
    };

    res.json(memesDB[memeIndex]);
  } catch (error) {
    res.status(500).json({ message: 'Error updating meme', error: error.message });
  }
});

// 删除 meme
app.delete('/api/memes/:id', (req, res) => {
  try {
    const memeIndex = memesDB.findIndex(m => m._id === req.params.id);

    if (memeIndex === -1) {
      return res.status(404).json({ message: 'Meme not found' });
    }

    const meme = memesDB[memeIndex];

    // 删除文件
    if (meme.imageUrl) {
      const imagePath = path.join(__dirname, meme.imageUrl);
      if (fs.existsSync(imagePath)) {
        fs.unlinkSync(imagePath);
      }
    }

    memesDB.splice(memeIndex, 1);
    res.json({ message: 'Meme deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Error deleting meme', error: error.message });
  }
});

// 404 处理
app.use((req, res) => {
  res.status(404).json({ message: 'Route not found' });
});

// 错误处理
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    message: 'Something went wrong!',
    error: err.message
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log('');
  console.log('========================================');
  console.log('🎉 Meme Generator DEMO Server');
  console.log('========================================');
  console.log(`Server: http://localhost:${PORT}`);
  console.log(`Mode: DEMO (In-Memory Storage)`);
  console.log(`Storage: ${memesDB.length} memes in memory`);
  console.log('');
  console.log('⚠️  NOTE: This is a demo version!');
  console.log('  - Data stored in memory (lost on restart)');
  console.log('  - No Canvas image generation');
  console.log('  - Text overlay shown in frontend only');
  console.log('');
  console.log('API Endpoints:');
  console.log('  - GET    /api/health');
  console.log('  - GET    /api/memes');
  console.log('  - POST   /api/memes');
  console.log('  - GET    /api/memes/:id');
  console.log('  - PUT    /api/memes/:id');
  console.log('  - DELETE /api/memes/:id');
  console.log('  - POST   /api/memes/:id/generate');
  console.log('========================================');
  console.log('');
});
