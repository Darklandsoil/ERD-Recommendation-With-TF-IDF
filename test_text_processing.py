"""
Test script untuk memverifikasi Fase 1 Text Processing
"""
from utils.text_processing import (
    split_camelcase,
    remove_special_characters,
    normalize_whitespace,
    stem_indonesian,
    advanced_normalize_text
)

print("=" * 70)
print("TEST FASE 1 TEXT PROCESSING")
print("=" * 70)

# Test cases yang relevan dengan ERD attributes
test_cases = [
    "MataKuliah",
    "Mata_kuliah",
    "Mata-Kuliah",
    "No.Telepon",
    "Email@Address",
    "Nilai_Pembelajaran",
    "NamaMahasiswa",
    "Kemahasiswaan",
    "Perkuliahan",
    "ID_Dosen",
    "Tanggal  Lahir",
    "  IPKMahasiswa  ",
    "UserID",
]

print("\n1. TEST CAMELCASE SPLITTING")
print("-" * 70)
for test in test_cases:
    result = split_camelcase(test)
    print(f"'{test:20}' -> '{result}'")

print("\n2. TEST SPECIAL CHARACTERS REMOVAL")
print("-" * 70)
for test in test_cases:
    result = remove_special_characters(test)
    print(f"'{test:20}' -> '{result}'")

print("\n3. TEST WHITESPACE NORMALIZATION")
print("-" * 70)
for test in test_cases:
    result = normalize_whitespace(test)
    print(f"'{test:20}' -> '{result}'")

print("\n4. TEST INDONESIAN STEMMING")
print("-" * 70)
stemming_tests = [
    "pembelajaran",
    "kemahasiswaan",
    "perkuliahan",
    "mengajar",
    "pendaftaran",
    "pembayaran",
    "berkuliah",
    "mahasiswa"
]
for test in stemming_tests:
    result = stem_indonesian(test)
    print(f"'{test:20}' -> '{result}'")

print("\n5. TEST ADVANCED NORMALIZE TEXT (ALL COMBINED)")
print("-" * 70)
for test in test_cases:
    result = advanced_normalize_text(test)
    print(f"'{test:20}' -> '{result}'")

print("\n6. TEST REAL QUERY SCENARIOS")
print("-" * 70)
query_scenarios = [
    ("mata kuliah", "User search: mata kuliah"),
    ("MataKuliah", "Database has: MataKuliah"),
    ("Mata_kuliah", "Database has: Mata_kuliah"),
    ("nilai pembelajaran", "User search: nilai pembelajaran"),
    ("Nilai_Pembelajaran", "Database has: Nilai_Pembelajaran"),
    ("mahasiswa", "User search: mahasiswa"),
    ("Kemahasiswaan", "Database has: Kemahasiswaan"),
]

print("\nSkenario: User mencari 'mata kuliah', Database punya 'MataKuliah'")
for query, desc in query_scenarios:
    normalized = advanced_normalize_text(query)
    print(f"{desc:40} -> Normalized: '{normalized}'")

print("\n" + "=" * 70)
print("Kesimpulan:")
print("- Semua variasi 'Mata Kuliah' akan dinormalisasi menjadi 'kuliah'")
print("- User search 'mata kuliah' akan match dengan 'MataKuliah', 'Mata_kuliah'")
print("- Stemming membantu match 'mahasiswa' dengan 'Kemahasiswaan'")
print("=" * 70)
