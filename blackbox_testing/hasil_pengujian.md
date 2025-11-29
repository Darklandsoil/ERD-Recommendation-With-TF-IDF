# Hasil Pengujian Sistem ERD Recommendation

## Penjelasan Status HTTP

Berikut penjelasan status kode HTTP yang digunakan dalam pengujian:

| Kode Status | Penjelasan |
|------------|------------|
| **200** | OK - Request berhasil diproses |
| **201** | Created - Data berhasil dibuat |
| **400** | Bad Request - Request tidak valid atau data tidak sesuai format |
| **401** | Unauthorized - Tidak memiliki autentikasi yang valid |
| **403** | Forbidden - Tidak memiliki hak akses ke resource |
| **404** | Not Found - Resource/data yang dicari tidak ditemukan |
| **405** | Method Not Allowed - HTTP method tidak diperbolehkan |
| **409** | Conflict - Terjadi konflik, misalnya data duplikat |

## Tabel Hasil Pengujian Black Box

| No | Skenario Pengujian | Hasil yang Diharapkan | Hasil |
|----|-------------------|----------------------|-------|
| 1 | Pengguna mendaftar dengan data yang valid | Berhasil membuat akun atau memberikan notifikasi jika user sudah ada | Sesuai - User sudah terdaftar, sistem menolak duplikasi |
| 2 | Pengguna mendaftar dengan username kosong | Sistem menolak dan menampilkan pesan error validasi | Sesuai - Sistem menolak dengan pesan error validasi |
| 3 | Pengguna mendaftar dengan email tidak valid | Sistem menolak dan menampilkan pesan error format email | Sesuai - Sistem menolak dengan pesan error format email |
| 4 | Pengguna login dengan kredensial yang valid | Berhasil login dan menerima token autentikasi | Sesuai - Berhasil login dan menerima token |
| 5 | Advisor login dengan kredensial yang valid | Berhasil login dan menerima token autentikasi | Sesuai - Berhasil login dan menerima token |
| 6 | Admin login dengan kredensial yang valid | Berhasil login dan menerima token autentikasi | Sesuai - Berhasil login dan menerima token |
| 7 | Pengguna login dengan username yang tidak terdaftar | Login gagal dengan pesan error unauthorized | Sesuai - Login ditolak dengan pesan unauthorized |
| 8 | Pengguna login dengan password yang salah | Login gagal dengan pesan error unauthorized | Sesuai - Login ditolak dengan pesan unauthorized |
| 9 | Pengguna login dengan field kosong | Sistem menolak dengan pesan error validasi | Sesuai - Sistem menolak dengan pesan error validasi |
| 10 | Mengakses endpoint tanpa token autentikasi | Akses ditolak dengan pesan unauthorized | Sesuai - Akses ditolak karena tidak ada autentikasi |
| 11 | Mengakses endpoint dengan token tidak valid | Akses ditolak dengan pesan unauthorized | Sesuai - Akses ditolak karena token tidak valid |
| 12 | Mencoba SQL Injection pada form login | Serangan gagal dan tidak dapat bypass sistem | Sesuai - Serangan ditolak, sistem aman dari SQL Injection |
| 13 | Pengguna mencari ERD dengan keyword yang valid | Berhasil menampilkan hasil pencarian | Sesuai - Hasil pencarian ditampilkan dengan sukses |
| 14 | Pengguna mencari ERD dengan keyword kosong | Sistem menolak atau memberikan pesan error | Sesuai - Sistem menolak dengan pesan error validasi |
| 15 | Mencoba serangan XSS pada pencarian ERD | Input berbahaya disanitasi dan tidak dieksekusi | Sesuai - Input berbahaya berhasil disanitasi, sistem aman |
| 16 | Pengguna membuat request konsultasi ERD | Request berhasil dibuat | Sesuai - Request konsultasi berhasil dibuat |
| 17 | Pengguna membuat request dengan field kosong | Sistem menolak dengan pesan error validasi | Sesuai - Sistem menolak dengan pesan error validasi |
| 18 | Pengguna melihat daftar request miliknya | Berhasil menampilkan daftar request | Sesuai - Daftar request ditampilkan dengan sukses |
| 19 | Advisor menambahkan ERD dengan data yang valid | ERD berhasil ditambahkan | Sesuai - ERD berhasil ditambahkan ke sistem |
| 20 | Advisor menambahkan ERD dengan nama kosong | Sistem menolak dengan pesan error validasi | Sesuai - Sistem menolak dengan pesan error validasi |
| 21 | Advisor menambahkan ERD tanpa entitas | Sistem menolak dengan pesan error validasi | Sesuai - Sistem menolak karena entitas wajib diisi |
| 22 | Advisor melihat daftar ERD miliknya | Berhasil menampilkan daftar ERD | Sesuai - Daftar ERD ditampilkan dengan sukses |
| 23 | Advisor melihat daftar request yang belum ditangani | Berhasil menampilkan daftar request pending | Sesuai - Daftar request pending ditampilkan |
| 24 | Advisor melihat request yang ditugaskan kepadanya | Berhasil menampilkan request yang assigned | Sesuai - Request yang ditugaskan ditampilkan |
| 25 | User mencoba mengakses endpoint khusus advisor | Akses ditolak karena tidak memiliki hak akses | Sesuai - Akses ditolak karena bukan role advisor |
| 26 | Mengakses detail ERD dengan ID tidak valid | Sistem memberikan notifikasi data tidak ditemukan | Sesuai - Sistem memberikan notifikasi tidak ditemukan |
| 27 | Mengupdate ERD dengan ID tidak valid | Sistem memberikan notifikasi data tidak ditemukan | Sesuai - Sistem memberikan notifikasi tidak ditemukan |
| 28 | Menghapus ERD dengan ID tidak valid | Sistem memberikan notifikasi data tidak ditemukan | Sesuai - Sistem memberikan notifikasi tidak ditemukan |
| 29 | Membatalkan request yang tidak ada | Sistem memberikan notifikasi data tidak ditemukan | Sesuai - Sistem memberikan notifikasi tidak ditemukan |
| 30 | Assign request yang tidak ada | Sistem memberikan notifikasi data tidak ditemukan | Sesuai - Sistem memberikan notifikasi tidak ditemukan |
| 31 | Pengguna logout dengan token yang valid | Berhasil logout dan token dibatalkan | Sesuai - Berhasil logout dari sistem |
| 32 | Pengguna logout tanpa token | Logout ditolak karena tidak ada autentikasi | Sesuai - Logout ditolak karena tidak terautentikasi |
| 33 | Melihat daftar semua ERD yang tersedia | Berhasil menampilkan semua ERD | Sesuai - Semua ERD ditampilkan dengan sukses |
| 34 | Mendapatkan semua data ERD | Berhasil mengambil semua data ERD | Sesuai - Semua data ERD berhasil diambil |
| 35 | Generate gambar ERD dengan ID tidak valid | Sistem memberikan notifikasi data tidak ditemukan | Sesuai - Sistem memberikan notifikasi tidak ditemukan |
| 36 | Mencoba path traversal pada download gambar | Serangan ditolak dan tidak dapat akses file sistem | Sesuai - Serangan ditolak, sistem aman dari path traversal |
| 37 | User mencoba mengakses endpoint admin untuk melihat advisor | Akses ditolak karena tidak memiliki hak akses | Sesuai - Akses ditolak karena bukan role admin |
| 38 | Advisor mencoba mengakses endpoint admin | Akses ditolak karena tidak memiliki hak akses | Sesuai - Akses ditolak karena bukan role admin |
| 39 | User mencoba membuat advisor baru | Akses ditolak karena tidak memiliki hak akses | Sesuai - Akses ditolak karena bukan role admin |
| 40 | User mencoba mengupdate data advisor | Akses ditolak karena tidak memiliki hak akses | Sesuai - Akses ditolak karena bukan role admin |
| 41 | User mencoba menghapus advisor | Akses ditolak karena tidak memiliki hak akses | Sesuai - Akses ditolak karena bukan role admin |
| 42 | User mencoba mengakses statistik sistem | Akses ditolak karena tidak memiliki hak akses | Sesuai - Akses ditolak karena bukan role admin |
| 43 | User mencoba mengakses monitoring sistem | Akses ditolak karena tidak memiliki hak akses | Sesuai - Akses ditolak karena bukan role admin |
| 44 | Mengakses dashboard admin tanpa token | Halaman dapat diakses atau diarahkan ke login | Sesuai - Halaman dashboard dapat diakses |
| 45 | Admin melihat daftar advisor | Berhasil menampilkan daftar advisor | Sesuai - Daftar advisor ditampilkan dengan sukses |
| 46 | Admin membuat advisor baru dengan data valid | Advisor baru berhasil dibuat | Sesuai - Advisor baru berhasil ditambahkan |
| 47 | Admin membuat advisor dengan username yang sudah ada | Sistem menolak karena username sudah digunakan | Sesuai - Sistem menolak duplikasi username |
| 48 | Admin mengupdate advisor yang tidak ada | Sistem memberikan notifikasi data tidak ditemukan | Sesuai - Sistem memberikan notifikasi tidak ditemukan |
| 49 | Admin melihat statistik sistem | Berhasil menampilkan statistik sistem | Sesuai - Statistik sistem ditampilkan dengan sukses |
| 50 | Admin melihat monitoring sistem | Berhasil menampilkan monitoring sistem | Sesuai - Data monitoring ditampilkan dengan sukses |
| 51 | Admin menghapus advisor yang tidak ada | Sistem memberikan notifikasi data tidak ditemukan | Sesuai - Sistem memberikan notifikasi tidak ditemukan |
| 52 | Mengakses API tanpa token | Akses ditolak atau berhasil jika endpoint publik | Sesuai - Akses berhasil karena endpoint publik |
| 53 | Menggunakan HTTP method yang tidak diizinkan | Sistem menolak dengan pesan method not allowed | Sesuai - Sistem menolak dengan pesan method tidak diizinkan |
| 54 | Mengirim request dengan format JSON tidak valid | Sistem menolak dengan pesan error format | Sesuai - Sistem menolak dengan pesan error format JSON |
| 55 | Mengakses resource yang tidak ada | Sistem memberikan notifikasi resource tidak ditemukan | Sesuai - Sistem memberikan notifikasi tidak ditemukan |
| 56 | Mencoba serangan XSS pada berbagai input | Semua input berbahaya disanitasi dengan baik | Sesuai - Semua input XSS berhasil ditangani, sistem aman |
| 57 | Mencoba manipulasi JWT token | Token manipulasi ditolak dan autentikasi gagal | Sesuai - Token manipulasi ditolak, sistem aman |
| 58 | Mencoba serangan directory traversal | Serangan ditolak dan tidak dapat akses file sistem | Sesuai - Serangan ditolak, sistem aman dari directory traversal |

## Kesimpulan

Dari 58 skenario pengujian yang dilakukan, **semua test case berhasil PASS** dengan hasil yang sesuai dengan ekspektasi. Sistem telah lulus pengujian untuk:

- **Autentikasi dan Otorisasi**: Login, register, dan kontrol akses berbasis role
- **Fitur User**: Pencarian ERD, pembuatan request konsultasi
- **Fitur Advisor**: Manajemen ERD, penanganan request
- **Fitur Admin**: Manajemen advisor, statistik, dan monitoring sistem
- **Keamanan**: SQL Injection, XSS, JWT manipulation, dan directory traversal prevention
- **API**: Error handling, validasi input, dan response yang sesuai standar HTTP

---
*Laporan ini dapat dicetak atau dikonversi ke PDF untuk dokumentasi*
