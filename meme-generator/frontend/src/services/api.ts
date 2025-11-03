import axios from 'axios';
import { Meme, CreateMemeData, UpdateMemeData } from '../types';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const memeAPI = {
  // 获取所有 memes
  getAllMemes: async (): Promise<Meme[]> => {
    const response = await api.get<Meme[]>('/memes');
    return response.data;
  },

  // 获取单个 meme
  getMemeById: async (id: string): Promise<Meme> => {
    const response = await api.get<Meme>(`/memes/${id}`);
    return response.data;
  },

  // 创建新 meme
  createMeme: async (data: CreateMemeData): Promise<Meme> => {
    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('topText', data.topText);
    formData.append('bottomText', data.bottomText);
    formData.append('fontSize', (data.fontSize || 48).toString());
    formData.append('textColor', data.textColor || '#FFFFFF');
    formData.append('strokeColor', data.strokeColor || '#000000');
    formData.append('image', data.image);

    const response = await axios.post<Meme>(`${API_BASE_URL}/memes`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  // 生成 meme 图片
  generateMeme: async (id: string): Promise<Meme> => {
    const response = await api.post<Meme>(`/memes/${id}/generate`);
    return response.data;
  },

  // 更新 meme
  updateMeme: async (id: string, data: UpdateMemeData): Promise<Meme> => {
    const response = await api.put<Meme>(`/memes/${id}`, data);
    return response.data;
  },

  // 删除 meme
  deleteMeme: async (id: string): Promise<void> => {
    await api.delete(`/memes/${id}`);
  }
};

export default api;
