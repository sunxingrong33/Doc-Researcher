"""
Flask后端API服务
提供Doc-Researcher系统的RESTful API接口
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from werkzeug.utils import secure_filename

# 添加父目录到路径以导入doc_researcher
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from doc_researcher import DocResearcher

app = Flask(__name__)
CORS(app)

# 配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# 创建上传文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 全局Doc-Researcher实例
researcher = None


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'Doc-Researcher API'
    })


@app.route('/api/upload', methods=['POST'])
def upload_documents():
    """上传文档"""
    global researcher

    if 'documents' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400

    files = request.files.getlist('documents')
    if not files or files[0].filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    uploaded_files = []
    file_paths = []

    try:
        # 保存上传的文件
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_files.append(filename)
                file_paths.append(filepath)

        if not file_paths:
            return jsonify({'error': '没有有效的PDF文件'}), 400

        # 创建或重置研究器
        researcher = DocResearcher(
            max_iterations=3,
            sufficiency_threshold=0.7
        )

        # 添加文档 (注意: 这里使用模拟的文档，因为真实解析需要额外的库)
        # 在生产环境中，这里应该调用 researcher.add_documents(file_paths)
        researcher.add_documents(file_paths)

        return jsonify({
            'message': f'成功上传 {len(uploaded_files)} 个文档',
            'documents': uploaded_files
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/research', methods=['POST'])
def research():
    """执行研究查询"""
    global researcher

    if researcher is None:
        return jsonify({'error': '请先上传文档'}), 400

    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': '缺少查询参数'}), 400

    query = data['query']
    if not query.strip():
        return jsonify({'error': '查询不能为空'}), 400

    try:
        # 执行研究
        report = researcher.research(query)

        # 获取迭代次数（如果available）
        iterations = getattr(researcher, '_last_iterations', 0)

        return jsonify({
            'report': report,
            'iterations': iterations,
            'query': query
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """重置系统"""
    global researcher

    try:
        # 清理上传的文件
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)

        # 重置研究器
        researcher = None

        return jsonify({'message': '系统已重置'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """获取系统状态"""
    global researcher

    status = {
        'initialized': researcher is not None,
        'documents_count': 0,
        'conversations_count': 0
    }

    if researcher:
        status['documents_count'] = len(researcher.documents)
        status['conversations_count'] = len(researcher.conversation_history)

    return jsonify(status)


if __name__ == '__main__':
    print("="*60)
    print("🚀 Doc-Researcher API Server")
    print("="*60)
    print("Server running on: http://localhost:5000")
    print("API endpoints:")
    print("  - GET  /api/health       - 健康检查")
    print("  - POST /api/upload       - 上传文档")
    print("  - POST /api/research     - 执行研究")
    print("  - POST /api/reset        - 重置系统")
    print("  - GET  /api/status       - 系统状态")
    print("="*60)

    app.run(debug=True, host='0.0.0.0', port=5000)
