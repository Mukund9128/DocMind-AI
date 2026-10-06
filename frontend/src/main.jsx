import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import api from './api';
import './style.css';


function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [mode, setMode] = useState('dashboard');
  const [docs, setDocs] = useState([]);
  const [msg, setMsg] = useState('');

  const load = async () => {
    if (!token) return;

    try {
      const response = await api.get('/documents');
      setDocs(response.data);
    } catch (e) {
      console.log(e);
    }
  };

  useEffect(() => {
    load();
  }, [token]);

  if (!token) {
    return (
      <Auth
        onLogin={(t) => {
          localStorage.setItem('token', t);
          setToken(t);
        }}
      />
    );
  }

  const menu = [
    ['dashboard', '▦', 'Dashboard'],
    ['documents', '▤', 'Documents'],
    ['upload', '↑', 'Upload'],
    ['chat', '✦', 'AI Chat'],
    ['summarize', '≡', 'Summarize'],
    ['history', '◷', 'Chat History'],
    ['compare', '⇄', 'Compare']
  ];

  const pageTitles = {
    dashboard: 'Dashboard',
    documents: 'Documents',
    upload: 'Upload Document',
    chat: 'AI Chat',
    summarize: 'Summarize Document',
    history: 'Chat History',
    compare: 'Compare Documents'
  };

  return (
    <div className="app">

      <aside>
        <div className="brand">
          <div className="brand-icon">D</div>

          <div>
            <h2>DocMind AI</h2>
            <small>Document Intelligence</small>
          </div>
        </div>

        <div className="menu-label">
          WORKSPACE
        </div>

        <nav>
          {menu.map(([key, icon, label]) => (
            <button
              key={key}
              className={mode === key ? 'active' : ''}
              onClick={() => {
                setMode(key);
                setMsg('');
              }}
            >
              <span className="nav-icon">
                {icon}
              </span>

              {label}
            </button>
          ))}
        </nav>

        <button
          className="logout"
          onClick={() => {
            localStorage.clear();
            setToken(null);
          }}
        >
          <span className="nav-icon">↪</span>
          Logout
        </button>
      </aside>


      <main>
        <header>
          <div>
            <h1>{pageTitles[mode]}</h1>

            <p>
              AI-powered document intelligence workspace
            </p>
          </div>

          <div className="status-badge">
            <span></span>
            AI Ready
          </div>
        </header>


        {msg && (
          <div className="notice">
            {msg}
          </div>
        )}


        {mode === 'dashboard' && (
          <Dashboard
            docs={docs}
            setMode={setMode}
          />
        )}

        {mode === 'documents' && (
          <Documents
            docs={docs}
            reload={load}
          />
        )}

        {mode === 'upload' && (
          <Upload
            reload={load}
            setMsg={setMsg}
          />
        )}

        {mode === 'chat' && (
          <Chat docs={docs} />
        )}

        {mode === 'summarize' && (
          <Summarize docs={docs} />
        )}

        {mode === 'history' && (
          <ChatHistory />
        )}

        {mode === 'compare' && (
          <Compare docs={docs} />
        )}
      </main>

    </div>
  );
}


/* =========================================
   LOGIN / REGISTER
========================================= */

function Auth({ onLogin }) {
  const [reg, setReg] = useState(false);

  const [form, setForm] = useState({
    name: '',
    email: '',
    password: ''
  });

  const [error, setError] = useState('');

  async function submit() {
    try {
      setError('');

      if (reg) {
        await api.post('/auth/register', form);

        setReg(false);

        setError(
          'Registration successful. Please login.'
        );
      } else {
        const response =
          await api.post('/auth/login', form);

        onLogin(response.data.access_token);
      }
    } catch (e) {
      setError(
        e.response?.data?.error ||
        e.response?.data?.msg ||
        'Request failed'
      );
    }
  }

  return (
    <div className="auth-page">

      <div className="auth card">

        <div className="auth-logo">
          D
        </div>

        <h1>DocMind AI</h1>

        <h3>
          {reg
            ? 'Create your workspace'
            : 'Welcome back'}
        </h3>

        {reg && (
          <input
            placeholder="Full name"
            onChange={(e) =>
              setForm({
                ...form,
                name: e.target.value
              })
            }
          />
        )}

        <input
          type="email"
          placeholder="Email address"
          onChange={(e) =>
            setForm({
              ...form,
              email: e.target.value
            })
          }
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) =>
            setForm({
              ...form,
              password: e.target.value
            })
          }
        />

        <button
          className="primary full"
          onClick={submit}
        >
          {reg ? 'Create Account' : 'Login'}
        </button>

        {error && (
          <p className="auth-message">
            {error}
          </p>
        )}

        <button
          className="link-button"
          onClick={() => {
            setReg(!reg);
            setError('');
          }}
        >
          {reg
            ? 'Already have an account? Login'
            : 'New to DocMind? Create account'}
        </button>

      </div>

    </div>
  );
}


