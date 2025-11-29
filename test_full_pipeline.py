"""
Test full pipeline untuk memahami kenapa 'kembali' tidak match dengan 'Pengembalian'
"""
from utils.text_processing import (
    advanced_normalize_text,
    remove_stopwords,
    stem_indonesian
)

print("=" * 80)
print("TEST FULL PIPELINE: Query 'kembali' vs Atribut 'Pengembalian'")
print("=" * 80)

# Simulasi data dari database
database_attributes = [
    "Pengembalian",
    "Tanggal_Pengembalian",
    "Status_Pengembalian",
    "ID_Peminjaman",
    "Nama_Peminjam",
]

# Simulasi query user
user_queries = [
    "kembali",
    "pengembalian",
    "pinjam",
    "peminjaman",
]

print("\n1. NORMALISASI ATRIBUT DATABASE")
print("-" * 80)
print(f"{'Atribut Asli':<30} {'Setelah advanced_normalize_text':<40}")
print("-" * 80)

normalized_db_attrs = {}
for attr in database_attributes:
    normalized = advanced_normalize_text(attr)
    normalized_db_attrs[attr] = normalized
    print(f"{attr:<30} {normalized:<40}")

print("\n2. NORMALISASI QUERY USER")
print("-" * 80)
print(f"{'Query User':<30} {'Setelah advanced_normalize_text':<40}")
print("-" * 80)

normalized_queries = {}
for query in user_queries:
    normalized = advanced_normalize_text(query)
    normalized_queries[query] = normalized
    print(f"{query:<30} {normalized:<40}")

print("\n3. STOPWORDS REMOVAL")
print("-" * 80)
print(f"{'Text':<40} {'Setelah remove_stopwords':<40}")
print("-" * 80)

# Test stopwords removal pada hasil normalisasi
for query, normalized in normalized_queries.items():
    after_stopwords = remove_stopwords(normalized)
    print(f"{normalized:<40} {after_stopwords:<40}")

print("\n4. ANALISIS MATCHING")
print("-" * 80)
print("Apakah query 'kembali' akan match dengan atribut 'Pengembalian'?")
print("-" * 80)

query_kembali_normalized = normalized_queries["kembali"]
attr_pengembalian_normalized = normalized_db_attrs["Pengembalian"]

print(f"\nQuery 'kembali' setelah normalisasi: '{query_kembali_normalized}'")
print(f"Atribut 'Pengembalian' setelah normalisasi: '{attr_pengembalian_normalized}'")
print(f"\nApakah sama? {query_kembali_normalized == attr_pengembalian_normalized}")

# Test dengan stopwords removal
query_after_stopwords = remove_stopwords(query_kembali_normalized)
attr_after_stopwords = remove_stopwords(attr_pengembalian_normalized)

print(f"\nQuery 'kembali' setelah stopwords removal: '{query_after_stopwords}'")
print(f"Atribut 'Pengembalian' setelah stopwords removal: '{attr_after_stopwords}'")
print(f"\nApakah sama? {query_after_stopwords == attr_after_stopwords}")

print("\n" + "=" * 80)
print("5. MINIMUM WORD LENGTH CHECK (> 2 characters)")
print("-" * 80)

test_words = ["kembali", "id", "no", "nim", "ipk"]
print(f"{'Kata':<20} {'Panjang':<10} {'Pass Filter (>2)?':<20}")
print("-" * 80)
for word in test_words:
    length = len(word)
    passes = "YES" if length > 2 else "NO (FILTERED OUT!)"
    print(f"{word:<20} {length:<10} {passes:<20}")

print("\n" + "=" * 80)
print("KESIMPULAN:")
print("=" * 80)
print("""
Berdasarkan test di atas, kemungkinan penyebab masalah:

1. STOPWORDS REMOVAL yang terlalu agresif
   - Jika 'kembali' dianggap stopword, akan dihapus!
   
2. MINIMUM WORD LENGTH filter (> 2 characters)
   - Kata pendek seperti 'id', 'no' akan difilter
   - Tapi 'kembali' (7 karakter) seharusnya aman
   
3. TF-IDF SCORING yang rendah
   - Jika banyak dokumen punya kata 'kembali', IDF-nya kecil
   - Similarity score bisa jadi terlalu rendah (< threshold)

REKOMENDASI DEBUG:
- Cek apakah 'kembali' ada di stopwords list
- Cek threshold similarity (min_similarity)
- Cek apakah ada dokumen ERD yang match tapi score-nya < threshold
""")

print("\n6. CEK STOPWORDS LIST")
print("-" * 80)
from utils.text_processing import get_stop_words
stopwords = get_stop_words()

test_check = ["kembali", "pengembalian", "pinjam", "mahasiswa", "dosen"]
print(f"{'Kata':<20} {'Ada di Stopwords?':<20}")
print("-" * 80)
for word in test_check:
    is_stopword = "YES (PROBLEM!)" if word in stopwords else "NO (OK)"
    print(f"{word:<20} {is_stopword:<20}")
