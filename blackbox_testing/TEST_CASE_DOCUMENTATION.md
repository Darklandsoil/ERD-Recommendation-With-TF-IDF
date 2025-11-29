# Dokumentasi Test Case - ERD Recommendation System
## Blackbox Testing

---

## 📋 Informasi Umum
- **Nama Sistem**: ERD Recommendation System dengan TF-IDF
- **Versi**: 1.0
- **Tanggal Pembuatan**: 28 November 2025
- **Tester**: [Nama Tester]

---

## 🎯 Tujuan Pengujian
Melakukan pengujian blackbox untuk memvalidasi:
1. Fungsionalitas setiap fitur sesuai requirement
2. Keamanan sistem (autentikasi, autorisasi, injection)
3. Performa sistem dengan berbagai kondisi
4. Integrasi antar modul

---

## 📊 Kategori Pengujian

### 1. MODUL AUTHENTICATION

#### TC-AUTH-001: Register dengan Data Valid
- **Jenis**: Positive Testing
- **Prekondisi**: User belum terdaftar dalam database
- **Langkah**:
  1. Buka halaman register (`/register`)
  2. Isi form:
     - Username: `testuser123`
     - Email: `test@mail.com`
     - Password: `Test123!`
     - Confirm Password: `Test123!`
     - Role: `user`
  3. Klik tombol "Register"
- **Expected Output**: 
  - Registrasi berhasil
  - Muncul notifikasi sukses
  - Redirect ke halaman login
  - Data tersimpan di database
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-002: Register dengan Username Kosong
- **Jenis**: Negative Testing
- **Prekondisi**: Halaman register terbuka
- **Langkah**:
  1. Buka halaman register
  2. Isi form:
     - Username: `(kosong)`
     - Email: `test@mail.com`
     - Password: `Test123!`
  3. Klik tombol "Register"
- **Expected Output**: 
  - Muncul error message: "Username wajib diisi"
  - Form tidak tersubmit
  - Tetap di halaman register
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-003: Register dengan Email Tidak Valid
- **Jenis**: Negative Testing
- **Prekondisi**: Halaman register terbuka
- **Langkah**:
  1. Buka halaman register
  2. Isi form dengan email invalid: `invalidemail`, `test@`, `@mail.com`
  3. Klik register
- **Expected Output**: Error "Format email tidak valid"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-004: Register dengan Password < 6 Karakter (Boundary)
- **Jenis**: Boundary Value Analysis
- **Prekondisi**: Halaman register terbuka
- **Test Data**:
  - Password 5 char: `12345` (Invalid)
  - Password 6 char: `123456` (Valid)
  - Password 7 char: `1234567` (Valid)
- **Expected Output**: Error jika < 6 karakter
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-005: Register dengan Username Duplikat
- **Jenis**: Negative Testing
- **Prekondisi**: Username `testuser` sudah terdaftar
- **Langkah**:
  1. Register dengan username `testuser` (yang sudah ada)
- **Expected Output**: Error "Username sudah digunakan"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-006: Login dengan Kredensial Valid
- **Jenis**: Positive Testing
- **Prekondisi**: User `testuser` dengan password `Test123!` sudah terdaftar
- **Langkah**:
  1. Buka `/login`
  2. Input username: `testuser`
  3. Input password: `Test123!`
  4. Klik Login
- **Expected Output**: 
  - Login berhasil
  - Mendapat JWT token
  - Redirect ke dashboard sesuai role
  - Token tersimpan di localStorage/cookie
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-007: Login dengan Username Tidak Terdaftar
- **Jenis**: Negative Testing
- **Prekondisi**: Username `notexistuser` tidak ada di database
- **Langkah**:
  1. Login dengan username: `notexistuser`
  2. Password: `anything`
- **Expected Output**: Error "Username tidak ditemukan"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-008: Login dengan Password Salah
- **Jenis**: Negative Testing
- **Prekondisi**: User `testuser` terdaftar dengan password `Test123!`
- **Langkah**:
  1. Login dengan username: `testuser`
  2. Password: `WrongPassword`
- **Expected Output**: Error "Password salah"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-009: Login dengan Field Kosong
- **Jenis**: Negative Testing
- **Test Data**:
  - Username kosong, password kosong
  - Username ada, password kosong
  - Username kosong, password ada