/* =========================================
   DASHBOARD
========================================= */

function Dashboard({ docs, setMode }) {
  return (
    <>

      <section className="welcome-card">

        <div>
          <span className="eyebrow">
            DOCMIND WORKSPACE
          </span>

          <h2>
            Turn your documents into knowledge.
          </h2>

          <p>
            Upload documents, ask grounded questions,
            summarize content, compare information and
            review previous AI conversations from one
            workspace.
          </p>
        </div>

        <button
          onClick={() => setMode('upload')}
        >
          + Upload Document
        </button>

      </section>


      <section className="stats-grid">

        <StatCard
          icon="▤"
          title="Total Documents"
          value={docs.length}
          text="Documents in your workspace"
        />

        <StatCard
          icon="✦"
          title="AI Chat"
          value="RAG"
          text="Grounded document Q&A"
        />

        <StatCard
          icon="≡"
          title="Summarize"
          value="AI"
          text="Generate document summaries"
        />

        <StatCard
          icon="⇄"
          title="Compare"
          value="2 Docs"
          text="AI document comparison"
        />

      </section>


      <section className="dashboard-bottom">

        <div className="card quick-card">

          <div className="section-heading">
            <div>
              <h2>Quick Actions</h2>

              <p>
                Continue working with your documents.
              </p>
            </div>
          </div>


          <div className="quick-actions">

            <button
              className="quick-action"
              onClick={() => setMode('upload')}
            >
              <span>↑</span>

              <div>
                <b>Upload Document</b>
                <small>
                  Add PDF or DOCX files
                </small>
              </div>
            </button>


            <button
              className="quick-action"
              onClick={() => setMode('chat')}
            >
              <span>✦</span>

              <div>
                <b>Ask DocMind</b>
                <small>
                  Ask questions using RAG
                </small>
              </div>
            </button>


            <button
              className="quick-action"
              onClick={() => setMode('summarize')}
            >
              <span>≡</span>

              <div>
                <b>Summarize</b>
                <small>
                  Generate document summary
                </small>
              </div>
            </button>


            <button
              className="quick-action"
              onClick={() => setMode('compare')}
            >
              <span>⇄</span>

              <div>
                <b>Compare Documents</b>
                <small>
                  Analyze two documents
                </small>
              </div>
            </button>

          </div>

        </div>


        <div className="card system-card">

          <h2>System Status</h2>

          <div className="system-row">
            <span>
              <i className="online-dot"></i>
              Document Engine
            </span>

            <b>Ready</b>
          </div>

          <div className="system-row">
            <span>
              <i className="online-dot"></i>
              Semantic Search
            </span>

            <b>Ready</b>
          </div>

          <div className="system-row">
            <span>
              <i className="online-dot"></i>
              AI Assistant
            </span>

            <b>Ready</b>
          </div>

        </div>

      </section>

    </>
  );
}


function StatCard({
  icon,
  title,
  value,
  text
}) {
  return (
    <div className="stat-card">

      <div className="stat-icon">
        {icon}
      </div>

      <div>
        <p>{title}</p>

        <h3>{value}</h3>

        <small>{text}</small>
      </div>

    </div>
  );
}


/* =========================================
   DOCUMENTS
========================================= */

