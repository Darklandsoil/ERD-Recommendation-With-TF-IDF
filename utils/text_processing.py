import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Download NLTK data if not available
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Initialize Indonesian Stemmer
_stemmer_factory = StemmerFactory()
_stemmer = _stemmer_factory.create_stemmer()

def get_stop_words():
    """
    Get Indonesian stop words with custom filtering for ERD domain
    
    Removes common stopwords that don't carry meaning, but preserves
    domain-specific words that are important for ERD search (e.g., 'kembali', 'ambil', 'simpan')
    """
    # Get default Indonesian stopwords from NLTK
    default_stopwords = set(stopwords.words('indonesian'))
    
    # Whitelist: Domain-specific words that should NOT be removed
    # These are important for ERD context (actions, operations, entities)
    domain_whitelist = {
        'kembali', 'ambil', 'simpan', 'hapus', 'ubah', 'tambah',
        'buat', 'lihat', 'cari', 'cetak', 'kirim', 'terima',
        'masuk', 'keluar', 'login', 'logout', 'daftar', 'bayar',
        'pinjam', 'ganti', 'update', 'delete', 'insert', 'select',
        'baca', 'tulis', 'edit', 'input', 'output', 'proses',
    }
    
    # Remove domain-specific words from stopwords
    custom_stopwords = default_stopwords - domain_whitelist
    
    return custom_stopwords

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

# ============================================
# FASE 1: ADVANCED TEXT PROCESSING
# ============================================

def split_camelcase(text):
    """
    Split CamelCase and camelCase words into separate words while preserving acronyms
    
    Examples:
        'MataKuliah' -> 'Mata Kuliah'
        'userId' -> 'user Id'
        'IPKMahasiswa' -> 'IPK Mahasiswa'
        'BKDD' -> 'BKDD' (preserved, not split)
        'XMLParser' -> 'XML Parser'
        'NIMSiswa' -> 'NIM Siswa'
    
    Algorithm:
        - Don't split consecutive uppercase letters (acronyms): BKDD stays BKDD
        - Split between lowercase and uppercase: camelCase -> camel Case
        - Split at end of acronym before lowercase: XMLParser -> XML Parser
    """
    if not isinstance(text, str):
        return text
    
    # Improved regex that preserves acronyms:
    # 1. (?<=[a-z])(?=[A-Z]) - Split between lowercase and uppercase (camelCase)
    # 2. (?<=[A-Z])(?=[A-Z][a-z]) - Split before last letter of acronym (XMLParser -> XML Parser)
    result = re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', ' ', text)
    return result

def remove_special_characters(text):
    """
    Remove special characters and punctuation, keep only alphanumeric and spaces
    Examples:
        'Mata-Kuliah' -> 'Mata Kuliah'
        'No.Telepon' -> 'No Telepon'
        'Email@Address' -> 'Email Address'
    """
    if not isinstance(text, str):
        return text
    
    # Keep only letters, numbers, and spaces
    # Also handles underscore replacement
    text = text.replace('_', ' ')
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text

def normalize_whitespace(text):
    """
    Normalize multiple whitespaces to single space and strip leading/trailing spaces
    Examples:
        'Mata  Kuliah' -> 'Mata Kuliah'
        '  ID   Dosen  ' -> 'ID Dosen'
    """
    if not isinstance(text, str):
        return text
    
    # Replace multiple spaces/tabs/newlines with single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading and trailing spaces
    text = text.strip()
    return text

def stem_indonesian(text):
    """
    Apply Indonesian stemming using Sastrawi
    Examples:
        'pembelajaran' -> 'ajar'
        'kemahasiswaan' -> 'mahasiswa'
        'perkuliahan' -> 'kuliah'
    """
    if not isinstance(text, str):
        return text
    
    # Stem the text
    stemmed = _stemmer.stem(text)
    return stemmed

def advanced_normalize_text(text):
    """
    Apply all Phase 1 text processing techniques in optimal order:
    1. CamelCase splitting
    2. Special characters removal (includes underscore -> space)
    3. Whitespace normalization
    4. Lowercase conversion
    5. Indonesian stemming
    
    Examples:
        'MataKuliah' -> 'mata kuliah' -> 'kuliah' (after stemming)
        'Nilai_Pembelajaran' -> 'nilai ajar'
        'No.Telepon' -> 'no telepon'
    """
    if not isinstance(text, str):
        return text
    
    # Step 1: Split CamelCase
    text = split_camelcase(text)
    
    # Step 2: Remove special characters (also handles underscores)
    text = remove_special_characters(text)
    
    # Step 3: Normalize whitespace
    text = normalize_whitespace(text)
    
    # Step 4: Convert to lowercase
    text = text.lower()
    
    # Step 5: Apply stemming
    text = stem_indonesian(text)
    
    return text