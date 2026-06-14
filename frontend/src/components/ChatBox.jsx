import { useState } from "react";

import AnswerCard from "./AnswerCard.jsx";
import Loader from "./Loader.jsx";

export default function ChatBox({ currentDocument, onAsk, answers, loading }) {
  const [question, setQuestion] = useState("");

  const submit = (event) => {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed || loading) return;
    onAsk(trimmed);
    setQuestion("");
  };

  return (
    <section className="panel chat-panel">
      <div className="section-heading">
        <p className="eyebrow">Question Answering</p>
        <h2>Ask from the current document</h2>
      </div>

      <form className="ask-form" onSubmit={submit}>
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder={currentDocument ? "Ask a question about the uploaded document" : "Upload a document first"}
          disabled={!currentDocument || loading}
        />
        <button className="primary-button" disabled={!currentDocument || !question.trim() || loading}>
          Ask
        </button>
      </form>

      {loading && <Loader label="Finding the most relevant chunk" />}

      <div className="conversation">
        {answers.length === 0 ? (
          <div className="empty-state">Answers will appear here with confidence scores and timestamps.</div>
        ) : (
          answers.map((item) => <AnswerCard key={item.id} item={item} />)
        )}
      </div>
    </section>
  );
}
