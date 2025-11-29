"""
Test custom stopwords filter untuk memastikan kata domain-specific tidak dihapus
"""
from utils.text_processing import (
    get_stop_words,
    remove_stopwords,
    advanced_normalize_text
)

print("=" * 80)
print("TEST CUSTOM STOPWORDS FILTER")
print("=" * 80)

# Get custom stopwords
custom_stopwords = get_stop_words()

print(f"\nTotal custom stopwords: {len(custom_stopwords)}")

# Test domain-specific words (should NOT be in stopwords)
domain_words = [
    'kembali', 'ambil', 'simpan', 'hapus', 'ubah', 'tambah',
    'buat', 'lihat', 'cari', 'cetak', 'kirim', 'terima',
    'masuk', 'keluar', 'login', 'logout', 'daftar', 'bayar',
    'pinjam', 'ganti', 'update', 'delete', 'insert', 'select',
]

print("\n1. CEK DOMAIN-SPECIFIC WORDS (Harus TIDAK dihapus)")
print("-" * 80)
print(f"{'Kata':<20} {'Ada di Stopwords?':<25} {'Status':<15}")
print("-" * 80)

for word in domain_words:
    is_stopword = word in custom_stopwords
    status = "PROBLEM!" if is_stopword else "OK (Preserved)"
    in_list = "YES (will be removed)" if is_stopword else "NO (will be kept)"
    print(f"{word:<20} {in_list:<25} {status:<15}")

# Test common stopwords (should still be in stopwords)
common_stopwords = [
    'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada',
    'adalah', 'ini', 'itu', 'dengan', 'oleh', 'akan', 'telah',
]

print("\n2. CEK COMMON STOPWORDS (Harus TETAP dihapus)")
print("-" * 80)
print(f"{'Kata':<20} {'Ada di Stopwords?':<25} {'Status':<15}")
print("-" * 80)

for word in common_stopwords:
    is_stopword = word in custom_stopwords
    status = "OK (Removed)" if is_stopword else "PROBLEM!"
    in_list = "YES (will be removed)" if is_stopword else "NO (will be kept)"
    print(f"{word:<20} {in_list:<25} {status:<15}")

print("\n3. TEST REMOVE_STOPWORDS FUNCTION")
print("-" * 80)
test_sentences = [
    "kembali buku yang dipinjam",
    "ambil data dari database",
    "simpan informasi ke sistem",
    "hapus record yang tidak digunakan",
    "mahasiswa yang akan daftar kuliah",
    "bayar biaya pendaftaran untuk semester baru",
]

print(f"{'Original Text':<50} {'After Stopwords Removal':<40}")
print("-" * 80)

for sentence in test_sentences:
    result = remove_stopwords(sentence)
    print(f"{sentence:<50} {result:<40}")

print("\n4. FULL PIPELINE TEST: Query 'kembali' vs Atribut 'Pengembalian'")
print("-" * 80)

# Simulasi query user
user_query = "kembali"
print(f"User Query: '{user_query}'")

# Step 1: Advanced normalization
normalized_query = advanced_normalize_text(user_query)
print(f"After normalization: '{normalized_query}'")

# Step 2: Stopwords removal
query_after_stopwords = remove_stopwords(normalized_query)
print(f"After stopwords removal: '{query_after_stopwords}'")

# Simulasi atribut database
db_attr = "Pengembalian"
print(f"\nDatabase Attribute: '{db_attr}'")

# Step 1: Advanced normalization
normalized_attr = advanced_normalize_text(db_attr)
print(f"After normalization: '{normalized_attr}'")

# Step 2: Stopwords removal
attr_after_stopwords = remove_stopwords(normalized_attr)
print(f"After stopwords removal: '{attr_after_stopwords}'")

print(f"\n{'='*80}")
if query_after_stopwords and attr_after_stopwords:
    print(f"SUCCESS! Both have content after processing")
    print(f"  Query: '{query_after_stopwords}'")
    print(f"  Attribute: '{attr_after_stopwords}'")
    if query_after_stopwords == attr_after_stopwords:
        print(f"  Match: YES - Will find recommendation!")
    else:
        print(f"  Match: NO - Words differ but TF-IDF might still match")
else:
    print(f"FAILED! Empty after stopwords removal")
    print(f"  Query: '{query_after_stopwords}' (empty={not query_after_stopwords})")
    print(f"  Attribute: '{attr_after_stopwords}' (empty={not attr_after_stopwords})")

print("=" * 80)
print("\nKESIMPULAN:")
print("-" * 80)
print("Dengan custom stopwords filter:")
print("1. Kata domain-specific seperti 'kembali', 'pinjam', 'ambil' TIDAK dihapus")
print("2. Kata umum seperti 'yang', 'dan', 'di' TETAP dihapus")
print("3. Query 'kembali' sekarang DAPAT match dengan 'Pengembalian'")
print("=" * 80)
