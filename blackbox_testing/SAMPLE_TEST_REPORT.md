# Laporan Pengujian Blackbox
## Sistem Rekomendasi ERD dengan TF-IDF

---

## 📋 Informasi Dokumen

| Informasi | Detail |
|-----------|--------|
| **Nama Sistem** | ERD Recommendation System dengan TF-IDF |
| **Versi** | 1.0 |
| **Tipe Pengujian** | Blackbox Testing |
| **Tanggal Pengujian** | 28 November 2025 |
| **Tester** | [Nama Tester] |
| **Durasi Pengujian** | [X] Hari |

---

## 1. EXECUTIVE SUMMARY

### 1.1 Tujuan Pengujian
Pengujian blackbox ini dilakukan untuk memvalidasi fungsionalitas sistem rekomendasi ERD dengan metode TF-IDF, memastikan keamanan sistem, dan mengukur performa aplikasi dalam berbagai kondisi.

### 1.2 Ringkasan Hasil
[Isi dengan ringkasan hasil, contoh:]

Pengujian telah dilakukan terhadap 82 test case yang mencakup 8 modul utama sistem. Dari total 82 test case, **78 test case PASSED (95.12%)** dan **4 test case FAILED (4.88%)**. 

**Status Sistem**: ✅ Dapat digunakan dengan catatan perbaikan minor.

---

## 2. CAKUPAN PENGUJIAN (TEST COVERAGE)

### 2.1 Modul yang Diuji

| No | Modul | Jumlah Test Case | Status |
|----|-------|------------------|--------|
| 1 | Authentication | 13 | ✅ Tested |
| 2 | User Dashboard | 11 | ✅ Tested |
| 3 | Advisor Dashboard | 20 | ✅ Tested |
| 4 | Admin Dashboard | 11 | ✅ Tested |
| 5 | API Testing | 8 | ✅ Tested |
| 6 | Integration Testing | 4 | ✅ Tested |
| 7 | Performance Testing | 4 | ✅ Tested |
| 8 | Security Testing | 8 | ✅ Tested |
| **TOTAL** | | **82** | |

### 2.2 Metode Pengujian yang Digunakan

1. **Equivalence Partitioning**: Pengujian dengan membagi input menjadi kelas valid dan invalid
2. **Boundary Value Analysis**: Pengujian pada nilai batas minimum dan maksimum
3. **Error Guessing**: Pengujian skenario error yang mungkin terjadi
4. **State Transition Testing**: Pengujian alur perubahan status
5. **Security Testing**: Pengujian keamanan (XSS, SQL Injection, JWT manipulation)
6. **Performance Testing**: Pengujian response time dan concurrent users

---

## 3. HASIL PENGUJIAN

### 3.1 Statistik Keseluruhan

```
Total Test Cases    : 82
Passed             : 78 (95.12%)
Failed             : 4 (4.88%)
Blocked            : 0 (0%)
Not Executed       : 0 (0%)
```

**Success Rate**: 95.12% ✅

### 3.2 Hasil per Modul

#### 3.2.1 Authentication Module
| Test Case ID | Test Name | Status | Severity |
|--------------|-----------|--------|----------|
| TC-AUTH-001 | Register dengan data valid | ✅ PASS | - |
| TC-AUTH-002 | Register dengan username kosong | ✅ PASS | - |
| TC-AUTH-003 | Register dengan email tidak valid | ✅ PASS | - |
| TC-AUTH-004 | Register dengan password < 6 char | ✅ PASS | - |
| TC-AUTH-005 | Register dengan username duplikat | ✅ PASS | - |
| TC-AUTH-006 | Login dengan kredensial valid | ✅ PASS | - |
| TC-AUTH-007 | Login dengan username tidak terdaftar | ✅ PASS | - |
| TC-AUTH-008 | Login dengan password salah | ✅ PASS | - |
| TC-AUTH-009 | Login dengan field kosong | ✅ PASS | - |
| TC-AUTH-010 | Logout | ✅ PASS | - |
| TC-AUTH-011 | Akses protected tanpa token | ✅ PASS | - |
| TC-AUTH-012 | Akses dengan token expired | ✅ PASS | - |
| TC-AUTH-013 | SQL Injection pada login | ✅ PASS | - |

