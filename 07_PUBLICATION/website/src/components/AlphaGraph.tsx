import React, { useState, useCallback, useEffect } from 'react';
import ReactFlow, { 
  Background, Controls, applyNodeChanges, applyEdgeChanges, 
  Node, Edge, NodeChange, EdgeChange, Handle, Position 
} from 'reactflow';
import 'reactflow/dist/style.css';

const SONIFICATION: Record<string, {freq: number, type: OscillatorType}> = {
  "EXIST": { freq: 440, type: "sine" }, "CAUSE": { freq: 330, type: "triangle" }, "PART": { freq: 523, type: "sine" },
  "SAME": { freq: 440, type: "sine" }, "ONE": { freq: 659, type: "sine" }, "ALL": { freq: 554, type: "square" },
  "NOT": { freq: 220, type: "sawtooth" }, "IF": { freq: 392, type: "sine" }, "DO": { freq: 349, type: "sine" },
  "HAPPEN": { freq: 294, type: "sine" }, "KNOW": { freq: 587, type: "sine" }, "SEE": { freq: 880, type: "sine" },
  "BIG": { freq: 110, type: "sine" }, "LIVE": { freq: 330, type: "triangle" }, "DIE": { freq: 165, type: "sawtooth" },
  "MOVE": { freq: 440, type: "sine" }, "THINK": { freq: 523, type: "sine" }, "SAY": { freq: 392, type: "square" },
  "TRUE": { freq: 659, type: "sine" }, "GOOD": { freq: 784, type: "sine" },
};
const PRIMITIVES = Object.keys(SONIFICATION);

let audioCtx: AudioContext | null = null;
const playSound = (name: string) => {
  if (!audioCtx) audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
  if (audioCtx.state === 'suspended') audioCtx.resume();
  const cfg = SONIFICATION[name];
  if (!cfg) return;
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

const PrimitiveNode = ({ data }: any) => (
  <div onClick={() => playSound(data.label)} style={{ padding: '10px 15px', border: '2px solid #17becf', borderRadius: '8px', background: '#fff', fontWeight: 'bold', color: '#1a1a2e', textAlign: 'center', cursor: 'pointer', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
    <Handle type="target" position={Position.Left} style={{ background: '#555' }} />
    {data.label}
    <Handle type="source" position={Position.Right} style={{ background: '#555' }} />
  </div>
);
const nodeTypes = { primitive: PrimitiveNode };

export default function AlphaGraph() {
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

  // --- NOUVEAU : Écouter le Tuteur IA ---
  useEffect(() => {
    const handleTutorExpression = (e: any) => {
      const expr = e.detail; // e.g., "MOVE(particle, 0, 10) AND BIG(10, 0)"
      setCompiledCode(expr);
      
      // Extraire les primitives (ex: MOVE, BIG)
      const matches = expr.match(/([A-Z]+)\(/g);
      if (matches) {
        const prims = matches.map((m: string) => m.replace('(', ''));
        const newNodes: Node[] = prims.map((p: string, i: number) => ({
          id: `node_ai_${Date.now()}_${i}`,
          type: 'primitive',
          position: { x: 100 + (i % 3) * 150, y: 100 + Math.floor(i / 3) * 100 },
          data: { label: p }
        }));
        
        // Connecter les nœuds en série pour le visuel
        const newEdges: Edge[] = [];
        for (let i = 0; i < newNodes.length - 1; i++) {
          newEdges.push({ id: `e_${i}`, source: newNodes[i].id, target: newNodes[i+1].id, animated: true });
        }
        
        setNodes(newNodes);
        setEdges(newEdges);
        
        // Jouer les sons
        prims.forEach((p: string, i: number) => setTimeout(() => playSound(p), i * 500));
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
    nodes.forEach((n) => { setTimeout(() => playSound(n.data.label), delay); delay += 600; });
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '650px', border: '1px solid #ddd', borderRadius: '8px', overflow: 'hidden' }}>
      <div style={{ padding: '10px', background: '#1a1a2e', color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ fontFamily: 'monospace', fontSize: '12px' }}>{compiledCode ? `Expression: ${compiledCode}` : "Draw a graph to generate Alpha-20 code..."}</span>
        <button onClick={compileGraph} style={{ padding: '8px 16px', background: '#2ca02c', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>▶ Compile & Play</button>
      </div>
      <div style={{ display: 'flex', flex: 1 }}>
        <div style={{ width: '200px', background: '#fafafa', borderRight: '1px solid #ddd', padding: '10px', overflowY: 'auto' }}>
          <h3 style={{ fontSize: '14px', marginBottom: '10px' }}>Palette</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '5px' }}>
            {PRIMITIVES.map(p => (<button key={p} onClick={() => addNode(p)} style={{ padding: '5px', fontSize: '10px', cursor: 'pointer', background: '#fff', border: '1px solid #ccc', borderRadius: '4px' }}>{p}</button>))}
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
