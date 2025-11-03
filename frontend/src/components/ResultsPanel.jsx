import React, { useState } from 'react'
import './ResultsPanel.css'

function ResultsPanel({ conversations }) {
  const [expandedId, setExpandedId] = useState(null)

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id)
  }

  if (conversations.length === 0) {
    return (
      <div className="results-panel">
        <h2>📊 研究结果</h2>
        <div className="empty-results">
          <div className="empty-icon">💡</div>
          <p>还没有研究结果</p>
          <p className="empty-hint">上传文档并提交查询后，研究结果将显示在这里</p>
        </div>
      </div>
    )
  }

  return (
    <div className="results-panel">
      <h2>📊 研究结果 ({conversations.length})</h2>

      <div className="conversations-list">
        {conversations.map((conv) => (
          <div
            key={conv.id}
            className={`conversation-card ${expandedId === conv.id ? 'expanded' : ''}`}
          >
            <div
              className="conversation-header"
              onClick={() => toggleExpand(conv.id)}
            >
              <div className="query-info">
                <div className="query-text">
                  <span className="query-icon">❓</span>
                  <strong>{conv.query}</strong>
                </div>
                <div className="meta-info">
                  <span className="timestamp">🕐 {conv.timestamp}</span>
                  {conv.iterations > 0 && (
                    <span className="iterations">🔄 {conv.iterations} 次迭代</span>
                  )}
                </div>
              </div>
              <button className="expand-button">
                {expandedId === conv.id ? '▼' : '▶'}
              </button>
            </div>

            {expandedId === conv.id && (
              <div className="conversation-body">
                <div className="report-content">
                  {formatReport(conv.report)}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function formatReport(report) {
  // 简单的markdown格式化
  const lines = report.split('\n')

  return (
    <div className="formatted-report">
      {lines.map((line, index) => {
        // 标题
        if (line.startsWith('## ')) {
          return <h3 key={index} className="report-heading">{line.replace('## ', '')}</h3>
        }
        // 列表项
        if (line.startsWith('- ')) {
          return <li key={index} className="report-list-item">{line.replace('- ', '')}</li>
        }
        // 空行
        if (line.trim() === '') {
          return <br key={index} />
        }
        // 普通文本
        return <p key={index} className="report-paragraph">{line}</p>
      })}
    </div>
  )
}

export default ResultsPanel