**Summary**: 13/13 PASSED (100%)

---

#### 3.2.2 User Dashboard Module
| Test Case ID | Test Name | Status | Severity |
|--------------|-----------|--------|----------|
| TC-USER-001 | Akses dashboard user | ✅ PASS | - |
| TC-USER-002 | Search ERD dengan keyword valid | ✅ PASS | - |
| TC-USER-003 | Search ERD dengan keyword kosong | ✅ PASS | - |
| TC-USER-004 | XSS pada search keyword | ✅ PASS | - |
| TC-USER-005 | Search dengan keyword sangat panjang | ⚠️ FAIL | Medium |
| TC-USER-006 | Membuat request konsultasi | ✅ PASS | - |
| TC-USER-007 | Request dengan field kosong | ✅ PASS | - |
| TC-USER-008 | Melihat daftar request pribadi | ✅ PASS | - |
| TC-USER-009 | Cancel request pending | ✅ PASS | - |
| TC-USER-010 | Cancel request assigned | ✅ PASS | - |
| TC-USER-011 | Akses ERD user lain | ✅ PASS | - |

**Summary**: 10/11 PASSED (90.91%)

---

#### 3.2.3 Advisor Dashboard Module
| Test Case ID | Test Name | Status | Severity |
|--------------|-----------|--------|----------|
| TC-ADV-001 | Akses dashboard advisor | ✅ PASS | - |
| TC-ADV-002 | Tambah ERD dengan data valid | ✅ PASS | - |
| TC-ADV-003 | Tambah ERD dengan nama kosong | ✅ PASS | - |
| TC-ADV-004 | Tambah ERD dengan nama duplikat | ✅ PASS | - |
| TC-ADV-005 | Tambah ERD tanpa entitas | ✅ PASS | - |
| TC-ADV-006 | Edit ERD milik sendiri | ✅ PASS | - |
| TC-ADV-007 | Edit ERD milik advisor lain | ✅ PASS | - |
| TC-ADV-008 | Hapus ERD milik sendiri | ✅ PASS | - |
| TC-ADV-009 | Hapus ERD milik advisor lain | ✅ PASS | - |
| TC-ADV-010 | Melihat daftar ERD milik sendiri | ✅ PASS | - |
| TC-ADV-011 | Generate ERD image | ✅ PASS | - |
| TC-ADV-012 | Download ERD image | ✅ PASS | - |
| TC-ADV-013 | Akses ERD Builder | ✅ PASS | - |
| TC-ADV-014 | Zoom in/out pada ERD Builder | ✅ PASS | - |
| TC-ADV-015 | Melihat pending requests | ✅ PASS | - |
| TC-ADV-016 | Assign request | ✅ PASS | - |
| TC-ADV-017 | Melihat assigned requests | ✅ PASS | - |
| TC-ADV-018 | Complete request | ✅ PASS | - |
| TC-ADV-019 | Complete request milik advisor lain | ✅ PASS | - |
| TC-ADV-020 | User akses advisor dashboard | ✅ PASS | - |

**Summary**: 20/20 PASSED (100%)

---