function Documents({ docs, reload }) {
  async function del(id) {
    const confirmed =
      window.confirm(
        'Are you sure you want to delete this document?'
      );

    if (!confirmed) return;

    try {
      await api.delete('/documents/' + id);

      reload();
    } catch (e) {
      alert(
        e.response?.data?.error ||
        'Unable to delete document.'
      );
    }
  }

  return (
    <div className="card">

      <div className="section-heading">
        <div>
          <h2>Your Documents</h2>

          <p>
            Manage documents available to DocMind.
          </p>
        </div>

        <span className="count-badge">
          {docs.length} files
        </span>
      </div>


      {docs.length ? (
        <div className="document-list">

          {docs.map((d) => (
            <div
              className="row"
              key={d.id}
            >

              <div className="document-info">

                <div className="file-icon">
                  {d.file_type?.toUpperCase() === 'PDF'
                    ? 'PDF'
                    : 'DOC'}
                </div>

                <span>
                  <b>{d.name}</b>

                  <small>
                    {d.file_type?.toUpperCase()}
                    {' · '}
                    {d.pages} pages
                  </small>
                </span>

              </div>

              <button
                className="danger-button"
                onClick={() => del(d.id)}
              >
                Delete
              </button>

            </div>
          ))}

        </div>
      ) : (
        <EmptyState
          icon="▤"
          title="No documents yet"
          text="Upload your first PDF or DOCX to begin."
        />
      )}

    </div>
  );
}


/* =========================================
   UPLOAD
========================================= */

