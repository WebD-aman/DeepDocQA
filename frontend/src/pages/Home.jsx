import { useEffect, useState } from "react";

import { askQuestion, getStatus, uploadDocument } from "../api.js";
import ChatBox from "../components/ChatBox.jsx";
import Navbar from "../components/Navbar.jsx";
import UploadCard from "../components/UploadCard.jsx";

export default function Home() {
  const [currentDocument, setCurrentDocument] = useState("");
  const [answers, setAnswers] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getStatus()
      .then((response) => setCurrentDocument(response.data.current_document || ""))
      .catch(() => setError("Backend is not reachable. Start Flask on port 5000."));
  }, []);

  const handleUpload = async (file) => {
    setUploading(true);
    setError("");
    try {
      const response = await uploadDocument(file);
      setCurrentDocument(response.data.current_document);
      setAnswers([]);
    } catch (err) {
      setError(err.response?.data?.error || "Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const handleAsk = async (question) => {
    setAsking(true);
    setError("");
    try {
      const response = await askQuestion(question);
      setAnswers((items) => [
        {
          id: crypto.randomUUID(),
          question,
          ...response.data
        },
        ...items
      ]);
    } catch (err) {
      setError(err.response?.data?.error || "Could not answer the question.");
    } finally {
      setAsking(false);
    }
  };

  return (
    <main className="app-shell">
      <Navbar currentDocument={currentDocument} />

      {error && <div className="error-banner">{error}</div>}

      <div className="workspace-grid">
        <UploadCard currentDocument={currentDocument} onUpload={handleUpload} loading={uploading} />
        <ChatBox currentDocument={currentDocument} onAsk={handleAsk} answers={answers} loading={asking} />
      </div>
    </main>
  );
}