#### 3.2.4 Admin Dashboard Module
| Test Case ID | Test Name | Status | Severity |
|--------------|-----------|--------|----------|
| TC-ADM-001 | Akses dashboard admin | ✅ PASS | - |
| TC-ADM-002 | Melihat daftar advisor | ✅ PASS | - |
| TC-ADM-003 | Tambah advisor baru | ✅ PASS | - |
| TC-ADM-004 | Tambah advisor username duplikat | ✅ PASS | - |
| TC-ADM-005 | Edit data advisor | ✅ PASS | - |
| TC-ADM-006 | Hapus advisor | ✅ PASS | - |
| TC-ADM-007 | Melihat statistics | ✅ PASS | - |
| TC-ADM-008 | Melihat advisor monitoring | ✅ PASS | - |
| TC-ADM-009 | Reload system | ⚠️ FAIL | Low |
| TC-ADM-010 | User akses admin dashboard | ✅ PASS | - |
| TC-ADM-011 | Advisor akses admin dashboard | ✅ PASS | - |

**Summary**: 10/11 PASSED (90.91%)

---

#### 3.2.5 API Testing
| Test Case ID | Test Name | Status | Severity |
|--------------|-----------|--------|----------|
| TC-API-001 | Get API tanpa token | ✅ PASS | - |
| TC-API-002 | Method not allowed | ✅ PASS | - |
| TC-API-003 | Invalid JSON body | ✅ PASS | - |
| TC-API-004 | Invalid ID format | ✅ PASS | - |
| TC-API-005 | Resource not found | ✅ PASS | - |
| TC-API-006 | Large payload upload | ✅ PASS | - |
| TC-API-007 | Concurrent requests | ✅ PASS | - |
| TC-API-008 | Rate limiting | ✅ PASS | - |

**Summary**: 8/8 PASSED (100%)

---

#### 3.2.6 Integration Testing
| Test Case ID | Test Name | Status | Severity |
|--------------|-----------|--------|----------|
| TC-INT-001 | End-to-end user journey | ✅ PASS | - |
| TC-INT-002 | End-to-end advisor journey | ✅ PASS | - |
| TC-INT-003 | Request flow complete | ✅ PASS | - |
| TC-INT-004 | Cross-role data sync | ✅ PASS | - |

**Summary**: 4/4 PASSED (100%)

---

#### 3.2.7 Performance Testing
| Test Case ID | Test Name | Status | Metric | Target | Actual |
|--------------|-----------|--------|--------|--------|--------|
| TC-PERF-001 | Search response time (1000+ ERD) | ✅ PASS | Response Time | < 3s | 2.1s |
| TC-PERF-002 | TF-IDF calculation | ✅ PASS | Processing Time | < 10s | 6.8s |
| TC-PERF-003 | 50 concurrent logins | ⚠️ FAIL | Success Rate | 100% | 94% |
| TC-PERF-004 | Page load time | ✅ PASS | Load Time | < 2s | 1.5s |

**Summary**: 3/4 PASSED (75%)

---

#### 3.2.8 Security Testing
| Test Case ID | Test Name | Status | Severity |
|--------------|-----------|--------|----------|
| TC-SEC-001 | XSS attack pada form | ✅ PASS | Critical |
| TC-SEC-002 | SQL Injection | ✅ PASS | Critical |
| TC-SEC-003 | CSRF token validation | ✅ PASS | High |
| TC-SEC-004 | JWT manipulation | ✅ PASS | Critical |
| TC-SEC-005 | Password hashing | ✅ PASS | Critical |
| TC-SEC-006 | Unauthorized file access | ✅ PASS | Medium |
| TC-SEC-007 | Directory traversal | ✅ PASS | High |
| TC-SEC-008 | Privilege escalation | ✅ PASS | Critical |

**Summary**: 8/8 PASSED (100%) ✅

**Security Status**: SECURE - Tidak ada critical vulnerability ditemukan

---

## 4. BUG REPORT

### 4.1 Daftar Bug yang Ditemukan

#### 🔴 BUG-001: Keyword Terlalu Panjang Tidak Divalidasi
- **Test Case**: TC-USER-005
- **Severity**: Medium
- **Priority**: Medium
- **Module**: User Dashboard - Search
- **Status**: Open

**Deskripsi**:  
Sistem tidak memvalidasi panjang keyword pada fitur search ERD. Keyword dengan panjang 1000+ karakter dapat menyebabkan response time yang sangat lambat.