- **Expected Output**: Error "Field wajib diisi"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-010: Logout
- **Jenis**: Positive Testing
- **Prekondisi**: User sudah login
- **Langkah**:
  1. Klik tombol Logout
- **Expected Output**: 
  - Token dihapus
  - Redirect ke login
  - Tidak bisa akses halaman protected
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-011: Akses Halaman Protected Tanpa Token
- **Jenis**: Negative Testing / Security
- **Prekondisi**: Belum login (no token)
- **Langkah**:
  1. Akses langsung `/user-dashboard`
  2. Akses `/advisor-dashboard`
  3. Akses `/admin-dashboard`
- **Expected Output**: 
  - HTTP 401 Unauthorized
  - Redirect ke login
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-012: Akses dengan Token Expired
- **Jenis**: Negative Testing
- **Prekondisi**: Token JWT sudah expired
- **Langkah**:
  1. Gunakan token yang sudah expired untuk akses API
- **Expected Output**: HTTP 401 "Token telah kadaluarsa"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-AUTH-013: SQL Injection pada Login
- **Jenis**: Security Testing
- **Prekondisi**: Sistem berjalan
- **Test Data**:
  - Username: `admin' OR '1'='1`
  - Username: `admin'--`
  - Username: `'; DROP TABLE users;--`
- **Expected Output**: 
  - Login gagal
  - Tidak bypass authentication
  - Query di-escape/parameterized
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

### 2. MODUL USER DASHBOARD

#### TC-USER-001: Akses Dashboard User
- **Jenis**: Positive Testing
- **Prekondisi**: Login sebagai role `user`
- **Langkah**:
  1. Login sebagai user
  2. Akses `/user-dashboard`
- **Expected Output**: 
  - Dashboard tampil dengan komponen:
    - Search bar
    - List ERD recommendations
    - Request consultation button
    - My requests section
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-002: Search ERD dengan Keyword Valid
- **Jenis**: Positive Testing
- **Prekondisi**: 
  - Login sebagai user
  - Database memiliki minimal 5 ERD
- **Langkah**:
  1. Input keyword: `mahasiswa`
  2. Klik Search / Enter
- **Expected Output**: 
  - Menampilkan ERD yang relevan
  - ERD diurutkan berdasarkan skor TF-IDF (tertinggi ke terendah)
  - Menampilkan nama ERD, entitas, dan skor relevansi
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-003: Search ERD dengan Keyword Kosong
- **Jenis**: Negative Testing
- **Prekondisi**: Login sebagai user
- **Langkah**:
  1. Kosongkan search box
  2. Klik Search
- **Expected Output**: 
  - Error "Keyword wajib diisi"
  - ATAU menampilkan semua ERD tanpa sorting
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-004: XSS pada Search Keyword
- **Jenis**: Security Testing
- **Prekondisi**: Login sebagai user
- **Test Data**:
  - `<script>alert('XSS')</script>`
  - `<img src=x onerror=alert('XSS')>`
  - `javascript:alert('XSS')`
- **Expected Output**: 
  - Input di-sanitize
  - Script tidak dieksekusi
  - Search tetap berjalan atau error "Invalid character"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-005: Search dengan Keyword Sangat Panjang
- **Jenis**: Boundary Value Analysis
- **Prekondisi**: Login sebagai user
- **Test Data**: String 1000+ karakter
- **Expected Output**: 
  - Error "Keyword terlalu panjang"
  - ATAU keyword dipotong otomatis
  - ATAU search berjalan normal
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-006: Membuat Request Konsultasi Valid
- **Jenis**: Positive Testing
- **Prekondisi**: Login sebagai user
- **Langkah**:
  1. Klik "Request Consultation"
  2. Isi form:
     - Judul: `Butuh bantuan ERD Perpustakaan`
     - Deskripsi: `Saya perlu bantuan membuat ERD untuk sistem perpustakaan dengan 5 entitas`
  3. Submit
- **Expected Output**: 
  - Request berhasil dibuat
  - Status: `pending`
  - Muncul di "My Requests"
  - Notifikasi sukses
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-007: Request dengan Field Kosong
- **Jenis**: Negative Testing
- **Prekondisi**: Login sebagai user
- **Test Data**:
  - Judul kosong, deskripsi ada
  - Judul ada, deskripsi kosong
  - Keduanya kosong
