const mongoose = require('mongoose');

const memeSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true
  },
  imageUrl: {
    type: String,
    required: true
  },
  topText: {
    type: String,
    default: ''
  },
  bottomText: {
    type: String,
    default: ''
  },
  fontSize: {
    type: Number,
    default: 48
  },
  textColor: {
    type: String,
    default: '#FFFFFF'
  },
  strokeColor: {
    type: String,
    default: '#000000'
  },
  generatedImageUrl: {
    type: String
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

// 添加索引以提高查询性能
memeSchema.index({ createdAt: -1 });

module.exports = mongoose.model('Meme', memeSchema);
