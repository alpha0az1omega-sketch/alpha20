import React, { useState, useCallback, useEffect } from 'react';
import ReactFlow, { 
  Background, Controls, applyNodeChanges, applyEdgeChanges, 
  Node, Edge, NodeChange, EdgeChange, Handle, Position 
} from 'reactflow';
import 'reactflow/dist/style.css';

const SONIFICATION: Record<string, {freq: number, type: OscillatorType, desc: string}> = {
  "EXIST": { freq: 440, type: "sine", desc: "Something exists." },
  "CAUSE": { freq: 330, type: "triangle", desc: "A causes B." },
  "PART": { freq: 523, type: "sine", desc: "A is part of B." },
  "SAME": { freq: 440, type: "sine", desc: "A is the same as B." },
  "ONE": { freq: 659, type: "sine", desc: "There is exactly one." },
  "ALL": { freq: 554, type: "square", desc: "All of them." },
  "NOT": { freq: 220, type: "sawtooth", desc: "It is not the case." },
  "IF": { freq: 392, type: "sine", desc: "If A, then B." },
  "DO": { freq: 349, type: "sine", desc: "An action is performed." },
  "HAPPEN": { freq: 294, type: "sine", desc: "An event occurs." },
  "KNOW": { freq: 587, type: "sine", desc: "Knowledge of something." },
  "SEE": { freq: 880, type: "sine", desc: "To perceive visually." },
  "BIG": { freq: 110, type: "sine", desc: "Large in magnitude." },
  "LIVE": { freq: 330, type: "triangle", desc: "Alive and functioning." },
  "DIE": { freq: 165, type: "sawtooth", desc: "Cessation of life." },
  "MOVE": { freq: 440, type: "sine", desc: "Change of position." },
  "THINK": { freq: 523, type: "sine", desc: "Cognitive process." },
  "SAY": { freq: 392, type: "square", desc: "To communicate." },
  "TRUE": { freq: 659, type: "sine", desc: "The statement is true." },
  "GOOD": { freq: 784, type: "sine", desc: "Positive value." },
};
const PRIMITIVES = Object.keys(SONIFICATION);

let audioCtx: AudioContext | null = null;
const playSound = (name: string) => {
  if (!audioCtx) audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
  if (audioCtx.state === 'suspended') audioCtx.resume();
  const cfg = SONIFICATION[name];
  if (!cfg) return;
  
  // Web Speech API (Accessibility)
  if ('speechSynthesis' in window) {
    const msg = new SpeechSynthesisUtterance(`${name}. ${cfg.desc}`);
    msg.rate = 1.2;
    window.speechSynthesis.speak(msg);
  }

  // Web Audio API
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = cfg.type;
  osc.frequency.setValueAtTime(cfg.freq, audioCtx.currentTime);
  gain.gain.setValueAtTime(0, audioCtx.currentTime);
  gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.05);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
  osc.connect(gain); gain.connect(audioCtx.destination);
  osc.start(); osc.stop(audioCtx.currentTime + 0.5);
};

const PrimitiveNodeV2 = ({ data }: any) => {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      playSound(data.label);
    }
  };
  return (
    <div 
      onClick={() => playSound(data.label)}
      onKeyDown={handleKeyDown}
      tabIndex={0}
      role="button"
      aria-label={`Primitive ${data.label}. Press Enter to hear its definition and sound.`}
      style={{ padding: '10px 15px', border: '2px solid #17becf', borderRadius: '8px', background: '#fff', fontWeight: 'bold', color: '#1a1a2e', textAlign: 'center', cursor: 'pointer', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}
    >
      <Handle type="target" position={Position.Left} style={{ background: '#555' }} />
      {data.label}
      <Handle type="source" position={Position.Right} style={{ background: '#555' }} />
    </div>
  );
};
const nodeTypes = { primitive: PrimitiveNodeV2 };

export default function AlphaGraphV2() {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [compiledCode, setCompiledCode] = useState<string>("");

  const onNodesChange = useCallback((changes: NodeChange[]) => setNodes((nds) => applyNodeChanges(changes, nds)), []);
  const onEdgesChange = useCallback((changes: EdgeChange[]) => setEdges((eds) => applyEdgeChanges(changes, eds)), []);
  const onConnect = useCallback((params: any) => setEdges((eds) => [...eds, params]), []);

  const addNode = (label: string) => {
    playSound(label);
    const newNode: Node = { id: `node_${Date.now()}_${Math.random()}`, type: 'primitive', position: { x: Math.random() * 300 + 50, y: Math.random() * 300 + 50 }, data: { label } };
    setNodes((nds) => [...nds, newNode]);
  };

  useEffect(() => {
    const handleTutorExpression = (e: any) => {
      const expr = e.detail;
      setCompiledCode(expr);
      const matches = expr.match(/([A-Z]+)\(/g);
      if (matches) {
        const prims = matches.map((m: string) => m.replace('(', ''));
        const newNodes: Node[] = prims.map((p: string, i: number) => ({
          id: `node_ai_${Date.now()}_${i}`, type: 'primitive',
          position: { x: 100 + (i % 3) * 150, y: 100 + Math.floor(i / 3) * 100 }, data: { label: p }
        }));
        const newEdges: Edge[] = [];
        for (let i = 0; i < newNodes.length - 1; i++) {
          newEdges.push({ id: `e_${i}`, source: newNodes[i].id, target: newNodes[i+1].id, animated: true });
        }
        setNodes(newNodes); setEdges(newEdges);
        prims.forEach((p: string, i: number) => setTimeout(() => playSound(p), i * 1000));
      }
    };
    window.addEventListener('alpha20-evaluate', handleTutorExpression);
    return () => window.removeEventListener('alpha20-evaluate', handleTutorExpression);
  }, []);

  const compileGraph = () => {
    if (nodes.length === 0) return;
    const expression = nodes.map(n => `${n.data.label}(x)`).join(" AND ");
    setCompiledCode(expression);
    let delay = 0;
    nodes.forEach((n) => { setTimeout(() => playSound(n.data.label), delay); delay += 1000; });
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '650px', border: '1px solid #ddd', borderRadius: '8px', overflow: 'hidden' }}>
      <div style={{ padding: '10px', background: '#1a1a2e', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontFamily: 'monospace', fontSize: '12px' }}>{compiledCode ? `Expression: ${compiledCode}` : "Draw a graph to generate Alpha-20 code..."}</span>
        <button onClick={compileGraph} style={{ padding: '8px 16px', background: '#2ca02c', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>▶ Compile & Play</button>
      </div>
      <div style={{ display: 'flex', flex: 1 }}>
        <div style={{ width: '200px', background: '#fafafa', borderRight: '1px solid #ddd', padding: '10px', overflowY: 'auto' }} aria-label="Primitive Palette">
          <h3 style={{ fontSize: '14px', marginBottom: '10px' }}>Palette</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px' }}>
            {PRIMITIVES.map(p => (<button key={p} onClick={() => addNode(p)} aria-label={`Add ${p} to canvas`} style={{ padding: '5px', fontSize: '10px', cursor: 'pointer', background: '#fff', border: '1px solid #ccc', borderRadius: '4px' }}>{p}</button>))}
          </div>
        </div>
        <div style={{ flex: 1, background: '#f0f0f0' }}>
          <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onConnect={onConnect} nodeTypes={nodeTypes} fitView>
            <Background /><Controls />
          </ReactFlow>
        </div>
      </div>
    </div>
  );
}