- **Expected Output**: Error "Field wajib diisi"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-008: Melihat Daftar Request Pribadi
- **Jenis**: Positive Testing
- **Prekondisi**: User memiliki 3 request (pending, assigned, completed)
- **Langkah**:
  1. Buka "My Requests"
- **Expected Output**: 
  - Menampilkan semua request milik user
  - Menampilkan status masing-masing
  - Ada tombol "Cancel" untuk pending request
  - Tidak menampilkan request user lain
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-009: Cancel Request dengan Status Pending
- **Jenis**: Positive Testing
- **Prekondisi**: User memiliki request dengan status `pending`
- **Langkah**:
  1. Klik "Cancel" pada request pending
  2. Konfirmasi cancellation
- **Expected Output**: 
  - Request dihapus / status berubah ke `cancelled`
  - Tidak muncul lagi di list pending
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-010: Cancel Request dengan Status Assigned
- **Jenis**: Negative Testing
- **Prekondisi**: User memiliki request dengan status `assigned`
- **Langkah**:
  1. Coba cancel request yang sudah assigned
- **Expected Output**: 
  - Error "Request tidak dapat dibatalkan karena sudah ditangani advisor"
  - ATAU tetap bisa cancel dengan konfirmasi
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-USER-011: Akses ERD Detail User Lain
- **Jenis**: Security Testing
- **Prekondisi**: Login sebagai user A
- **Langkah**:
  1. Dapatkan ID ERD milik user B (private)
  2. Akses `/api/erd/{id_erd_user_b}`
- **Expected Output**: 
  - HTTP 403 Forbidden
  - ATAU hanya bisa akses jika ERD public
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

### 3. MODUL ADVISOR DASHBOARD

#### TC-ADV-001: Akses Dashboard Advisor
- **Jenis**: Positive Testing
- **Prekondisi**: Login sebagai role `advisor`
- **Langkah**:
  1. Login sebagai advisor
  2. Akses `/advisor-dashboard`
- **Expected Output**: 
  - Dashboard tampil dengan:
    - My ERDs list
    - Add ERD button
    - Pending Requests
    - My Assigned Requests
    - ERD Builder link
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-002: Tambah ERD dengan Data Valid
- **Jenis**: Positive Testing
- **Prekondisi**: Login sebagai advisor
- **Langkah**:
  1. Klik "Add ERD"
  2. Isi form:
     - Nama: `ERD_Penjualan_Online`
     - Deskripsi: `ERD untuk sistem penjualan online`
     - Entitas: 
       - `Pelanggan` (atribut: id, nama, email, telepon)
       - `Produk` (atribut: id, nama, harga, stok)
       - `Pesanan` (atribut: id, tanggal, total)
     - Relasi:
       - `Pelanggan` membeli `Produk` (M:N)
       - `Pelanggan` memiliki `Pesanan` (1:N)
  3. Submit
- **Expected Output**: 
  - ERD berhasil ditambahkan
  - Muncul di "My ERDs"
  - Data tersimpan di database
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-003: Tambah ERD dengan Nama Kosong
- **Jenis**: Negative Testing
- **Prekondisi**: Login sebagai advisor
- **Langkah**:
  1. Isi form ERD tanpa nama
  2. Submit
- **Expected Output**: Error "Nama ERD wajib diisi"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-004: Tambah ERD dengan Nama Duplikat
- **Jenis**: Negative Testing
- **Prekondisi**: ERD dengan nama `ERD_Test` sudah ada
- **Langkah**:
  1. Tambah ERD dengan nama `ERD_Test`
- **Expected Output**: Error "Nama ERD sudah digunakan"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-005: Tambah ERD Tanpa Entitas
- **Jenis**: Negative Testing
- **Prekondisi**: Login sebagai advisor
- **Langkah**:
  1. Isi nama ERD
  2. Tidak tambahkan entitas (array kosong)
  3. Submit
