import UploadForm from "./components/UploadForm.jsx";

function App() {
  return (
    <div className="relative min-h-screen bg-[#030712] flex flex-col items-center px-4 py-14 sm:py-20 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_rgba(56,189,248,0.08)_0%,_transparent_50%)] pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_right,_rgba(99,102,241,0.06)_0%,_transparent_50%)] pointer-events-none" />

      <header className="relative z-10 max-w-2xl text-center mb-12 animate-fade-in-up">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-slate-700/50 bg-slate-800/40 backdrop-blur-sm text-xs font-medium text-slate-400 mb-6">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-sky-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-sky-500" />
          </span>
          AI-Powered Sales Analytics
        </div>
        <h1 className="text-5xl sm:text-6xl font-extrabold tracking-tight mb-4">
          <span className="text-white">Sales Insight</span>
          <br />
          <span className="text-gradient">Automator</span>
        </h1>
        <p className="text-slate-400 text-lg leading-relaxed max-w-lg mx-auto">
          Upload a sales dataset and receive an AI-generated executive summary delivered straight to your inbox.
        </p>
      </header>

      <main className="relative z-10 w-full max-w-lg animate-fade-in-up-delay">
        <UploadForm />
      </main>

      <footer className="relative z-10 mt-auto pt-16 animate-fade-in-up-delay-2">
        <div className="flex items-center gap-3 text-slate-600 text-xs">
          <span className="h-px w-8 bg-slate-700/50" />
          Powered by Groq &middot; FastAPI &middot; React
          <span className="h-px w-8 bg-slate-700/50" />
        </div>
      </footer>
    </div>
  );
}

export default App;
