require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');
const memeRoutes = require('./routes/memeRoutes');

const app = express();
const PORT = process.env.PORT || 5000;

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 静态文件服务 - 提供上传的图片
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// MongoDB 连接
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/meme-generator';

mongoose.connect(MONGODB_URI)
  .then(() => {
    console.log('✅ Connected to MongoDB');
  })
  .catch((err) => {
    console.error('❌ MongoDB connection error:', err);
    process.exit(1);
  });

// 路由
app.use('/api/memes', memeRoutes);

// 健康检查
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Meme Generator API',
    timestamp: new Date().toISOString()
  });
});

// 404 处理
app.use((req, res) => {
  res.status(404).json({ message: 'Route not found' });
});

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    message: 'Something went wrong!',
    error: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log('');
  console.log('========================================');
  console.log('🚀 Meme Generator API Server');
  console.log('========================================');
  console.log(`Server running on: http://localhost:${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`MongoDB: ${MONGODB_URI}`);
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
