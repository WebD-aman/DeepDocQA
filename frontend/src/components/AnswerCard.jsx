export default function AnswerCard({ item }) {
  const timestamp = item.timestamp ? new Date(item.timestamp).toLocaleString() : "";
  const paragraphs = String(item.answer || "")
    .split(/\n{2,}/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);

  return (
    <article className="answer-card">
      <div className="question-bubble">{item.question}</div>
      <div className="answer-body">
        <div className="answer-header">
          <strong>Answer</strong>
        </div>
        <div className="answer-text">
          {paragraphs.map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>
        <time>{timestamp}</time>
      </div>
    </article>
  );
}
