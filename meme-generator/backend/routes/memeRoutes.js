const express = require('express');
const router = express.Router();
const memeController = require('../controllers/memeController');
const upload = require('../middleware/upload');

// GET /api/memes - 获取所有 memes
router.get('/', memeController.getAllMemes);

// GET /api/memes/:id - 获取单个 meme
router.get('/:id', memeController.getMemeById);

// POST /api/memes - 创建新 meme
router.post('/', upload.single('image'), memeController.createMeme);

// POST /api/memes/:id/generate - 生成 meme 图片
router.post('/:id/generate', memeController.generateMeme);

// PUT /api/memes/:id - 更新 meme
router.put('/:id', memeController.updateMeme);

// DELETE /api/memes/:id - 删除 meme
router.delete('/:id', memeController.deleteMeme);

module.exports = router;
