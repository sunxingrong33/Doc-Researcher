#!/bin/bash

echo "=========================================="
echo "🚀 启动 Doc-Researcher 系统"
echo "=========================================="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "请先安装 Python 3.8+"
    exit 1
fi

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js"
    echo "请先安装 Node.js 16+"
    exit 1
fi

echo ""
echo "📦 安装后端依赖..."
cd backend
pip install -r requirements.txt

echo ""
echo "📦 安装前端依赖..."
cd ../frontend
npm install

echo ""
echo "=========================================="
echo "✅ 依赖安装完成!"
echo "=========================================="
echo ""
echo "启动说明:"
echo ""
echo "1. 启动后端API服务器 (端口 5000):"
echo "   cd backend"
echo "   python app.py"
echo ""
echo "2. 在新终端启动前端开发服务器 (端口 3000):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. 在浏览器打开: http://localhost:3000"
echo ""
echo "=========================================="
