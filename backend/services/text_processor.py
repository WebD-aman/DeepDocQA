import re

_nltk = None
_nltk_checked = False


def get_nltk():
    global _nltk, _nltk_checked
    if _nltk_checked:
        return _nltk

    _nltk_checked = True
    try:
        import nltk
    except Exception:
        _nltk = None
    else:
        _nltk = nltk

    return _nltk


def ensure_nltk_data():
    nltk = get_nltk()
    if nltk is None:
        return False

    try:
        nltk.data.find("tokenizers/punkt")
        return True
    except LookupError:
        return False


def clean_text(text):
    text = text.replace("\x00", " ")
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)
    text = re.sub(r"\s+", " ", text)
    return normalize_spacing(text)


def normalize_spacing(text):
    text = re.sub(r"\s+([,.;:!?%)\]])", r"\1", text)
    text = re.sub(r"([(])\s+", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def split_sentences(text):
    try:
        if ensure_nltk_data():
            sentences = nltk.sent_tokenize(text)
        else:
            sentences = re.split(r"(?<=[.!?])\s+", text)
    except Exception:
        # Offline-safe fallback for demos where NLTK data cannot be downloaded.
        sentences = re.split(r"(?<=[.!?])\s+", text)

    return [sentence.strip() for sentence in sentences if sentence.strip()]


def format_readable_answer(text):
    cleaned = clean_text(text)
    sentences = split_sentences(cleaned)

    if not sentences:
        return cleaned

    if len(sentences) == 1:
        return sentences[0]

    paragraphs = []
    current = []
    current_words = 0

    for sentence in sentences:
        word_count = len(sentence.split())
        if current and current_words + word_count > 55:
            paragraphs.append(" ".join(current))
            current = []
            current_words = 0

        current.append(sentence)
        current_words += word_count

    if current:
        paragraphs.append(" ".join(current))

    return "\n\n".join(paragraphs)
