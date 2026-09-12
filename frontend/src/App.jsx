import { useState } from 'react'
import './App.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState('')
  const [question, setQuestion] = useState('')
  const [chatAnswer, setChatAnswer] = useState('')
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(false)

  async function handleUpload(event) {
    event.preventDefault()

    if (!selectedFile) {
      setUploadStatus('Please choose a PDF file first.')
      return
    }

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Upload failed')
      }

      setUploadStatus(`Uploaded: ${data.filename} (${data.status})`)
    } catch (error) {
      setUploadStatus(error.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleAskQuestion(event) {
    event.preventDefault()

    if (!question.trim()) {
      setChatAnswer('Please enter a question first.')
      return
    }

    try {
      setLoading(true)
      const response = await fetch(`${API_BASE_URL}/documents/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question, top_k: 3 }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Chat request failed')
      }

      setChatAnswer(data.answer || 'No answer found.')
      setSources(data.sources || [])
    } catch (error) {
      setChatAnswer(error.message)
      setSources([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">AI Knowledge Workspace</p>
          <h1>Document Upload & Q&A</h1>
        </div>
      </header>

      <main className="grid">
        <section className="panel">
          <h2>1. Upload PDF</h2>
          <form onSubmit={handleUpload} className="stack">
            <input
              type="file"
              accept="application/pdf"
              onChange={(event) => setSelectedFile(event.target.files?.[0] || null)}
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Uploading...' : 'Upload document'}
            </button>
          </form>
          {uploadStatus && <p className="status">{uploadStatus}</p>}
        </section>

        <section className="panel">
          <h2>2. Ask a question</h2>
          <form onSubmit={handleAskQuestion} className="stack">
            <textarea
              rows="4"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              placeholder="Ask about the uploaded document..."
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Thinking...' : 'Ask AI'}
            </button>
          </form>

          {chatAnswer && (
            <div className="answer-box">
              <h3>Answer</h3>
              <p>{chatAnswer}</p>
            </div>
          )}

          {sources.length > 0 && (
            <div className="source-box">
              <h3>Sources</h3>
              <ul>
                {sources.map((source, index) => (
                  <li key={`${source.document_id}-${index}`}>
                    <strong>{source.filename}</strong> · page {source.page_number} · score {source.score}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
