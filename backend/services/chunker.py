from services.text_processor import split_sentences


def chunk_text(text, max_words=120, overlap_sentences=1):
    sentences = split_sentences(text)
    chunks = []
    current = []
    current_words = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        if current and current_words + word_count > max_words:
            chunks.append(" ".join(current).strip())
            current = current[-overlap_sentences:] if overlap_sentences > 0 else []
            current_words = sum(len(item.split()) for item in current)

        current.append(sentence)
        current_words += word_count

    if current:
        chunks.append(" ".join(current).strip())

    return chunks