- **Expected Output**: Error "Minimal 1 entitas diperlukan"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-006: Edit ERD Milik Sendiri
- **Jenis**: Positive Testing
- **Prekondisi**: Advisor memiliki ERD `ERD_Old`
- **Langkah**:
  1. Klik "Edit" pada ERD milik sendiri
  2. Ubah nama menjadi `ERD_New`
  3. Tambah 1 entitas baru
  4. Save
- **Expected Output**: 
  - ERD berhasil diupdate
  - Perubahan tersimpan
  - Nama dan entitas berubah
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-007: Edit ERD Milik Advisor Lain
- **Jenis**: Security Testing
- **Prekondisi**: Login sebagai advisor A
- **Langkah**:
  1. Dapatkan ID ERD milik advisor B
  2. PUT `/api/erd/{id_erd_advisor_b}` dengan perubahan
- **Expected Output**: HTTP 403 Forbidden
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-008: Hapus ERD Milik Sendiri
- **Jenis**: Positive Testing
- **Prekondisi**: Advisor memiliki ERD
- **Langkah**:
  1. Klik "Delete" pada ERD milik sendiri
  2. Konfirmasi delete
- **Expected Output**: 
  - ERD berhasil dihapus
  - Tidak muncul di list
  - Data terhapus dari database
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-009: Hapus ERD Milik Advisor Lain
- **Jenis**: Security Testing
- **Prekondisi**: Login sebagai advisor A
- **Langkah**:
  1. DELETE `/api/erd/{id_erd_advisor_b}`
- **Expected Output**: HTTP 403 Forbidden
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-010: Melihat Daftar ERD Milik Sendiri
- **Jenis**: Positive Testing
- **Prekondisi**: Advisor memiliki 5 ERD
- **Langkah**:
  1. Buka "My ERDs"
- **Expected Output**: 
  - Menampilkan 5 ERD milik advisor
  - Tidak menampilkan ERD advisor lain
  - Ada tombol Edit dan Delete untuk setiap ERD
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-011: Generate ERD Image
- **Jenis**: Positive Testing
- **Prekondisi**: Advisor memiliki ERD `ERD_Test`
- **Langkah**:
  1. Klik "Generate Image" pada ERD
- **Expected Output**: 
  - Image PNG berhasil di-generate
  - Image tersimpan di `/static/image/`
  - Image dapat dilihat preview
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-012: Download ERD Image
- **Jenis**: Positive Testing
- **Prekondisi**: ERD image sudah di-generate
- **Langkah**:
  1. Klik "Download" pada ERD image
- **Expected Output**: 
  - File PNG berhasil didownload
  - Filename: `erd_{nama_erd}.png`
  - File bisa dibuka
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-013: Akses ERD Builder
- **Jenis**: Positive Testing
- **Prekondisi**: Login sebagai advisor
- **Langkah**:
  1. Klik "ERD Builder" atau akses `/erd-builder`
- **Expected Output**: 
  - Halaman ERD Builder tampil
  - Canvas untuk drawing
  - Tools untuk add entity/relation
  - Zoom controls
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-014: Zoom In/Out pada ERD Builder
- **Jenis**: Positive Testing
- **Prekondisi**: Di halaman ERD Builder
- **Langkah**:
  1. Klik Zoom In (+)
  2. Klik Zoom Out (-)
- **Expected Output**: 
  - Canvas zoom sesuai aksi
  - Tidak ada distorsi
  - Smooth transition
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-015: Melihat Pending Requests
- **Jenis**: Positive Testing
- **Prekondisi**: Ada 3 request dengan status `pending`
- **Langkah**:
  1. Buka "Pending Requests"
- **Expected Output**: 
  - Menampilkan semua request pending
  - Menampilkan nama user, judul, deskripsi
  - Ada tombol "Assign to Me"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-016: Assign Request ke Diri Sendiri
- **Jenis**: Positive Testing
- **Prekondisi**: Ada pending request
- **Langkah**:
  1. Klik "Assign to Me" pada pending request
- **Expected Output**: 
  - Request status berubah ke `assigned`
  - Request pindah ke "My Assigned Requests"
  - advisor_id terisi dengan ID advisor
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-017: Melihat Assigned Requests Milik Sendiri
- **Jenis**: Positive Testing
- **Prekondisi**: Advisor memiliki 2 assigned request
- **Langkah**:
  1. Buka "My Assigned Requests"
