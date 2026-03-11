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
        message: "Summary generated and emailed to the recipient."
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
    <form className="card" onSubmit={handleSubmit}>
      <div className="field-group">
        <label htmlFor="file">Upload Sales File</label>
        <input
          id="file"
          type="file"
          accept=".csv,.xlsx"
          onChange={handleFileChange}
          disabled={loading}
        />
      </div>

      <div className="field-group">
        <label htmlFor="email">Recipient Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={handleEmailChange}
          placeholder="you@example.com"
          disabled={loading}
        />
      </div>

      <button type="submit" className="primary-button" disabled={loading}>
        {loading ? "Processing..." : "Generate AI Summary"}
      </button>

      <div className="status-area">
        {loading && <p className="status-text">Processing upload and generating summary...</p>}
        {!loading && status?.type === "success" && (
          <p className="status-text success">{status.message}</p>
        )}
        {!loading && status?.type === "error" && (
          <p className="status-text error">{status.message}</p>
        )}
      </div>
    </form>
  );
}

export default UploadForm;