function Upload({ reload, setMsg }) {
  const [file, setFile] = useState();
  const [uploading, setUploading] =
    useState(false);

  async function go() {
    if (!file || uploading) return;

    const fd = new FormData();

    fd.append('file', file);

    try {
      setUploading(true);

      await api.post(
        '/documents/upload',
        fd
      );

      setMsg(
        'Document uploaded and indexed successfully.'
      );

      setFile(undefined);

      reload();
    } catch (e) {
      setMsg(
        e.response?.data?.error ||
        'Upload failed'
      );
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="card upload-card">

      <div className="upload-icon">
        ↑
      </div>

      <h2>Upload a Document</h2>

      <p>
        Add a PDF or DOCX file to your knowledge
        workspace. DocMind will extract and index
        the document for AI search.
      </p>

      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      {file && (
        <div className="selected-file">
          Selected: <b>{file.name}</b>
        </div>
      )}

      <button
        disabled={!file || uploading}
        onClick={go}
      >
        {uploading
          ? 'Processing...'
          : 'Upload & Process'}
      </button>

      <small className="upload-help">
        Supported formats: PDF and DOCX
      </small>

    </div>
  );
}


/* =========================================
   CHAT
========================================= */

function Chat({ docs }) {
  const [sel, setSel] = useState([]);
  const [q, setQ] = useState('');
  const [a, setA] = useState('');
  const [sources, setSources] =
    useState([]);
  const [loading, setLoading] =
    useState(false);

  async function go() {
    if (!q.trim()) {
      setA('Please enter a question.');
      return;
    }

    if (sel.length === 0) {
      setA(
        'Please select at least one document.'
      );
      return;
    }

    try {
      setLoading(true);
      setA('');
      setSources([]);

      const r = await api.post(
        '/ai/ask',
        {
          document_ids: sel.map(Number),
          question: q
        }
      );

      setA(r.data.answer);

      setSources(r.data.sources || []);
    } catch (e) {
      setA(
        e.response?.data?.error ||
        e.response?.data?.msg ||
        'Unable to generate an answer.'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">

      <div className="section-heading">
        <div>
          <h2>Ask your documents</h2>

          <p>
            Select documents and ask a grounded
            question.
          </p>
        </div>

        <span className="ai-badge">
          ✦ RAG
        </span>
      </div>


      <div className="document-selector">

        <label className="field-label">
          Select knowledge sources
        </label>

        <DocChecks
          docs={docs}
          sel={sel}
          setSel={setSel}
        />

      </div>


      <label className="field-label">
        Your question
      </label>

      <textarea
        placeholder="Example: What are the main concepts explained in this document?"
        value={q}
        onChange={(e) =>
          setQ(e.target.value)
        }
      />


      <button
        disabled={loading}
        onClick={go}
      >
        {loading
          ? 'DocMind is thinking...'
          : '✦ Ask AI'}
      </button>


      {a && (
        <div className="answer">

          <div className="answer-title">
            <span>✦</span>
            DocMind Answer
          </div>

          {a}

        </div>
      )}


      {sources.length > 0 && (
        <div className="sources">

          <h4>
            Sources
          </h4>

          <div className="source-list">

            {sources.map(
              (s, index) => (
                <div
                  className="source"
                  key={index}
                >
                  ▤ {s.document}
                  {' · page '}
                  {s.page}
                </div>
              )
            )}

          </div>

        </div>
      )}

    </div>
  );
}


/* =========================================
   SUMMARIZE
========================================= */

function Summarize({ docs }) {
  const [selectedDoc, setSelectedDoc] =
    useState('');

  const [summary, setSummary] =
    useState('');

  const [loading, setLoading] =
    useState(false);


  async function generateSummary() {
    if (!selectedDoc) {
      setSummary(
        'Please select a document first.'
      );
      return;
    }

    try {
      setLoading(true);
      setSummary('');

      const response = await api.post(
        '/ai/summarize',
        {
          document_id: Number(selectedDoc)
        }
      );

      setSummary(
        response.data.summary ||
        'No summary was returned.'
      );

    } catch (e) {
      setSummary(
        e.response?.data?.error ||
        e.response?.data?.msg ||
        'Unable to summarize this document.'
      );
    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="card">

      <div className="section-heading">

        <div>
          <h2>AI Document Summarizer</h2>

          <p>
            Select one document and generate an
            AI summary based only on its content.
          </p>
        </div>

        <span className="ai-badge">
          ≡ AI Summary
        </span>

      </div>


      {docs.length === 0 ? (

        <EmptyState
          icon="≡"
          title="No documents available"
          text="Upload a PDF or DOCX before generating a summary."
        />

      ) : (

        <>
          <label className="field-label">
            Select document
          </label>

          <select
            className="document-select"
            value={selectedDoc}
            onChange={(e) => {
              setSelectedDoc(
                e.target.value
              );

              setSummary('');
            }}
          >

            <option value="">
              Choose a document...
            </option>

            {docs.map((doc) => (
              <option
                key={doc.id}
                value={doc.id}
              >
                {doc.name}
              </option>
            ))}

          </select>


          <button
            disabled={
              !selectedDoc ||
              loading
            }
            onClick={generateSummary}
          >
            {loading
              ? 'Generating Summary...'
              : '✦ Generate Summary'}
          </button>


          {summary && (
            <div className="answer">

              <div className="answer-title">
                <span>≡</span>
                Document Summary
              </div>

              {summary}

            </div>
          )}

        </>

      )}

    </div>
  );
}


/* =========================================
   CHAT HISTORY
========================================= */

function ChatHistory() {
  const [chats, setChats] = useState([]);
  const [messages, setMessages] =
    useState([]);
  const [selectedChat, setSelectedChat] =
    useState(null);
  const [loading, setLoading] =
    useState(true);

  useEffect(() => {
    loadChats();
  }, []);

  async function loadChats() {
    try {
      const r = await api.get('/chats');

      setChats(r.data);
    } catch (e) {
      console.log(
        'Chat history error:',
        e.response?.data
      );
    } finally {
      setLoading(false);
    }
  }

  async function openChat(chat) {
    setSelectedChat(chat);
    setMessages([]);

    try {
      const r = await api.get(
        `/chats/${chat.id}/messages`
      );

      setMessages(r.data);
    } catch (e) {
      console.log(
        'Message history error:',
        e.response?.data
      );
    }
  }

  if (loading) {
    return (
      <div className="card">
        <p>Loading chat history...</p>
      </div>
    );
  }

  return (
    <div className="card">

      <div className="section-heading">

        <div>
          <h2>Previous Conversations</h2>

          <p>
            Revisit your previous document
            questions and AI answers.
          </p>
        </div>

        <span className="count-badge">
          {chats.length} chats
        </span>

      </div>


      {chats.length === 0 && (
        <EmptyState
          icon="◷"
          title="No chat history yet"
          text="Your AI conversations will appear here."
        />
      )}


      {chats.map((chat) => (
        <div
          className="row"
          key={chat.id}
        >

          <div className="history-info">

            <div className="history-icon">
              ✦
            </div>

            <span>
              <b>{chat.title}</b>

              <small>
                {new Date(
                  chat.created_at
                ).toLocaleString()}
              </small>
            </span>

          </div>

          <button
            className="secondary-button"
            onClick={() =>
              openChat(chat)
            }
          >
            Open
          </button>

        </div>
      ))}


      {selectedChat && (
        <div className="history-chat">

          <hr />

          <h3>
            {selectedChat.title}
          </h3>

          {messages.map(
            (message, index) => (
              <div
                key={index}
                className={
                  message.role === 'user'
                    ? 'history-message user-message'
                    : 'history-message ai-message'
                }
              >

                <b>
                  {message.role === 'user'
                    ? 'You'
                    : '✦ DocMind AI'}
                </b>

                <p>
                  {message.content}
                </p>


                {message.sources?.length > 0 && (
                  <div className="sources">

                    {message.sources.map(
                      (source, i) => (
                        <div
                          className="source"
                          key={i}
                        >
                          ▤ {source.document}
                          {' · page '}
                          {source.page}
                        </div>
                      )
                    )}

                  </div>
                )}

              </div>
            )
          )}

        </div>
      )}

    </div>
  );
}


/* =========================================
   DOCUMENT CHECKBOXES
========================================= */

function DocChecks({
  docs,
  sel,
  setSel
}) {
  if (docs.length === 0) {
    return (
      <p className="muted">
        No documents available. Upload a document first.
      </p>
    );
  }

  return (
    <div className="check-list">

      {docs.map((d) => (
        <label
          className={
            sel.includes(d.id)
              ? 'check selected'
              : 'check'
          }
          key={d.id}
        >

          <input
            type="checkbox"
            checked={sel.includes(d.id)}
            onChange={(e) =>
              setSel(
                e.target.checked
                  ? [...sel, d.id]
                  : sel.filter(
                      (x) => x !== d.id
                    )
              )
            }
          />

          <span>
            <b>{d.name}</b>

            <small>
              {d.file_type?.toUpperCase()}
              {' · '}
              {d.pages} pages
            </small>
          </span>

        </label>
      ))}

    </div>
  );
}


/* =========================================
   COMPARE
========================================= */

function Compare({ docs }) {
  const [sel, setSel] = useState([]);
  const [out, setOut] = useState('');
  const [loading, setLoading] =
    useState(false);

  async function go() {
    if (sel.length !== 2) {
      setOut(
        'Please select exactly two documents.'
      );
      return;
    }

    try {
      setLoading(true);
      setOut('');

      const r = await api.post(
        '/ai/compare',
        {
          document_ids: sel
        }
      );

      setOut(r.data.comparison);
    } catch (e) {
      setOut(
        e.response?.data?.error ||
        e.response?.data?.msg ||
        'Unable to compare documents.'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card">

      <div className="section-heading">

        <div>
          <h2>Compare Documents</h2>

          <p>
            Select exactly two documents and let
            DocMind identify similarities,
            differences and important facts.
          </p>
        </div>

        <span className="ai-badge">
          ⇄ AI Compare
        </span>

      </div>


      <DocChecks
        docs={docs}
        sel={sel}
        setSel={(x) =>
          setSel(x.slice(-2))
        }
      />


      <button
        disabled={loading}
        onClick={go}
      >
        {loading
          ? 'Comparing...'
          : '⇄ Compare with AI'}
      </button>


      {out && (
        <div className="answer">

          <div className="answer-title">
            <span>⇄</span>
            Comparison Result
          </div>

          {out}

        </div>
      )}

    </div>
  );
}


/* =========================================
   EMPTY STATE
========================================= */

function EmptyState({
  icon,
  title,
  text
}) {
  return (
    <div className="empty-state">

      <div className="empty-icon">
        {icon}
      </div>

      <h3>{title}</h3>

      <p>{text}</p>

    </div>
  );
}


createRoot(
  document.getElementById('root')
).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);