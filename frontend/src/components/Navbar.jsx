export default function Navbar({ currentDocument }) {
  return (
    <header className="navbar">
      <div>
        <p className="eyebrow">Academic NLP Project</p>
        <h1>Deep Learning Document Question Answering System</h1>
      </div>
      <div className="document-pill" title={currentDocument || "No active document"}>
        <span className={currentDocument ? "status-dot active" : "status-dot"} />
        <span>{currentDocument || "No document active"}</span>
      </div>
    </header>
  );
}