- **Expected Output**: 
  - Menampilkan 2 request yang di-assign ke advisor
  - Tidak menampilkan request assigned ke advisor lain
  - Ada tombol "Complete"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-018: Complete Request
- **Jenis**: Positive Testing
- **Prekondisi**: Advisor memiliki assigned request
- **Langkah**:
  1. Klik "Complete" pada assigned request
  2. (Optional) Isi catatan completion
  3. Confirm
- **Expected Output**: 
  - Request status berubah ke `completed`
  - Request pindah ke history
  - User mendapat notifikasi (jika ada fitur)
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-019: Complete Request Milik Advisor Lain
- **Jenis**: Security Testing
- **Prekondisi**: Login sebagai advisor A
- **Langkah**:
  1. Dapatkan ID request yang assigned ke advisor B
  2. PUT `/api/requests/{id}/complete`
- **Expected Output**: HTTP 403 Forbidden
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADV-020: User Akses Advisor Dashboard
- **Jenis**: Security Testing
- **Prekondisi**: Login sebagai role `user`
- **Langkah**:
  1. Akses `/advisor-dashboard`
- **Expected Output**: 
  - HTTP 403 Forbidden
  - Redirect ke user dashboard
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

### 4. MODUL ADMIN DASHBOARD

#### TC-ADM-001: Akses Dashboard Admin
- **Jenis**: Positive Testing
- **Prekondisi**: Login sebagai role `admin`
- **Langkah**:
  1. Login sebagai admin
  2. Akses `/admin-dashboard`
- **Expected Output**: 
  - Dashboard tampil dengan:
    - Statistics (total users, advisors, ERDs, requests)
    - Advisor Management
    - Advisor Monitoring
    - System Controls
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-002: Melihat Daftar Semua Advisor
- **Jenis**: Positive Testing
- **Prekondisi**: Database memiliki 5 advisor
- **Langkah**:
  1. Buka "Advisor Management"
- **Expected Output**: 
  - Menampilkan 5 advisor
  - Menampilkan username, email, status
  - Ada tombol Edit dan Delete
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-003: Tambah Advisor Baru
- **Jenis**: Positive Testing
- **Prekondisi**: Login sebagai admin
- **Langkah**:
  1. Klik "Add Advisor"
  2. Isi form:
     - Username: `newadvisor`
     - Email: `advisor@mail.com`
     - Password: `Advisor123!`
  3. Submit
- **Expected Output**: 
  - Advisor berhasil ditambahkan
  - Muncul di list advisor
  - Advisor bisa login
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-004: Tambah Advisor dengan Username Duplikat
- **Jenis**: Negative Testing
- **Prekondisi**: Username `advisor1` sudah ada
- **Langkah**:
  1. Tambah advisor dengan username `advisor1`
- **Expected Output**: Error "Username sudah digunakan"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-005: Edit Data Advisor
- **Jenis**: Positive Testing
- **Prekondisi**: Advisor `advisor1` ada
- **Langkah**:
  1. Klik "Edit" pada advisor1
  2. Ubah email menjadi `newemail@mail.com`
  3. Save
- **Expected Output**: 
  - Data advisor berhasil diupdate
  - Email berubah di database
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-006: Hapus Advisor
- **Jenis**: Positive Testing
- **Prekondisi**: Advisor `advisor1` ada
- **Langkah**:
  1. Klik "Delete" pada advisor1
  2. Konfirmasi delete
- **Expected Output**: 
  - Advisor berhasil dihapus
  - Data terhapus dari database
  - ERD milik advisor1 (handling: cascade/set null)
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-007: Melihat Statistics System
- **Jenis**: Positive Testing
- **Prekondisi**: Database berisi data
- **Langkah**:
  1. Buka "Statistics"
- **Expected Output**: 
  - Total Users: [angka]
  - Total Advisors: [angka]
  - Total ERDs: [angka]
  - Total Requests: [angka]
  - Request by status (pending/assigned/completed)
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-008: Melihat Advisor Monitoring
- **Jenis**: Positive Testing
- **Prekondisi**: Ada aktivitas advisor
- **Langkah**:
  1. Buka "Advisor Monitoring"
