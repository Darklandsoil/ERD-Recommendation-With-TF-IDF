import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Download NLTK data if not available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

def get_stop_words():
    """Get Indonesian stop words"""
    return set(stopwords.words('indonesian'))

def normalize_erd_name(erd_name):
    """Normalize ERD name for consistent storage"""
    return erd_name.lower().replace(" ", "_")

def remove_stopwords(text):
    """Remove stopwords from text"""
    stop_words = get_stop_words()
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words and len(word) > 2]
    return " ".join(filtered_words)

def extract_erd_name(text):
    """Extract ERD name from query text"""
    text = text.lower()
    match = re.search(r"\berd\b\s*(.*)", text)
    if match:
        return normalize_erd_name(match.group(1).strip())
    return None