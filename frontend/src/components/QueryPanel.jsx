import React, { useState } from 'react'
import './QueryPanel.css'

function QueryPanel({ onQuery, isProcessing }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim() && !isProcessing) {
      onQuery(query)
      setQuery('')
    }
  }

  const exampleQueries = [
    '这些文档讨论的主要技术是什么?',
    '比较文档中提到的不同方法的优缺点',
    '总结实验结果和关键发现',
    '文档中提到的系统架构是怎样的?'
  ]

  const handleExampleClick = (example) => {
    setQuery(example)
  }

  return (
    <div className="query-panel">
      <h2>🔍 深度研究查询</h2>

      <form onSubmit={handleSubmit} className="query-form">
        <textarea
          className="query-input"
          placeholder="请输入您的研究问题，例如：这些文档的主要贡献是什么？"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows="4"
          disabled={isProcessing}
        />

        <button
          type="submit"
          className="submit-button"
          disabled={!query.trim() || isProcessing}
        >
          {isProcessing ? '🔄 研究中...' : '🚀 开始研究'}
        </button>
      </form>

      <div className="example-queries">
        <p className="example-label">示例查询:</p>
        <div className="example-tags">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              className="example-tag"
              onClick={() => handleExampleClick(example)}
              disabled={isProcessing}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default QueryPanel
