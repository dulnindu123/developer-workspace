export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-950 p-4">
      <div className="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-black text-white mb-2">Developer <span className="text-blue-500">Workspace</span></h1>
          <p className="text-zinc-400">Sign in to your architecture portal</p>
        </div>
        
        <form className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-2">Email Address</label>
            <input 
              type="email" 
              className="w-full px-4 py-3 bg-zinc-950 border border-zinc-800 rounded-lg text-white focus:outline-none focus:border-blue-500 transition-colors"
              placeholder="developer@example.com"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-2">Password</label>
            <input 
              type="password" 
              className="w-full px-4 py-3 bg-zinc-950 border border-zinc-800 rounded-lg text-white focus:outline-none focus:border-blue-500 transition-colors"
              placeholder="••••••••"
            />
          </div>
          
          <button 
            type="button"
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition-colors"
          >
            Authenticate
          </button>
        </form>
        
        <div className="mt-8 text-center text-sm text-zinc-500">
          <p>Or continue with <a href="#" className="text-blue-400 hover:text-blue-300">GitHub OAuth</a></p>
        </div>
      </div>
    </div>
  );
}
