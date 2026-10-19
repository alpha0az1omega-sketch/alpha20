import React, { useState } from 'react';

export default function TutorSidebar() {
  const [messages, setMessages] = useState<{role: string, text: string}[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input;
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setInput('');
    setLoading(true);

    // Format history for the AI API context
    const history = messages.map(m => ({
      role: m.role === 'user' ? 'user' : 'assistant',
      content: m.text
    }));

    try {
      const res = await fetch('/api/tutor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg, history })
      });
      if (!res.ok) throw new Error("API request failed");
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'ai', text: data.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', text: "Error: Unable to connect to the AI service. Please try again." }]);
    } finally {
      setLoading(false);
    }
  };

  const extractExpression = (text: string) => {
    const match = text.match(/[A-Z]+\([^)]+\)(?: AND [A-Z]+\([^)]+\))*/g);
    return match ? match[0] : null;
  };

  return (
    <div className="tutor-sidebar">
      <h3 style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#17becf' }}>L.E.U. Tutor</h3>
      <div className="chat-window" style={{ height: '400px', overflowY: 'auto', border: '1px solid #ddd', padding: '10px', borderRadius: '4px', background: '#fff' }}>
        {messages.length === 0 && <p style={{ color: '#888', fontSize: '12px' }}>Ask a question about the grammar or request an example.</p>}
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: '10px', textAlign: m.role === 'user' ? 'right' : 'left' }}>
            <span style={{ display: 'inline-block', padding: '6px 10px', borderRadius: '8px', fontSize: '13px', background: m.role === 'user' ? '#17becf' : '#f0f0f0', color: m.role === 'user' ? '#fff' : '#333' }}>
              {m.text}
            </span>
            {m.role === 'ai' && extractExpression(m.text) && (
              <div style={{ marginTop: '5px' }}>
                <button 
                  onClick={() => {
                    const expr = extractExpression(m.text);
                    if (expr) window.dispatchEvent(new CustomEvent('alpha20-evaluate', { detail: expr }));
                  }}
                  style={{ fontSize: '11px', padding: '4px 8px', cursor: 'pointer', background: '#2ca02c', color: '#fff', border: 'none', borderRadius: '4px' }}
                >
                  ▶ Draw on canvas
                </button>
              </div>
            )}
          </div>
        ))}
        {loading && <p style={{ color: '#17becf', fontSize: '12px' }}>AI is thinking...</p>}
      </div>
      <form onSubmit={sendMessage} style={{ display: 'flex', marginTop: '10px' }}>
        <input 
          type="text" 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          placeholder="Ex: Give me an example." 
          style={{ flex: 1, padding: '8px', border: '1px solid #ddd', borderRadius: '4px 0 0 4px', fontSize: '13px' }} 
          disabled={loading}
        />
        <button 
          type="submit" 
          style={{ padding: '8px 15px', background: '#1a1a2e', color: '#fff', border: 'none', borderRadius: '0 4px 4px 0', cursor: loading ? 'not-allowed' : 'pointer' }}
          disabled={loading}
        >
          Send
        </button>
      </form>
    </div>
  );
}
