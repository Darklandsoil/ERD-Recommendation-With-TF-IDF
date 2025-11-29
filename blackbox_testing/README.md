# Blackbox Testing - ERD Recommendation System

## 📁 File Structure

```
blackbox_testing/
├── README.md                           # Panduan penggunaan (file ini)
├── template_pengujian_blackbox.csv     # Template test case (Excel/CSV)
├── TEST_CASE_DOCUMENTATION.md          # Dokumentasi lengkap test case
├── automated_api_test.py               # Script otomasi testing API
├── requirements_testing.txt            # Dependencies untuk testing
└── test_results_[timestamp].json       # Hasil testing (auto-generated)
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install requests colorama tabulate
```

Atau menggunakan file requirements:

```bash
pip install -r blackbox_testing/requirements_testing.txt
```

### 2. Jalankan Server

Pastikan aplikasi Flask sudah berjalan:

```bash
python app.py
```

Server akan berjalan di `http://127.0.0.1:5000`

### 3. Jalankan Automated Testing

```bash
python blackbox_testing/automated_api_test.py
```

---

## 📋 Jenis-Jenis Pengujian

### 1. Manual Testing dengan Template CSV

**File**: `template_pengujian_blackbox.csv`

**Cara Penggunaan**:
1. Buka file CSV dengan Excel/Google Sheets
2. Untuk setiap test case, lakukan:
   - Jalankan aksi sesuai kolom "Input/Aksi"
   - Catat hasil di kolom "Actual Output"
   - Tentukan status (Pass/Fail) di kolom "Status"
   - Isi kolom "Tested By" dan "Test Date"
3. Hitung success rate di bagian summary

**Total Test Cases**: 82
- Authentication: 13 test cases
- User Dashboard: 11 test cases
- Advisor Dashboard: 20 test cases
- Admin Dashboard: 11 test cases
- API Testing: 8 test cases
- Integration Testing: 4 test cases
- Performance Testing: 4 test cases
- Security Testing: 8 test cases

---

### 2. Detailed Manual Testing dengan Dokumentasi

**File**: `TEST_CASE_DOCUMENTATION.md`

**Cara Penggunaan**:
1. Buka file markdown
2. Setiap test case memiliki:
   - ID Test Case
   - Jenis pengujian
   - Prekondisi
   - Langkah-langkah detail
   - Expected output yang jelas
   - Checkbox untuk Pass/Fail
3. Isi bagian "Actual Output" dan centang checkbox status
4. Buat screenshot untuk dokumentasi (optional)

**Keunggulan**:
- Penjelasan lebih detail
- Langkah-langkah yang jelas
- Mudah untuk dipahami tester pemula

---

### 3. Automated API Testing

**File**: `automated_api_test.py`

**Cara Penggunaan**:

```bash
# Jalankan semua test
python blackbox_testing/automated_api_test.py
```

**Fitur**:
- ✅ Otomatis membuat user test dan login
- ✅ Testing authentication (register, login, token validation)
- ✅ Testing user endpoints (search, request)
- ✅ Testing advisor endpoints (CRUD ERD, manage requests)
- ✅ Testing security (XSS, SQL Injection, JWT manipulation)
- ✅ Colored output untuk hasil yang mudah dibaca
- ✅ Generate JSON report otomatis
- ✅ Summary statistics (total, passed, failed, success rate)

**Output**:
- Console output dengan warna (hijau = pass, merah = fail)
- File JSON: `test_results_[timestamp].json`

**Contoh Output**:
```
================================================================================
                    TESTING AUTHENTICATION MODULE
================================================================================

[TC-AUTH-002] Register User dengan Data Valid
✓ PASS

[TC-AUTH-003] Register dengan Username Kosong
✓ PASS

...

================================================================================
                        TEST EXECUTION SUMMARY
================================================================================
Total Tests: 35
Passed: 33
Failed: 2
Success Rate: 94.29%
```

---

## 🎯 Tahap-Tahap Pengujian Blackbox

### Tahap 1: Persiapan
1. ✅ Pastikan database sudah di-setup
2. ✅ Pastikan server berjalan di `http://127.0.0.1:5000`
3. ✅ Install dependencies testing: `pip install -r blackbox_testing/requirements_testing.txt`
4. ✅ Siapkan akun testing:
   - Admin: username `admin`, password `Admin123!`
   - Advisor: username `testadvisor`, password `Test123!`
   - User: username `testuser`, password `Test123!`

### Tahap 2: Automated Testing (Recommended untuk API)
1. Jalankan: `python blackbox_testing/automated_api_test.py`
2. Review hasil di console
3. Cek file JSON hasil testing untuk detail
4. Dokumentasikan bug yang ditemukan

### Tahap 3: Manual Testing (Untuk UI dan UX)
1. Buka `TEST_CASE_DOCUMENTATION.md`
2. Test setiap modul secara berurutan:
   - Authentication (TC-AUTH-001 s/d TC-AUTH-013)
   - User Dashboard (TC-USER-001 s/d TC-USER-011)
   - Advisor Dashboard (TC-ADV-001 s/d TC-ADV-020)
   - Admin Dashboard (TC-ADM-001 s/d TC-ADM-011)
3. Isi "Actual Output" untuk setiap test case
4. Screenshot untuk dokumentasi (jika perlu)
5. Catat bug/issue di bagian "Bug/Issue Found"

### Tahap 4: Performance Testing
1. Test dengan data besar:
   - 1000+ ERD di database
   - 50+ concurrent users
2. Ukur:
   - Response time search
   - TF-IDF calculation time
   - Page load time
