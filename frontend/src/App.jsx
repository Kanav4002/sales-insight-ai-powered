import UploadForm from "./components/UploadForm.jsx";

function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>Sales Insight Automator</h1>
        <p>Upload a sales dataset and deliver an AI-generated executive summary by email.</p>
      </header>
      <main className="app-main">
        <UploadForm />
      </main>
    </div>
  );
}

export default App;

