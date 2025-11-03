const Meme = require('../models/Meme');
const { createCanvas, loadImage } = require('canvas');
const path = require('path');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');

// 获取所有 memes
exports.getAllMemes = async (req, res) => {
  try {
    const memes = await Meme.find().sort({ createdAt: -1 });
    res.json(memes);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching memes', error: error.message });
  }
};

// 获取单个 meme
exports.getMemeById = async (req, res) => {
  try {
    const meme = await Meme.findById(req.params.id);
    if (!meme) {
      return res.status(404).json({ message: 'Meme not found' });
    }
    res.json(meme);
  } catch (error) {
    res.status(500).json({ message: 'Error fetching meme', error: error.message });
  }
};

// 创建新 meme
exports.createMeme = async (req, res) => {
  try {
    const { title, topText, bottomText, fontSize, textColor, strokeColor } = req.body;

    if (!req.file) {
      return res.status(400).json({ message: 'Image file is required' });
    }

    const imageUrl = `/uploads/${req.file.filename}`;

    const meme = new Meme({
      title,
      imageUrl,
      topText: topText || '',
      bottomText: bottomText || '',
      fontSize: fontSize || 48,
      textColor: textColor || '#FFFFFF',
      strokeColor: strokeColor || '#000000'
    });

    await meme.save();
    res.status(201).json(meme);
  } catch (error) {
    res.status(500).json({ message: 'Error creating meme', error: error.message });
  }
};

// 生成 meme 图片（带文字）
exports.generateMeme = async (req, res) => {
  try {
    const { id } = req.params;
    const meme = await Meme.findById(id);

    if (!meme) {
      return res.status(404).json({ message: 'Meme not found' });
    }

    // 加载原始图片
    const imagePath = path.join(__dirname, '..', meme.imageUrl);
    const image = await loadImage(imagePath);

    // 创建 canvas
    const canvas = createCanvas(image.width, image.height);
    const ctx = canvas.getContext('2d');

    // 绘制图片
    ctx.drawImage(image, 0, 0);

    // 设置文字样式
    const fontSize = meme.fontSize || 48;
    ctx.font = `bold ${fontSize}px Impact, sans-serif`;
    ctx.textAlign = 'center';
    ctx.fillStyle = meme.textColor || '#FFFFFF';
    ctx.strokeStyle = meme.strokeColor || '#000000';
    ctx.lineWidth = fontSize / 20;

    // 绘制顶部文字
    if (meme.topText) {
      const topY = fontSize + 20;
      ctx.strokeText(meme.topText.toUpperCase(), canvas.width / 2, topY);
      ctx.fillText(meme.topText.toUpperCase(), canvas.width / 2, topY);
    }

    // 绘制底部文字
    if (meme.bottomText) {
      const bottomY = canvas.height - 20;
      ctx.strokeText(meme.bottomText.toUpperCase(), canvas.width / 2, bottomY);
      ctx.fillText(meme.bottomText.toUpperCase(), canvas.width / 2, bottomY);
    }

    // 保存生成的图片
    const generatedFilename = `generated-${uuidv4()}.png`;
    const generatedPath = path.join(__dirname, '../uploads', generatedFilename);
    const out = fs.createWriteStream(generatedPath);
    const stream = canvas.createPNGStream();
    stream.pipe(out);

    await new Promise((resolve, reject) => {
      out.on('finish', resolve);
      out.on('error', reject);
    });

    // 更新数据库
    meme.generatedImageUrl = `/uploads/${generatedFilename}`;
    await meme.save();

    res.json(meme);
  } catch (error) {
    console.error('Error generating meme:', error);
    res.status(500).json({ message: 'Error generating meme', error: error.message });
  }
};

// 更新 meme
exports.updateMeme = async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    const meme = await Meme.findByIdAndUpdate(id, updates, { new: true });

    if (!meme) {
      return res.status(404).json({ message: 'Meme not found' });
    }

    res.json(meme);
  } catch (error) {
    res.status(500).json({ message: 'Error updating meme', error: error.message });
  }
};

// 删除 meme
exports.deleteMeme = async (req, res) => {
  try {
    const { id } = req.params;
    const meme = await Meme.findByIdAndDelete(id);

    if (!meme) {
      return res.status(404).json({ message: 'Meme not found' });
    }

    // 删除相关文件
    if (meme.imageUrl) {
      const imagePath = path.join(__dirname, '..', meme.imageUrl);
      if (fs.existsSync(imagePath)) {
        fs.unlinkSync(imagePath);
      }
    }

    if (meme.generatedImageUrl) {
      const generatedPath = path.join(__dirname, '..', meme.generatedImageUrl);
      if (fs.existsSync(generatedPath)) {
        fs.unlinkSync(generatedPath);
      }
    }

    res.json({ message: 'Meme deleted successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Error deleting meme', error: error.message });
  }
};
