import { useState } from "react";
import { uploadSalesFile } from "../services/api.js";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const selected = event.target.files && event.target.files[0];
    setFile(selected || null);
    setStatus(null);
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
    setStatus(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file || !email) {
      setStatus({ type: "error", message: "File and email are required." });
      return;
    }

    setLoading(true);
    setStatus(null);

    try {
      await uploadSalesFile({ file, email });
      setStatus({
        type: "success",
        message: "Summary generated and emailed successfully!",
      });
    } catch (error) {
      const message =
        error?.response?.data?.detail ||
        error?.message ||
        "Unexpected error while processing upload.";
      setStatus({ type: "error", message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="group relative bg-slate-900/60 backdrop-blur-xl border border-slate-700/40 rounded-3xl p-7 sm:p-9 animate-glow-pulse hover:border-slate-600/60 transition-colors duration-500"
    >
      <div className="absolute inset-0 rounded-3xl bg-shimmer animate-shimmer opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none" />

      <div className="relative z-10 space-y-6">
        <div>
          <label htmlFor="file" className="block text-sm font-medium text-slate-300 mb-2">
            Upload Sales File
          </label>
          <div className="relative">
            <input
              id="file"
              type="file"
              accept=".csv,.xlsx"
              onChange={handleFileChange}
              disabled={loading}
              className="block w-full text-sm text-slate-400 file:mr-4 file:py-2.5 file:px-5 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-slate-800 file:text-sky-400 hover:file:bg-slate-700 file:cursor-pointer file:transition-all file:duration-200 disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
            />
            {file && (
              <span className="mt-2 block text-xs text-slate-500 animate-slide-in truncate">
                Selected: {file.name}
              </span>
            )}
          </div>
        </div>

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
            Recipient Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={handleEmailChange}
            placeholder="you@example.com"
            disabled={loading}
            className="w-full px-4 py-3 rounded-xl border border-slate-700/60 bg-slate-800/50 text-slate-200 placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-sky-500/50 focus:border-sky-500/50 hover:border-slate-600 transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3.5 rounded-2xl btn-gradient text-white font-semibold text-sm tracking-wide shadow-lg shadow-sky-500/20 hover:shadow-sky-500/40 hover:-translate-y-0.5 hover:scale-[1.01] active:translate-y-0 active:scale-100 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:scale-100 disabled:hover:shadow-sky-500/20"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2.5">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Generating Summary...
            </span>
          ) : (
            <span className="flex items-center justify-center gap-2">
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Generate AI Summary
            </span>
          )}
        </button>

        <div className="min-h-[2rem]">
          {loading && (
            <div className="flex items-center gap-2 animate-slide-in">
              <div className="flex gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-sky-400 animate-bounce [animation-delay:0ms]" />
                <span className="h-1.5 w-1.5 rounded-full bg-sky-400 animate-bounce [animation-delay:150ms]" />
                <span className="h-1.5 w-1.5 rounded-full bg-sky-400 animate-bounce [animation-delay:300ms]" />
              </div>
              <p className="text-sm text-slate-400">
                Analyzing data and crafting your summary...
              </p>
            </div>
          )}
          {!loading && status?.type === "success" && (
            <div className="flex items-start gap-2 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 animate-slide-in">
              <svg className="h-5 w-5 text-emerald-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-emerald-300">{status.message}</p>
            </div>
          )}
          {!loading && status?.type === "error" && (
            <div className="flex items-start gap-2 p-3 rounded-xl bg-red-500/10 border border-red-500/20 animate-slide-in">
              <svg className="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-red-300">{status.message}</p>
            </div>
          )}
        </div>
      </div>
    </form>
  );
}

export default UploadForm;
