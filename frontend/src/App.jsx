import React, { useState } from 'react'
import axios from 'axios'
import DocumentUpload from './components/DocumentUpload'
import QueryPanel from './components/QueryPanel'
import ResultsPanel from './components/ResultsPanel'
import './App.css'

function App() {
  const [documents, setDocuments] = useState([])
  const [conversations, setConversations] = useState([])
  const [isProcessing, setIsProcessing] = useState(false)
  const [systemStatus, setSystemStatus] = useState('')

  const handleDocumentsUploaded = async (files) => {
    setIsProcessing(true)
    setSystemStatus('正在上传文档...')

    const formData = new FormData()
    files.forEach(file => {
      formData.append('documents', file)
    })

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setDocuments(response.data.documents)
      setSystemStatus(`成功上传 ${response.data.documents.length} 个文档`)
      setTimeout(() => setSystemStatus(''), 3000)
    } catch (error) {
      console.error('上传文档失败:', error)
      setSystemStatus('上传失败: ' + (error.response?.data?.error || error.message))
    } finally {
      setIsProcessing(false)
    }
  }

  const handleQuery = async (query) => {
    if (!query.trim()) {
      setSystemStatus('请输入查询内容')
      return
    }

    setIsProcessing(true)
    setSystemStatus('正在研究您的问题...')

    try {
      const response = await axios.post('/api/research', {
        query: query
      })

      const newConversation = {
        id: Date.now(),
        query: query,
        report: response.data.report,
        timestamp: new Date().toLocaleString(),
        iterations: response.data.iterations || 0
      }

      setConversations([newConversation, ...conversations])
      setSystemStatus('研究完成')
      setTimeout(() => setSystemStatus(''), 3000)
    } catch (error) {
      console.error('研究失败:', error)
      setSystemStatus('研究失败: ' + (error.response?.data?.error || error.message))
    } finally {
      setIsProcessing(false)
    }
  }

  const handleReset = async () => {
    try {
      await axios.post('/api/reset')
      setDocuments([])
      setConversations([])
      setSystemStatus('系统已重置')
      setTimeout(() => setSystemStatus(''), 3000)
    } catch (error) {
      console.error('重置失败:', error)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>📚 Doc-Researcher</h1>
          <p className="subtitle">多模态文档解析和深度研究系统</p>
        </div>
        {systemStatus && (
          <div className="status-bar">
            {systemStatus}
          </div>
        )}
      </header>

      <div className="app-content">
        <div className="sidebar">
          <DocumentUpload
            onUpload={handleDocumentsUploaded}
            documents={documents}
            isProcessing={isProcessing}
            onReset={handleReset}
          />
        </div>

        <div className="main-panel">
          <QueryPanel
            onQuery={handleQuery}
            isProcessing={isProcessing}
          />

          <ResultsPanel
            conversations={conversations}
          />
        </div>
      </div>

      <footer className="app-footer">
        <p>基于论文: <em>Doc-Researcher: A Unified System for Multimodal Document Parsing and Deep Research</em></p>
      </footer>
    </div>
  )
}

export default App
