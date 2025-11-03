# Doc-Researcher 前端应用

这是Doc-Researcher系统的Web前端界面，提供直观的用户交互体验。

## 📸 功能特性

- 📁 **文档上传**: 支持拖拽上传多个PDF文档
- 🔍 **智能查询**: 输入研究问题，系统进行深度分析
- 📊 **结果展示**: 清晰展示研究报告和引用
- 💬 **对话历史**: 保存所有查询和结果，支持多轮对话
- 🎨 **现代UI**: 响应式设计，美观易用

## 🚀 快速开始

### 前置要求

- Node.js 16+
- npm 或 yarn

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

前端将在 `http://localhost:3000` 启动

### 3. 启动后端API

在另一个终端窗口：

```bash
cd backend
pip install -r requirements.txt
python app.py
```

后端API将在 `http://localhost:5000` 启动

## 📁 项目结构

```
frontend/
├── src/
│   ├── components/          # React组件
│   │   ├── DocumentUpload.jsx    # 文档上传组件
│   │   ├── QueryPanel.jsx        # 查询面板组件
│   │   └── ResultsPanel.jsx      # 结果展示组件
│   ├── App.jsx              # 主应用组件
│   ├── App.css              # 应用样式
│   ├── main.jsx             # 入口文件
│   └── index.css            # 全局样式
├── index.html               # HTML模板
├── package.json             # 依赖配置
└── vite.config.js          # Vite配置

backend/
├── app.py                   # Flask API服务
├── requirements.txt         # Python依赖
└── uploads/                 # 上传文件目录
```

## 🎯 使用说明

### 1. 上传文档

1. 点击或拖拽PDF文件到上传区域
2. 等待文档上传和解析完成
3. 已上传的文档会显示在左侧列表中

### 2. 执行研究

1. 在查询框中输入您的研究问题
2. 或点击示例查询快速开始
3. 点击"开始研究"按钮
4. 等待系统分析，结果将自动显示

### 3. 查看结果

1. 研究结果按时间倒序排列
2. 点击任意结果可展开查看详细报告
3. 报告包含查询、时间、迭代次数等信息

### 4. 重置系统

- 点击"重置系统"按钮清除所有文档和对话历史

## 🛠️ 构建生产版本

```bash
cd frontend
npm run build
```

构建文件将生成在 `frontend/dist` 目录。

## 🔌 API接口

前端通过以下API与后端交互：

- `POST /api/upload` - 上传文档
- `POST /api/research` - 执行研究查询
- `POST /api/reset` - 重置系统
- `GET /api/status` - 获取系统状态
- `GET /api/health` - 健康检查

## 🎨 技术栈

- **React 18** - UI框架
- **Vite** - 构建工具
- **Axios** - HTTP客户端
- **CSS3** - 样式设计

## 💡 开发提示

### 修改API地址

编辑 `frontend/vite.config.js`:

```javascript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://your-backend-url:5000',
        changeOrigin: true
      }
    }
  }
})
```

### 添加新组件

1. 在 `src/components/` 创建新的 `.jsx` 文件
2. 创建对应的 `.css` 文件
3. 在需要的地方导入使用

### 自定义样式

主题色和通用样式定义在：
- `src/index.css` - 全局样式
- `src/App.css` - 应用布局
- 各组件的 `.css` 文件 - 组件样式

## ⚠️ 注意事项

1. **文件大小限制**: 单个文件最大50MB
2. **文件格式**: 仅支持PDF格式
3. **并发限制**: 同时只能处理一个研究任务
4. **浏览器兼容**: 推荐使用Chrome、Firefox、Safari最新版本

## 🐛 故障排除

### 上传失败

- 检查文件是否为PDF格式
- 确认文件大小不超过50MB
- 检查后端服务是否正常运行

### 查询无响应

- 确认已上传文档
- 检查网络连接
- 查看浏览器控制台错误信息

### 样式显示异常

- 清除浏览器缓存
- 重启开发服务器
- 检查CSS文件是否正确导入

## 📝 更新日志

### v1.0.0 (2025-11-01)

- ✅ 初始版本发布
- ✅ 文档上传功能
- ✅ 查询和结果展示
- ✅ 响应式设计
- ✅ 对话历史管理

## 📄 许可证

本项目仅供教育和研究使用。

## 🙏 致谢

基于华为技术有限公司团队的研究论文：
*"Doc-Researcher: A Unified System for Multimodal Document Parsing and Deep Research"*
