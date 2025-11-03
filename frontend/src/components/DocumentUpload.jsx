import React, { useRef } from 'react'
import './DocumentUpload.css'

function DocumentUpload({ onUpload, documents, isProcessing, onReset }) {
  const fileInputRef = useRef(null)

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    if (files.length > 0) {
      onUpload(files)
    }
    // 重置input以允许重复选择同一文件
    e.target.value = ''
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const files = Array.from(e.dataTransfer.files).filter(file =>
      file.type === 'application/pdf' || file.name.endsWith('.pdf')
    )
    if (files.length > 0) {
      onUpload(files)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  return (
    <div className="document-upload">
      <h2>📁 文档管理</h2>

      <div
        className="upload-area"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="upload-icon">📤</div>
        <p className="upload-text">点击或拖拽PDF文件到这里</p>
        <p className="upload-hint">支持多个文件上传</p>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          multiple
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
      </div>

      {documents.length > 0 && (
        <div className="documents-list">
          <h3>已上传文档 ({documents.length})</h3>
          <ul>
            {documents.map((doc, index) => (
              <li key={index} className="document-item">
                <span className="doc-icon">📄</span>
                <span className="doc-name" title={doc}>{doc}</span>
              </li>
            ))}
          </ul>
          <button
            className="reset-button"
            onClick={onReset}
            disabled={isProcessing}
          >
            🔄 重置系统
          </button>
        </div>
      )}

      {documents.length === 0 && (
        <div className="empty-state">
          <p>还没有上传文档</p>
          <p className="empty-hint">上传PDF文档开始研究</p>
        </div>
      )}
    </div>
  )
}

export default DocumentUpload