3. Tools (optional):
   - Apache JMeter
   - Locust
   - k6

### Tahap 5: Security Testing
1. **XSS Testing**: Input `<script>alert('XSS')</script>` di setiap form
2. **SQL Injection**: Input `' OR '1'='1` di login
3. **JWT Manipulation**: Modify token dan test access
4. **CSRF**: Test form submission tanpa token (jika ada)
5. **Directory Traversal**: Test download dengan path `../../etc/passwd`
6. **Password Security**: Check database - password harus di-hash

### Tahap 6: Integration Testing
1. **User Flow**: Register → Login → Search → Request → Check Status
2. **Advisor Flow**: Login → Add ERD → Generate → Assign Request → Complete
3. **Admin Flow**: Login → Create Advisor → Monitor → View Stats
4. **Cross-Role**: Admin create advisor → Advisor create ERD → User search ERD

### Tahap 7: Reporting
1. Hitung success rate: `(Passed / Total) * 100%`
2. List semua bug/issue yang ditemukan
3. Prioritas bug: Critical, High, Medium, Low
4. Buat dokumentasi dengan:
   - Executive summary
   - Test coverage
   - Test results (passed/failed)
   - Bug list dengan severity
   - Recommendations

---

## 📊 Metode Pengujian Blackbox yang Digunakan

### 1. Equivalence Partitioning
Membagi input menjadi kelompok valid dan invalid.

**Contoh**:
- **Username**: 
  - Valid: "testuser" (string 5-20 karakter)
  - Invalid: "" (kosong), "ab" (terlalu pendek), "verylongusernameover20chars" (terlalu panjang)

### 2. Boundary Value Analysis (BVA)
Testing pada nilai batas.

**Contoh**:
- **Password length**:
  - Boundary: 5 char (invalid), 6 char (valid minimum), 7 char (valid)
  - Boundary: 127 char (valid), 128 char (max), 129 char (invalid)

### 3. Error Guessing
Menebak error yang mungkin terjadi.

**Contoh**:
- SQL Injection: `admin' OR '1'='1`
- XSS: `<script>alert('XSS')</script>`
- Path Traversal: `../../etc/passwd`

### 4. State Transition Testing
Testing alur state.

**Contoh - Request Flow**:
```
[Pending] → (Advisor Assign) → [Assigned] → (Advisor Complete) → [Completed]
                ↓
         (User Cancel)
                ↓
           [Cancelled]
```

---

## 🐛 Template Bug Report

Jika menemukan bug, dokumentasikan dengan format:

```markdown
## Bug ID: BUG-001

**Severity**: Critical / High / Medium / Low
**Module**: Authentication / User / Advisor / Admin / API
**Summary**: [Singkat deskripsi bug]

**Steps to Reproduce**:
1. [Langkah 1]
2. [Langkah 2]
3. [Langkah 3]

**Expected Result**: [Apa yang seharusnya terjadi]
**Actual Result**: [Apa yang terjadi]

**Screenshot/Video**: [Link jika ada]
**Environment**: 
- OS: Windows 10
- Browser: Chrome 120
- Python: 3.11.9
- Date: 2025-11-28

**Additional Notes**: [Catatan tambahan]
```

---

## 📈 Metrics yang Diukur

### 1. Functional Metrics
- **Test Coverage**: Jumlah fitur yang ditest / Total fitur × 100%
- **Defect Density**: Jumlah bug / Total test cases
- **Pass Rate**: Passed tests / Total tests × 100%

### 2. Performance Metrics
- **Response Time**: Waktu respon API (target: < 3 detik)
- **Page Load Time**: Waktu load halaman (target: < 2 detik)
- **TF-IDF Calculation**: Waktu kalkulasi (target: < 10 detik untuk 1000 ERD)

### 3. Security Metrics
- **Vulnerability Count**: Jumlah security issues ditemukan
- **Critical Vulnerabilities**: SQL Injection, XSS, Authentication bypass
- **Authentication Strength**: Password hashing, JWT validation

---

## 🔧 Troubleshooting

### Server tidak berjalan
```bash
# Check apakah port 5000 sudah digunakan
netstat -ano | findstr :5000

# Jalankan server
python app.py
```

### Dependencies error
```bash
# Install ulang dependencies
pip install --upgrade -r blackbox_testing/requirements_testing.txt
```

### Test gagal karena database kosong
1. Pastikan database sudah di-initialize
2. Jalankan: `python init_admin.py` untuk create admin
3. Manual create beberapa sample ERD

### Token error
- Token expired: Login ulang
- Token invalid: Check JWT_SECRET_KEY di config.py

---

## 📞 Support

Jika ada pertanyaan atau menemukan issue:
1. Check dokumentasi di `TEST_CASE_DOCUMENTATION.md`
2. Review test results JSON file
3. Check application logs

---

## 📝 Checklist Sebelum Testing

- [ ] Server Flask berjalan
- [ ] Database sudah di-setup
- [ ] Admin account sudah dibuat (`python init_admin.py`)
- [ ] Dependencies testing sudah diinstall
- [ ] Port 5000 available
- [ ] Sample data ERD ada di database (minimal 5)

---

## ✅ Checklist Setelah Testing

- [ ] Semua test case sudah dijalankan
- [ ] Hasil documented (CSV atau JSON)
- [ ] Bug list sudah dibuat
- [ ] Screenshot important issues
- [ ] Success rate calculated
- [ ] Final report completed

---

**Generated**: 28 November 2025  
**Version**: 1.0  
**Maintainer**: [Nama Anda]