- **Expected Output**: 
  - List advisor dengan:
    - Jumlah ERD yang dibuat
    - Jumlah request ditangani
    - Completion rate
    - Last activity
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-009: Reload System
- **Jenis**: Positive Testing
- **Prekondisi**: Login sebagai admin
- **Langkah**:
  1. Klik "Reload System"
  2. Konfirmasi
- **Expected Output**: 
  - System berhasil di-reload
  - TF-IDF matrix di-reindex
  - Notification sukses
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-010: User Akses Admin Dashboard
- **Jenis**: Security Testing
- **Prekondisi**: Login sebagai role `user`
- **Langkah**:
  1. Akses `/admin-dashboard`
- **Expected Output**: 
  - HTTP 403 Forbidden
  - Redirect ke user dashboard
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-ADM-011: Advisor Akses Admin Dashboard
- **Jenis**: Security Testing
- **Prekondisi**: Login sebagai role `advisor`
- **Langkah**:
  1. Akses `/admin-dashboard`
- **Expected Output**: HTTP 403 Forbidden
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

### 5. API TESTING

#### TC-API-001: Get Semua ERD Tanpa Autentikasi
- **Jenis**: Negative Testing / Security
- **Prekondisi**: Tidak ada token
- **Langkah**:
  1. GET `/api/all-erds` tanpa Authorization header
- **Expected Output**: 
  - HTTP 401 Unauthorized
  - ATAU berhasil jika endpoint public
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-API-002: Method Not Allowed
- **Jenis**: Negative Testing
- **Prekondisi**: Login
- **Langkah**:
  1. GET `/api/search-erd` (harusnya POST)
- **Expected Output**: HTTP 405 Method Not Allowed
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-API-003: Invalid JSON Body
- **Jenis**: Negative Testing
- **Prekondisi**: Login sebagai advisor
- **Langkah**:
  1. POST `/api/add-erd` dengan body: `{invalid json}`
- **Expected Output**: HTTP 400 Bad Request
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-API-004: Invalid ID Format
- **Jenis**: Negative Testing
- **Prekondisi**: Login
- **Langkah**:
  1. PUT `/api/erd/invalid-id-format`
- **Expected Output**: HTTP 400 Bad Request
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-API-005: Resource Not Found
- **Jenis**: Negative Testing
- **Prekondisi**: Login
- **Langkah**:
  1. DELETE `/api/erd/999999` (ID tidak ada)
- **Expected Output**: HTTP 404 Not Found
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-API-006: Large Payload Upload
- **Jenis**: Boundary Value Analysis
- **Prekondisi**: Login sebagai advisor
- **Langkah**:
  1. Upload file ERD > 10MB
- **Expected Output**: Error "File size limit exceeded"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-API-007: Concurrent Request Handling
- **Jenis**: Performance Testing
- **Prekondisi**: 10 user login
- **Langkah**:
  1. Kirim 10 search request bersamaan
- **Expected Output**: 
  - Semua request berhasil
  - Response time reasonable
  - No race condition
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-API-008: Rate Limiting
- **Jenis**: Performance / Security Testing
- **Prekondisi**: Login
- **Langkah**:
  1. Kirim 100 requests dalam 1 detik
- **Expected Output**: 
  - Rate limit triggered (HTTP 429)
  - ATAU semua sukses jika tidak ada rate limit
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

### 6. INTEGRATION TESTING

#### TC-INT-001: End-to-End User Journey
- **Jenis**: Integration Testing
- **Langkah**:
  1. Register sebagai user baru
  2. Login
  3. Search ERD dengan keyword
  4. Create request konsultasi
  5. View my requests
- **Expected Output**: Semua flow berhasil tanpa error
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-INT-002: End-to-End Advisor Journey
- **Jenis**: Integration Testing
- **Langkah**:
  1. Login sebagai advisor
  2. Add ERD baru
  3. Generate ERD image
  4. Download ERD image
  5. Assign pending request
  6. Complete assigned request
- **Expected Output**: Semua flow berhasil
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-INT-003: Request Flow Complete
- **Jenis**: State Transition Testing
- **Langkah**:
  1. User create request (status: pending)
  2. Advisor assign request (status: assigned)
  3. Advisor complete request (status: completed)
