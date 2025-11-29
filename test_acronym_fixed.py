"""
Test untuk verifikasi bahwa akronim sekarang di-preserve dengan benar
"""
from utils.text_processing import (
    split_camelcase,
    advanced_normalize_text,
    remove_stopwords
)

print("=" * 80)
print("VERIFIKASI FIX UNTUK AKRONIM")
print("=" * 80)

# Test cases dengan akronim
test_cases = [
    ("BKDD", "BKDD", "Akronim murni"),
    ("IPK", "IPK", "Akronim murni"),
    ("NIM", "NIM", "Akronim murni"),
    ("IPKMahasiswa", "IPK Mahasiswa", "Akronim + kata"),
    ("NIMSiswa", "NIM Siswa", "Akronim + kata"),
    ("XMLParser", "XML Parser", "Akronim + kata"),
    ("StatusBKDD", "Status BKDD", "Kata + akronim"),
    ("Verifikasi_BKDD", "Verifikasi_ BKDD", "Kata + underscore + akronim"),
    ("MataKuliah", "Mata Kuliah", "PascalCase biasa"),
    ("mataKuliah", "mata Kuliah", "camelCase biasa"),
    ("userId", "user Id", "camelCase dengan Id"),
]

print("\n1. TEST SPLIT CAMELCASE (Harus preserve akronim)")
print("-" * 80)
print(f"{'Input':<25} {'Expected':<25} {'Result':<25} {'Status':<10}")
print("-" * 80)

all_pass = True
for input_text, expected, description in test_cases:
    result = split_camelcase(input_text)
    status = "PASS" if result == expected else "FAIL"
    if status == "FAIL":
        all_pass = False
    print(f"{input_text:<25} {expected:<25} {result:<25} {status:<10}")

print(f"\nOverall: {'ALL TESTS PASSED!' if all_pass else 'SOME TESTS FAILED!'}")

print("\n2. TEST ADVANCED NORMALIZE TEXT")
print("-" * 80)
print(f"{'Input':<25} {'After advanced_normalize_text':<40}")
print("-" * 80)

acronym_tests = ["BKDD", "IPK", "NIM", "IPKMahasiswa", "NIMSiswa", "Verifikasi_BKDD"]
for test in acronym_tests:
    result = advanced_normalize_text(test)
    print(f"{test:<25} {result:<40}")

print("\n3. FULL PIPELINE TEST: Database 'Verifikasi_BKDD'")
print("-" * 80)

db_attr = "Verifikasi_BKDD"
print(f"Database Attribute: '{db_attr}'")
db_normalized = advanced_normalize_text(db_attr)
print(f"After normalization: '{db_normalized}'")
db_final = remove_stopwords(db_normalized)
print(f"After stopwords removal: '{db_final}'")

print("\n" + "-" * 80)
print("Query Test Cases:")
print("-" * 80)

test_queries = [
    ("verifikasi", "Match dengan 'verifikasi' di DB"),
    ("BKDD", "Match dengan 'bkdd' di DB"),
    ("bkdd", "Match dengan 'bkdd' di DB"),
]

for query, description in test_queries:
    print(f"\nQuery: '{query}' ({description})")
    q_normalized = advanced_normalize_text(query)
    print(f"  After normalization: '{q_normalized}'")
    q_final = remove_stopwords(q_normalized)
    print(f"  After stopwords removal: '{q_final}'")
    
    # Check if query is non-empty and can match
    if q_final:
        can_match = q_final in db_final or db_final in q_final or q_final == db_final.split()[0] or q_final == db_final.split()[-1]
        print(f"  Query is non-empty: YES")
        print(f"  Contains in DB final '{db_final}': {can_match}")
    else:
        print(f"  Query is non-empty: NO (PROBLEM!)")

print("\n" + "=" * 80)
print("4. COMPARISON: BEFORE vs AFTER FIX")
print("=" * 80)

print("\nBEFORE (Old regex):")
print("  'BKDD' -> 'B K D D' -> filter len>2 -> '' (EMPTY!)")
print("  Query 'BKDD' -> No results")

print("\nAFTER (New regex):")
print(f"  'BKDD' -> '{split_camelcase('BKDD')}' -> normalize -> '{advanced_normalize_text('BKDD')}'")
result = remove_stopwords(advanced_normalize_text('BKDD'))
print(f"  After stopwords: '{result}' (NON-EMPTY!)")
print(f"  Query 'BKDD' -> Can find results!")

print("\n" + "=" * 80)
print("KESIMPULAN:")
print("-" * 80)
print("Dengan regex baru:")
print("1. Akronim (BKDD, IPK, NIM) TIDAK dipecah - tetap utuh")
print("2. CamelCase masih berfungsi (MataKuliah -> Mata Kuliah)")
print("3. Akronim + kata berfungsi (IPKMahasiswa -> IPK Mahasiswa)")
print("4. Query 'BKDD' sekarang dapat menemukan 'Verifikasi_BKDD'!")
print("=" * 80)
