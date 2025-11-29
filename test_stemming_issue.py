"""
Test untuk menginvestigasi issue stemming pada kata 'pengembalian'
"""
from utils.text_processing import stem_indonesian, advanced_normalize_text

print("=" * 80)
print("INVESTIGASI STEMMING ISSUE")
print("=" * 80)

# Test kata-kata yang berhasil dan yang tidak
test_words = [
    # Yang berhasil
    ("kemahasiswaan", "mahasiswa"),
    ("peminjaman", "pinjam"),
    ("pembelajaran", "ajar"),
    ("perkuliahan", "kuliah"),
    ("pendaftaran", "daftar"),
    
    # Yang bermasalah
    ("pengembalian", "kembali"),
    
    # Variasi kata 'kembali'
    ("kembali", "kembali"),
    ("mengembalikan", "kembali"),
    ("dikembalikan", "kembali"),
    ("pengembalian", "kembali"),
    
    # Test kata lain yang mungkin bermasalah
    ("pengambilan", "ambil"),
    ("pemberitahuan", "berita"),
    ("penghapusan", "hapus"),
]

print("\nHASIL STEMMING:")
print("-" * 80)
print(f"{'Kata Asli':<25} {'Harapan':<20} {'Hasil Stemming':<20} {'Match?':<10}")
print("-" * 80)

for word, expected in test_words:
    result = stem_indonesian(word)
    match = "YES" if result == expected else "NO"
    print(f"{word:<25} {expected:<20} {result:<20} {match:<10}")

print("\n" + "=" * 80)
print("ANALISIS SPESIFIK: kata 'pengembalian' dan variasinya")
print("=" * 80)

kembali_variants = [
    "kembali",
    "mengembalikan", 
    "dikembalikan",
    "pengembalian",
    "kembalian",
    "balik",
    "membalik",
]

print("\nHasil stemming untuk variasi 'kembali':")
for word in kembali_variants:
    result = stem_indonesian(word)
    print(f"  {word:<20} -> {result}")

print("\n" + "=" * 80)
print("KESIMPULAN:")
print("=" * 80)
print("""
Jika 'pengembalian' tidak menjadi 'kembali', kemungkinan penyebab:

1. LIMITASI ALGORITMA SASTRAWI (Nazief & Adriani)
   - Algoritma stemming tidak sempurna untuk semua kata
   - Ada kata-kata yang sulit di-stem karena kompleksitas imbuhan
   
2. MULTIPLE ROOT WORDS
   - 'pengembalian' bisa dari: 'kembali' ATAU 'balik'
   - Sastrawi mungkin memilih 'balik' sebagai root
   
3. AMBIGUITAS MORFOLOGI
   - Prefix: pe-N-
   - Root: kembali atau balik?
   - Suffix: -an
   
SOLUSI:
- Gunakan synonym dictionary untuk mapping manual
- Atau gunakan lemmatization (lebih akurat tapi lebih lambat)
""")