- **Expected Output**: 
  - State transition sesuai
  - Data konsisten di semua tahap
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-INT-004: Cross-Role Data Sync
- **Jenis**: Integration Testing
- **Langkah**:
  1. Admin create advisor
  2. Advisor create ERD
  3. User search dan menemukan ERD
- **Expected Output**: Data sinkron di semua role
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

### 7. PERFORMANCE TESTING

#### TC-PERF-001: Search Response Time dengan 1000+ ERD
- **Jenis**: Performance Testing
- **Prekondisi**: Database berisi 1000+ ERD
- **Langkah**:
  1. Search dengan keyword umum
  2. Ukur response time
- **Expected Output**: Response time < 3 detik
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-PERF-002: TF-IDF Calculation Performance
- **Jenis**: Performance Testing
- **Prekondisi**: Database berisi banyak ERD dengan teks panjang
- **Langkah**:
  1. Trigger TF-IDF recalculation (reload system)
- **Expected Output**: Proses selesai < 10 detik
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-PERF-003: Load Testing - 50 Concurrent Logins
- **Jenis**: Load Testing
- **Prekondisi**: 50 user accounts
- **Langkah**:
  1. 50 users login bersamaan
- **Expected Output**: 
  - Semua login berhasil
  - No timeout
  - Server stable
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-PERF-004: Page Load Time
- **Jenis**: Performance Testing
- **Langkah**:
  1. Load user/advisor/admin dashboard
  2. Ukur waktu load
- **Expected Output**: Page load < 2 detik
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

### 8. SECURITY TESTING

#### TC-SEC-001: XSS Attack pada Form Input
- **Jenis**: Security Testing
- **Test Data**: `<script>alert('XSS')</script>`
- **Lokasi**: Register, Login, Add ERD, Search
- **Expected Output**: Input di-sanitize, script tidak execute
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-SEC-002: SQL Injection pada Search
- **Jenis**: Security Testing
- **Test Data**: `' OR '1'='1`
- **Expected Output**: Query di-escape/parameterized
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-SEC-003: CSRF Token Validation
- **Jenis**: Security Testing
- **Langkah**:
  1. Submit form tanpa CSRF token (jika ada implementasi)
- **Expected Output**: Error "CSRF token missing"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-SEC-004: JWT Token Manipulation
- **Jenis**: Security Testing
- **Langkah**:
  1. Modify JWT payload (ubah role user ke admin)
  2. Akses admin endpoint
- **Expected Output**: Error "Invalid token signature"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-SEC-005: Password Hashing
- **Jenis**: Security Testing
- **Langkah**:
  1. Register user
  2. Check database password storage
- **Expected Output**: Password di-hash (bcrypt/argon2), tidak plain text
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-SEC-006: Unauthorized File Access
- **Jenis**: Security Testing
- **Langkah**:
  1. Akses `/static/image/erd_xxx.png` tanpa login
- **Expected Output**: 
  - File accessible jika public
  - 401/403 jika restricted
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-SEC-007: Directory Traversal Attack
- **Jenis**: Security Testing
- **Langkah**:
  1. Download dengan path: `../../etc/passwd`
- **Expected Output**: Error "Path traversal blocked"
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

#### TC-SEC-008: Privilege Escalation
- **Jenis**: Security Testing
- **Langkah**:
  1. Login sebagai user
  2. Modify token role dari user ke admin
  3. Akses admin endpoints
- **Expected Output**: 
  - Token invalid
  - 403 Forbidden pada admin endpoint
- **Actual Output**: [Diisi saat testing]
- **Status**: [ ] Pass [ ] Fail

---

## 📈 Summary Template

### Total Test Cases: 82
- Authentication: 13
- User Dashboard: 11
- Advisor Dashboard: 20
- Admin Dashboard: 11
- API Testing: 8
- Integration Testing: 4
- Performance Testing: 4
- Security Testing: 8

### Hasil Pengujian:
- **Total Pass**: [ ]
- **Total Fail**: [ ]
- **Success Rate**: [ ]%

### Bug/Issue Found:
| ID | Severity | Deskripsi | Status |
|----|----------|-----------|--------|
|    |          |           |        |

---

## 📝 Catatan Tambahan
- [Tambahkan catatan khusus selama testing]

---

**Generated**: 28 November 2025
**Last Updated**: [Update date]