**Steps to Reproduce**:
1. Login sebagai user
2. Input keyword dengan 1500 karakter
3. Klik search

**Expected Result**: Error message "Keyword terlalu panjang (maksimal 500 karakter)"

**Actual Result**: Request timeout setelah 30 detik

**Recommendation**: Tambahkan validasi max length 500 karakter pada frontend dan backend

---

#### 🟡 BUG-002: Reload System Tidak Memberikan Feedback
- **Test Case**: TC-ADM-009
- **Severity**: Low
- **Priority**: Low
- **Module**: Admin Dashboard
- **Status**: Open

**Deskripsi**:  
Ketika admin klik "Reload System", tidak ada loading indicator atau feedback bahwa proses sedang berjalan. User tidak tahu apakah system sedang di-reload atau tidak.

**Steps to Reproduce**:
1. Login sebagai admin
2. Klik "Reload System"
3. Observe UI

**Expected Result**: 
- Muncul loading indicator
- Disable button saat proses
- Success notification setelah selesai

**Actual Result**: Tidak ada visual feedback

**Recommendation**: Tambahkan loading spinner dan disable button saat proses reload

---

#### 🟡 BUG-003: Concurrent Login Menyebabkan Beberapa Request Gagal
- **Test Case**: TC-PERF-003
- **Severity**: Medium
- **Priority**: Medium
- **Module**: Authentication
- **Status**: Open

**Deskripsi**:  
Ketika 50 users login bersamaan, 3 request (6%) gagal dengan error connection timeout.

**Steps to Reproduce**:
1. Siapkan 50 user accounts
2. Gunakan script load testing untuk login bersamaan
3. Check success rate

**Expected Result**: 100% success (50/50)

**Actual Result**: 94% success (47/50), 3 failed dengan timeout

**Recommendation**: 
- Implementasi connection pooling
- Optimize database query
- Consider load balancer untuk production

---

#### 🟢 BUG-004: Minor UI Issue - Button Alignment
- **Test Case**: Manual UI Testing
- **Severity**: Low
- **Priority**: Low
- **Module**: UI/UX
- **Status**: Open

**Deskripsi**:  
Button "Cancel" pada modal request tidak sejajar dengan button "Submit"

**Steps to Reproduce**:
1. Buka user dashboard
2. Klik "Request Consultation"
3. Observe button alignment di modal

**Expected Result**: Buttons sejajar horizontal

**Actual Result**: Button "Cancel" sedikit lebih rendah

**Recommendation**: Fix CSS margin/padding

---

### 4.2 Severity Distribution

| Severity | Count | Percentage |
|----------|-------|------------|
| Critical | 0 | 0% |
| High | 0 | 0% |
| Medium | 2 | 50% |
| Low | 2 | 50% |
| **Total** | **4** | **100%** |

**Status**: ✅ Tidak ada critical bug ditemukan

---

## 5. ANALISIS HASIL

### 5.1 Kekuatan Sistem (Strengths)

1. ✅ **Security**: Sistem memiliki security yang baik
   - XSS prevention implemented
   - SQL Injection protection
   - JWT authentication secure
   - Password hashing implemented
   - Authorization properly implemented

2. ✅ **Authentication**: Modul authentication sangat robust
   - Validasi input lengkap
   - Error handling baik
   - Token management secure

3. ✅ **API Design**: API design consistent dan RESTful
   - HTTP status codes appropriate
   - Error responses informative
   - JSON format consistent

4. ✅ **Core Functionality**: Fitur utama berfungsi dengan baik
   - TF-IDF recommendation accurate
   - CRUD operations stable
   - Request flow berjalan lancar

### 5.2 Kelemahan Sistem (Weaknesses)

1. ⚠️ **Input Validation**: Beberapa input belum divalidasi dengan baik
   - Keyword length tidak dibatasi (BUG-001)
   - Large payload handling perlu improvement

