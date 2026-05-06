export default function Dashboard() {
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-sans">
      <header className="border-b border-zinc-800 bg-zinc-900/50 p-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-white">Dev<span className="text-blue-500">Workspace</span></h1>
          <div className="flex gap-4">
            <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-md font-semibold text-sm transition-colors">
              New Project
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-8">
        <h2 className="text-3xl font-black mb-8">My Architecture Hub</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Mock Project Card */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 hover:border-zinc-700 transition-colors cursor-pointer group">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-white group-hover:text-blue-400 transition-colors">Smart Campus API</h3>
              <span className="px-2 py-1 bg-green-500/10 text-green-400 text-xs rounded-full font-mono">Analyzed</span>
            </div>
            <p className="text-zinc-400 text-sm mb-6">REST API for telemetry and metadata management.</p>
            <div className="flex justify-between items-center text-xs text-zinc-500 font-mono">
              <span>24 Classes</span>
              <span>Updated 2h ago</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
