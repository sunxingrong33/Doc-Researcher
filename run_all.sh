#!/bin/bash

echo "=========================================="
echo "🚀 启动 Doc-Researcher 完整系统"
echo "=========================================="

# 启动后端
echo ""
echo "📡 启动后端API服务器..."
cd backend
python app.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
echo ""
echo "🎨 启动前端开发服务器..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo "✅ 系统启动完成!"
echo "=========================================="
echo ""
echo "后端API: http://localhost:5000"
echo "前端界面: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 等待用户中断
trap "echo ''; echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