2. ⚠️ **User Feedback**: UI feedback kurang optimal
   - Loading indicators kurang (BUG-002)
   - Error messages bisa lebih descriptive

3. ⚠️ **Performance**: Performance dengan load tinggi perlu improvement
   - Concurrent request handling (BUG-003)
   - Database query optimization needed

4. ⚠️ **UI/UX**: Minor UI issues
   - Button alignment (BUG-004)
   - Responsive design bisa ditingkatkan

---

## 6. REKOMENDASI

### 6.1 Prioritas Tinggi (Must Fix)
1. **BUG-001**: Implementasi validasi panjang keyword
2. **BUG-003**: Optimize concurrent request handling

### 6.2 Prioritas Medium (Should Fix)
1. **BUG-002**: Tambahkan loading indicators
2. Improve error messages untuk lebih user-friendly
3. Tambahkan rate limiting untuk prevent abuse

### 6.3 Prioritas Rendah (Nice to Have)
1. **BUG-004**: Fix minor UI alignment issues
2. Improve responsive design
3. Add more detailed logging untuk debugging

### 6.4 Future Improvements
1. Implementasi caching untuk improve performance
2. Add pagination untuk list yang panjang
3. Implement websocket untuk real-time notifications
4. Add export feature untuk ERD (PDF, SQL)
5. Implement full-text search dengan Elasticsearch

---

## 7. KESIMPULAN

### 7.1 Summary
Sistem ERD Recommendation dengan TF-IDF telah melalui pengujian blackbox yang komprehensif dengan **82 test cases** mencakup 8 modul utama. Hasil pengujian menunjukkan **success rate 95.12%** dengan 4 bug ditemukan (2 medium, 2 low, 0 critical).

### 7.2 Overall Assessment
**Status**: ✅ **READY FOR PRODUCTION** dengan catatan perbaikan minor

**Justifikasi**:
- ✅ Core functionality berjalan dengan baik
- ✅ Security sangat baik (100% passed)
- ✅ No critical bugs found
- ⚠️ Beberapa improvement diperlukan untuk performance dan UX
- ⚠️ 4 minor bugs dapat diperbaiki di sprint berikutnya

### 7.3 Go/No-Go Decision
**✅ GO** - Sistem dapat di-deploy ke production dengan monitoring

**Conditions**:
1. Fix BUG-001 (keyword validation) sebelum deployment
2. Monitor performance untuk concurrent users
3. Siapkan rollback plan
4. Setup error logging dan monitoring

---

## 8. LAMPIRAN

### 8.1 Test Environment
- **OS**: Windows 10
- **Browser**: Chrome 120, Firefox 121
- **Python**: 3.11.9
- **Flask**: 3.0.0
- **Database**: [Database yang digunakan]
- **Server**: Local development (127.0.0.1:5000)

### 8.2 Test Data
- Total Users: 10 (3 admin, 3 advisor, 4 user)
- Total ERDs: 25
- Total Requests: 15 (5 pending, 5 assigned, 5 completed)

### 8.3 Tools Used
- **Manual Testing**: Browser DevTools
- **Automated Testing**: Python script (automated_api_test.py)
- **Load Testing**: Custom Python script
- **Security Testing**: Manual payload injection

### 8.4 References
- Test Case Documentation: `TEST_CASE_DOCUMENTATION.md`
- Test Results JSON: `test_results_[timestamp].json`
- Bug Reports: Issues tracked in GitHub/Jira

---

## 9. SIGN-OFF

| Role | Nama | Signature | Date |
|------|------|-----------|------|
| **Tester** | [Nama] | | [Date] |
| **Developer** | [Nama] | | [Date] |
| **Project Manager** | [Nama] | | [Date] |
| **QA Lead** | [Nama] | | [Date] |

---

**Document Version**: 1.0  
**Last Updated**: 28 November 2025  
**Next Review Date**: [Date]
