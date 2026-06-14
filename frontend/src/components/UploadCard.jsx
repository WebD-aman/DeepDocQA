import { useRef, useState } from "react";

import Loader from "./Loader.jsx";

export default function UploadCard({ currentDocument, onUpload, loading }) {
  const inputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragging, setDragging] = useState(false);

  const chooseFile = (file) => {
    if (file) {
      setSelectedFile(file);
    }
  };

  const submit = () => {
    if (selectedFile && !loading) {
      onUpload(selectedFile);
    }
  };

  return (
    <section className="panel upload-panel">
      <div className="section-heading">
        <p className="eyebrow">Document Upload</p>
        <h2>One active source at a time</h2>
      </div>

      <div
        className={`drop-zone ${dragging ? "dragging" : ""}`}
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragging(false);
          chooseFile(event.dataTransfer.files[0]);
        }}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt,.docx"
          onChange={(event) => chooseFile(event.target.files[0])}
          hidden
        />
        <div className="upload-icon">DOC</div>
        <strong>Drop a PDF, TXT, or DOCX file here</strong>
        <span>or click to browse from your laptop</span>
      </div>

      <div className="file-meta">
        <span>Selected: {selectedFile?.name || "None"}</span>
        <span>Active: {currentDocument || "None"}</span>
      </div>

      <button className="primary-button" onClick={submit} disabled={!selectedFile || loading}>
        Upload and Process
      </button>

      {loading && <Loader label="Reading and embedding document" />}
    </section>
  );
}
