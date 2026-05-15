"use client";
import { useState } from "react";

export default function Dashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [language, setLanguage] = useState("Python");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setIsAnalyzing(true);
    
    // Simulate real-time API call to our new FastAPI endpoint
    setTimeout(() => {
      setIsAnalyzing(false);
      setResult({
        classes: [{ name: "ParserEngine" }, { name: "ASTNode" }],
        functions: [{ name: "parse_python" }, { name: "extract_dependencies" }],
      });
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-sans">
      <header className="border-b border-zinc-800 bg-zinc-900/50 p-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-white">Dev<span className="text-blue-500">Workspace</span></h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-8 grid md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-3xl font-black mb-6">Upload Codebase</h2>
          <form onSubmit={handleUpload} className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
            
            <div>
              <label className="block text-sm text-zinc-400 mb-2">Select Language Parser</label>
              <select 
                value={language} 
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full bg-zinc-950 border border-zinc-800 rounded-md p-3 text-white focus:outline-none focus:border-blue-500"
              >
                <option>Python</option>
                <option>Java</option>
                <option>JavaScript</option>
                <option>HTML</option>
                <option>CSS</option>
              </select>
            </div>

            <div>
              <label className="block text-sm text-zinc-400 mb-2">Upload Source File</label>
              <input 
                type="file" 
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="w-full text-zinc-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-500/10 file:text-blue-500 hover:file:bg-blue-500/20"
              />
            </div>

            <button 
              type="submit"
              disabled={!file || isAnalyzing}
              className={`w-full py-3 rounded-md font-bold transition-all ${isAnalyzing ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-500 text-white'}`}
            >
              {isAnalyzing ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-4 h-4 border-2 border-zinc-400 border-t-transparent rounded-full animate-spin"></div>
                  Parsing AST...
                </span>
              ) : "Analyze Architecture"}
            </button>
          </form>
        </div>

        <div>
          <h2 className="text-3xl font-black mb-6">Architecture Output</h2>
          {isAnalyzing && (
            <div className="h-64 flex flex-col items-center justify-center border-2 border-dashed border-zinc-800 rounded-xl">
              <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-zinc-400 font-mono animate-pulse">Running {language} Syntax Parser...</p>
            </div>
          )}
          
          {result && !isAnalyzing && (
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <div className="mb-6">
                <h3 className="text-green-400 font-mono mb-2">Detected Classes ({result.classes.length})</h3>
                <div className="flex gap-2 flex-wrap">
                  {result.classes.map((c: any, i: int) => (
                    <span key={i} className="px-3 py-1 bg-zinc-800 rounded-md text-sm text-zinc-300 border border-zinc-700">{c.name}</span>
                  ))}
                </div>
              </div>
              
              <div>
                <h3 className="text-blue-400 font-mono mb-2">Detected Functions ({result.functions.length})</h3>
                <div className="flex gap-2 flex-wrap">
                  {result.functions.map((f: any, i: int) => (
                    <span key={i} className="px-3 py-1 bg-zinc-800 rounded-md text-sm text-zinc-300 border border-zinc-700">{f.name}()</span>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
