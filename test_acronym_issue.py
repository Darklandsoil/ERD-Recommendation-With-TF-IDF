"""
Test untuk menginvestigasi masalah dengan akronim seperti BKDD
"""
from utils.text_processing import (
    split_camelcase,
    advanced_normalize_text,
    remove_stopwords
)

print("=" * 80)
print("INVESTIGASI MASALAH AKRONIM (BKDD, IPK, NIM, dll)")
print("=" * 80)

# Test cases dengan akronim
test_cases = [
    "verifikasi BKDD",
    "Verifikasi_BKDD",
    "VerifikasiBKDD",
    "BKDD",
    "IPK",
    "NIM",
    "IPKMahasiswa",
    "NIMSiswa",
    "StatusBKDD",
]

print("\n1. TEST SPLIT CAMELCASE (Masalah di sini)")
print("-" * 80)
print(f"{'Input':<30} {'After split_camelcase':<40}")
print("-" * 80)

for test in test_cases:
    result = split_camelcase(test)
    print(f"{test:<30} {result:<40}")

print("\n2. TEST ADVANCED NORMALIZE TEXT (Full pipeline)")
print("-" * 80)
print(f"{'Input':<30} {'After advanced_normalize_text':<40}")
print("-" * 80)

for test in test_cases:
    result = advanced_normalize_text(test)
    print(f"{test:<30} {result:<40}")

print("\n3. ANALISIS SPESIFIK: 'verifikasi BKDD' vs query 'BKDD'")
print("-" * 80)

# Atribut di database
attr_db = "Verifikasi_BKDD"
print(f"Database Attribute: '{attr_db}'")
result_db = advanced_normalize_text(attr_db)
print(f"After normalization: '{result_db}'")
result_db_stopwords = remove_stopwords(result_db)
print(f"After stopwords removal: '{result_db_stopwords}'")

print()

# Query user: "verifikasi"
query1 = "verifikasi"
print(f"User Query 1: '{query1}'")
result_q1 = advanced_normalize_text(query1)
print(f"After normalization: '{result_q1}'")
result_q1_stopwords = remove_stopwords(result_q1)
print(f"After stopwords removal: '{result_q1_stopwords}'")
print(f"Match with DB? Contains '{result_q1_stopwords}' in '{result_db_stopwords}': {result_q1_stopwords in result_db_stopwords}")

print()

# Query user: "BKDD"
query2 = "BKDD"
print(f"User Query 2: '{query2}'")
result_q2 = advanced_normalize_text(query2)
print(f"After normalization: '{result_q2}'")
result_q2_stopwords = remove_stopwords(result_q2)
print(f"After stopwords removal: '{result_q2_stopwords}'")
print(f"Match with DB? Contains '{result_q2_stopwords}' in '{result_db_stopwords}': {result_q2_stopwords in result_db_stopwords}")

print("\n" + "=" * 80)
print("ANALISIS MASALAH:")
print("-" * 80)
print("""
Regex saat ini: r'(?<!^)(?=[A-Z])'
Ini akan insert space SEBELUM SETIAP huruf kapital (kecuali di awal)

Contoh:
- "BKDD" -> "B K D D" (SALAH! Akronim dipecah)
- "IPKMahasiswa" -> "I P K Mahasiswa" (SALAH! IPK dipecah)
- "NIM" -> "N I M" (SALAH! Akronim dipecah)

Setelah tokenization dengan filter length > 2:
- "B K D D" -> semua dihapus (setiap huruf < 3 karakter)
- Query "BKDD" menjadi KOSONG!

SOLUSI:
Perbaiki regex untuk:
1. TIDAK split consecutive uppercase (akronim): BKDD tetap BKDD
2. Split lowercase ke uppercase: camelCase -> camel Case
3. Split uppercase ke lowercase (akhir akronim): XMLParser -> XML Parser
""")

print("\n4. TEST TOKENIZATION & LENGTH FILTER")
print("-" * 80)
from nltk.tokenize import word_tokenize

problematic = ["B K D D", "I P K", "N I M"]
print(f"{'Token String':<30} {'After tokenize':<30} {'After len>2 filter':<30}")
print("-" * 80)

for text in problematic:
    tokens = word_tokenize(text)
    filtered = [w for w in tokens if len(w) > 2]
    print(f"{text:<30} {str(tokens):<30} {str(filtered):<30}")

print("\n" + "=" * 80)
print("KESIMPULAN:")
print("Regex split_camelcase harus diperbaiki untuk preserve akronim!")
print("=" * 80)
