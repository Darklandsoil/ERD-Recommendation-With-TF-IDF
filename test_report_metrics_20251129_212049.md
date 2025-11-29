# Laporan Pengujian Sistem Rekomendasi ERD

## Informasi Pengujian

- **Tanggal**: 2025-11-29 21:20:49
- **Total Queries**: 50
- **Nilai K**: [5, 10]
- **Minimum Similarity**: 0.0

## Ringkasan Hasil

### Metrik Rata-rata untuk Setiap K

| K | Precision@K | Recall@K | F1-Score@K |
|---|-------------|----------|------------|
| 5 | 0.2080 | 1.0000 | 0.3429 |
| 10 | 0.1060 | 1.0200 | 0.1915 |

### Metrik Overall

- **MAP (Mean Average Precision)**: 0.9667
- **MRR (Mean Reciprocal Rank)**: 0.9600

## Interpretasi Hasil

### Precision@K
Precision@K mengukur **seberapa relevan** rekomendasi yang diberikan sistem.
- Nilai tinggi (mendekati 1.0) = Sebagian besar rekomendasi relevan
- Nilai rendah (mendekati 0.0) = Banyak rekomendasi yang tidak relevan

### Recall@K
Recall@K mengukur **seberapa lengkap** sistem dalam menemukan ERD yang relevan.
- Nilai tinggi (mendekati 1.0) = Sistem berhasil menemukan sebagian besar ERD relevan
- Nilai rendah (mendekati 0.0) = Sistem melewatkan banyak ERD relevan

### F1-Score@K
F1-Score adalah **harmonic mean** dari Precision dan Recall, memberikan keseimbangan antara keduanya.
- Nilai tinggi = Sistem baik dalam precision maupun recall

### MAP (Mean Average Precision)
MAP mengukur **kualitas keseluruhan ranking** dari sistem rekomendasi.
- Mempertimbangkan posisi setiap ERD relevan dalam hasil rekomendasi
- Nilai tinggi = ERD relevan muncul di posisi atas

### MRR (Mean Reciprocal Rank)
MRR mengukur **seberapa cepat** sistem menemukan ERD relevan pertama.
- Nilai tinggi = ERD relevan pertama muncul di posisi atas
- Nilai rendah = ERD relevan pertama muncul di posisi bawah

## Detail Hasil Per Query

### Query 1: sistem mahasiswa dosen mata kuliah nilai semester

**Deskripsi**: Query tentang sistem universitas

**ERD Relevan**: universitas

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 0.500, RR: 0.500

**Top-5 Rekomendasi**:
1. sistem_informasi_akademik_universitas ✗
2. universitas ✓
3. sekolah ✗
4. erd_manajemen_sistem ✗
5. asuransi ✗

---

### Query 2: siswa guru kelas mata pelajaran nilai rapor

**Deskripsi**: Query tentang sistem sekolah

**ERD Relevan**: sekolah

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. sekolah ✓
2. bimbingan_belajar ✗
3. taman_kanak_kanak ✗
4. gym ✗
5. universitas ✗

---

### Query 3: peminjaman buku anggota perpustakaan denda

**Deskripsi**: Query tentang perpustakaan

**ERD Relevan**: perpustakaan, perpustakaan_daerah

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.400, Recall@5: 1.000, F1@5: 0.571
- Precision@10: 0.200, Recall@10: 1.000, F1@10: 0.333
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. perpustakaan_daerah ✓
2. perpustakaan ✓
3. koperasi ✗
4. bank ✗
5. rental_mobil ✗

---

### Query 4: peserta instruktur kursus materi sertifikat online

**Deskripsi**: Query tentang kursus online

**ERD Relevan**: kursus_online

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. kursus_online ✓
2. perpustakaan ✗
3. kantor ✗
4. sistem_informasi_akademik_universitas ✗
5. manajemen_sekolah ✗

---

### Query 5: tutor siswa paket belajar jadwal bimbingan

**Deskripsi**: Query tentang bimbingan belajar

**ERD Relevan**: bimbingan_belajar

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. bimbingan_belajar ✓
2. ekspedisi ✗
3. sekolah ✗
4. bioskop ✗
5. universitas ✗

---

### Query 6: anak taman kanak guru kegiatan orang tua

**Deskripsi**: Query tentang TK

**ERD Relevan**: taman_kanak_kanak

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. taman_kanak_kanak ✓
2. sekolah ✗
3. perpustakaan ✗
4. kantor ✗
5. sistem_informasi_akademik_universitas ✗

---

### Query 7: pasien dokter perawat ruangan rekam medis obat

**Deskripsi**: Query tentang rumah sakit

**ERD Relevan**: rumah_sakit

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. rumah_sakit ✓
2. apotek ✗
3. poliklinik ✗
4. laboratorium_klinik ✗
5. bimbingan_belajar ✗

---

### Query 8: obat supplier pelanggan resep penjualan apotek

**Deskripsi**: Query tentang apotek

**ERD Relevan**: apotek

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. apotek ✓
2. toko_bangunan ✗
3. supermarket ✗
4. rumah_sakit ✗
5. e_commerce ✗

---

### Query 9: pasien tes laboratorium hasil teknisi peralatan

**Deskripsi**: Query tentang laboratorium klinik

**ERD Relevan**: laboratorium_klinik

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. laboratorium_klinik ✓
2. service_center ✗
3. rumah_sakit ✗
4. gym ✗
5. poliklinik ✗

---

### Query 10: pasien dokter poliklinik kunjungan diagnosa

**Deskripsi**: Query tentang poliklinik

**ERD Relevan**: poliklinik

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 0.500, RR: 0.500

**Top-5 Rekomendasi**:
1. rumah_sakit ✗
2. poliklinik ✓
3. laboratorium_klinik ✗
4. service_center ✗
5. apotek ✗

---

### Query 11: produk pelanggan keranjang transaksi pengiriman online

**Deskripsi**: Query tentang e-commerce

**ERD Relevan**: e_commerce

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. e_commerce ✓
2. laundry ✗
3. salon ✗
4. pabrik ✗
5. real_estate ✗

---

### Query 12: barang kasir supplier member transaksi supermarket

**Deskripsi**: Query tentang supermarket

**ERD Relevan**: supermarket

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. supermarket ✓
2. gym ✗
3. laundry ✗
4. toko_bangunan ✗
5. real_estate ✗

---

### Query 13: menu pelanggan meja pegawai pesanan restoran bahan baku

**Deskripsi**: Query tentang restoran

**ERD Relevan**: restoran

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. restoran ✓
2. pabrik ✗
3. kantor ✗
4. apotek ✗
5. e_commerce ✗

---

### Query 14: kamar tamu reservasi hotel pembayaran check in

**Deskripsi**: Query tentang hotel

**ERD Relevan**: hotel

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. hotel ✓
2. kos_kosan ✗
3. perpajakan ✗
4. bimbingan_belajar ✗
5. rental_mobil ✗

---

### Query 15: pelanggan pakaian layanan laundry transaksi status cucian

**Deskripsi**: Query tentang laundry

**ERD Relevan**: laundry

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. laundry ✓
2. salon ✗
3. e_commerce ✗
4. real_estate ✗
5. hotel ✗

---

### Query 16: kendaraan booking rental mobil pengembalian pembayaran

**Deskripsi**: Query tentang rental mobil

**ERD Relevan**: rental_mobil

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. rental_mobil ✓
2. perpustakaan ✗
3. perpajakan ✗
4. kos_kosan ✗
5. bimbingan_belajar ✗

---

### Query 17: penerbangan penumpang tiket maskapai gate bandara

**Deskripsi**: Query tentang bandara

**ERD Relevan**: bandara

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. bandara ✓
2. bioskop ✗
3. perpustakaan ✗
4. kantor ✗
5. sistem_informasi_akademik_universitas ✗

---

### Query 18: paket pengirim penerima tracking kurir ekspedisi

**Deskripsi**: Query tentang ekspedisi

**ERD Relevan**: ekspedisi

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. ekspedisi ✓
2. bimbingan_belajar ✗
3. e_commerce ✗
4. laboratorium_klinik ✗
5. perpustakaan ✗

---

### Query 19: nasabah rekening transaksi pinjaman kartu kredit bank

**Deskripsi**: Query tentang bank

**ERD Relevan**: bank

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. bank ✓
2. perpustakaan_daerah ✗
3. laundry ✗
4. perpustakaan ✗
5. koperasi ✗

---

### Query 20: anggota simpanan pinjaman angsuran dividen koperasi

**Deskripsi**: Query tentang koperasi

**ERD Relevan**: koperasi

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. koperasi ✓
2. perpustakaan_daerah ✗
3. perpustakaan ✗
4. bank ✗
5. kantor ✗

---

### Query 21: nasabah polis premi klaim agen asuransi

**Deskripsi**: Query tentang asuransi

**ERD Relevan**: asuransi

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. asuransi ✓
2. bank ✗
3. ekspedisi ✗
4. real_estate ✗
5. perpustakaan ✗

---

### Query 22: wajib pajak npwp pembayaran pelaporan tunggakan

**Deskripsi**: Query tentang perpajakan

**ERD Relevan**: perpajakan

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. perpajakan ✓
2. kos_kosan ✗
3. bimbingan_belajar ✗
4. rental_mobil ✗
5. hotel ✗

---

### Query 23: penduduk nik ktp kartu keluarga surat keterangan kelurahan

**Deskripsi**: Query tentang kelurahan

**ERD Relevan**: kelurahan

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. kelurahan ✓
2. bank ✗
3. ekspedisi ✗
4. laboratorium_klinik ✗
5. perpustakaan ✗

---

### Query 24: buku anggota peminjaman denda kategori perpustakaan daerah

**Deskripsi**: Query tentang perpustakaan daerah

**ERD Relevan**: perpustakaan_daerah, perpustakaan

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.400, Recall@5: 1.000, F1@5: 0.571
- Precision@10: 0.200, Recall@10: 1.000, F1@10: 0.333
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. perpustakaan_daerah ✓
2. perpustakaan ✓
3. koperasi ✗
4. bank ✗
5. rental_mobil ✗

---

### Query 25: properti pembeli agen transaksi cicilan real estate

**Deskripsi**: Query tentang real estate

**ERD Relevan**: real_estate

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. real_estate ✓
2. laundry ✗
3. ekspedisi ✗
4. e_commerce ✗
5. poliklinik ✗

---

### Query 26: kamar penyewa pembayaran fasilitas kos kosan

**Deskripsi**: Query tentang kos-kosan

**ERD Relevan**: kos_kosan

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. kos_kosan ✓
2. hotel ✗
3. rental_mobil ✗
4. perpajakan ✗
5. bimbingan_belajar ✗

---

### Query 27: film studio jadwal tayang tiket bioskop pelanggan

**Deskripsi**: Query tentang bioskop

**ERD Relevan**: bioskop

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. bioskop ✓
2. bandara ✗
3. bimbingan_belajar ✗
4. apotek ✗
5. e_commerce ✗

---

### Query 28: member trainer kelas peralatan membership gym fitness

**Deskripsi**: Query tentang gym

**ERD Relevan**: gym

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. gym ✓
2. supermarket ✗
3. sekolah ✗
4. taman_kanak_kanak ✗
5. laboratorium_klinik ✗

---

### Query 29: produk bahan baku produksi pegawai mesin pabrik manufaktur

**Deskripsi**: Query tentang pabrik

**ERD Relevan**: pabrik

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. pabrik ✓
2. restoran ✗
3. e_commerce ✗
4. kantor ✗
5. salon ✗

---

### Query 30: material supplier pelanggan penjualan proyek toko bangunan

**Deskripsi**: Query tentang toko bangunan

**ERD Relevan**: toko_bangunan

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. toko_bangunan ✓
2. apotek ✗
3. supermarket ✗
4. e_commerce ✗
5. service_center ✗

---

### Query 31: pelanggan perangkat teknisi perbaikan sparepart service center

**Deskripsi**: Query tentang service center

**ERD Relevan**: service_center

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. service_center ✓
2. laboratorium_klinik ✗
3. apotek ✗
4. e_commerce ✗
5. toko_bangunan ✗

---

### Query 32: pelanggan layanan stylist appointment produk salon barbershop

**Deskripsi**: Query tentang salon

**ERD Relevan**: salon

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. salon ✓
2. e_commerce ✗
3. laundry ✗
4. pabrik ✗
5. hotel ✗

---

### Query 33: pegawai departemen proyek tugas kantor

**Deskripsi**: Query tentang kantor

**ERD Relevan**: kantor

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 0.500, RR: 0.500

**Top-5 Rekomendasi**:
1. perpustakaan ✗
2. kantor ✓
3. toko_bangunan ✗
4. pabrik ✗
5. restoran ✗

---

### Query 34: mahasiswa nim jurusan krs dosen mata kuliah kampus

**Deskripsi**: Query spesifik universitas dengan detail

**ERD Relevan**: universitas

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. universitas ✓
2. sistem_informasi_akademik_universitas ✗
3. sekolah ✗
4. perpustakaan ✗
5. kantor ✗

---

### Query 35: pasien rawat inap dokter spesialis kamar rumah sakit

**Deskripsi**: Query spesifik rumah sakit

**ERD Relevan**: rumah_sakit

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.200, Recall@10: 2.000, F1@10: 0.364
- AP: 1.333, RR: 1.000

**Top-5 Rekomendasi**:
1. rumah_sakit ✓
2. poliklinik ✗
3. kos_kosan ✗
4. laboratorium_klinik ✗
5. hotel ✗

---

### Query 36: transaksi pembayaran online keranjang belanja produk

**Deskripsi**: Query e-commerce dengan pembayaran

**ERD Relevan**: e_commerce

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. e_commerce ✓
2. pabrik ✗
3. laundry ✗
4. real_estate ✗
5. salon ✗

---

### Query 37: pemesanan kamar hotel check in check out tamu

**Deskripsi**: Query hotel dengan reservasi

**ERD Relevan**: hotel

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. hotel ✓
2. kos_kosan ✗
3. perpustakaan ✗
4. kantor ✗
5. sistem_informasi_akademik_universitas ✗

---

### Query 38: penerbangan tiket pesawat boarding pass maskapai

**Deskripsi**: Query bandara dengan penerbangan

**ERD Relevan**: bandara

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. bandara ✓
2. bioskop ✗
3. perpustakaan ✗
4. kantor ✗
5. sistem_informasi_akademik_universitas ✗

---

### Query 39: rekening tabungan deposito bunga nasabah perbankan

**Deskripsi**: Query bank dengan produk perbankan

**ERD Relevan**: bank

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. bank ✓
2. asuransi ✗
3. koperasi ✗
4. perpustakaan ✗
5. kantor ✗

---

### Query 40: siswa nis guru wali kelas nilai ujian sekolah

**Deskripsi**: Query sekolah dengan detail siswa

**ERD Relevan**: sekolah

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. sekolah ✓
2. taman_kanak_kanak ✗
3. manajemen_sekolah ✗
4. bimbingan_belajar ✗
5. gym ✗

---

### Query 41: obat resep dokter stok harga apotek farmasi

**Deskripsi**: Query apotek dengan detail obat

**ERD Relevan**: apotek

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. apotek ✓
2. rumah_sakit ✗
3. poliklinik ✗
4. laboratorium_klinik ✗
5. pabrik ✗

---

### Query 42: tes darah urine laboratorium hasil pemeriksaan

**Deskripsi**: Query laboratorium dengan jenis tes

**ERD Relevan**: laboratorium_klinik

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. laboratorium_klinik ✓
2. rumah_sakit ✗
3. poliklinik ✗
4. perpustakaan ✗
5. kantor ✗

---

### Query 43: barang stok kasir struk pembayaran minimarket

**Deskripsi**: Query supermarket dengan transaksi

**ERD Relevan**: supermarket

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. supermarket ✓
2. perpajakan ✗
3. kos_kosan ✗
4. bimbingan_belajar ✗
5. rental_mobil ✗

---

### Query 44: menu makanan pesanan meja waiters dapur restoran

**Deskripsi**: Query restoran dengan detail operasional

**ERD Relevan**: restoran

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. restoran ✓
2. perpustakaan ✗
3. kantor ✗
4. sistem_informasi_akademik_universitas ✗
5. manajemen_sekolah ✗

---

### Query 45: mobil sewa rental harian mingguan sopir

**Deskripsi**: Query rental mobil dengan detail sewa

**ERD Relevan**: rental_mobil

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 0.500, RR: 0.500

**Top-5 Rekomendasi**:
1. kos_kosan ✗
2. rental_mobil ✓
3. perpustakaan ✗
4. kantor ✗
5. sistem_informasi_akademik_universitas ✗

---

### Query 46: paket resi pengiriman alamat kurir tracking ekspedisi

**Deskripsi**: Query ekspedisi dengan tracking

**ERD Relevan**: ekspedisi

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. ekspedisi ✓
2. bimbingan_belajar ✗
3. e_commerce ✗
4. laboratorium_klinik ✗
5. sistem_informasi_akademik_universitas ✗

---

### Query 47: anggota simpanan wajib sukarela pinjaman lunak koperasi

**Deskripsi**: Query koperasi dengan jenis simpanan

**ERD Relevan**: koperasi

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. koperasi ✓
2. perpustakaan_daerah ✗
3. perpustakaan ✗
4. perpajakan ✗
5. bank ✗

---

### Query 48: polis asuransi jiwa kesehatan premi bulanan klaim

**Deskripsi**: Query asuransi dengan jenis polis

**ERD Relevan**: asuransi

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. asuransi ✓
2. perpustakaan ✗
3. kantor ✗
4. sistem_informasi_akademik_universitas ✗
5. manajemen_sekolah ✗

---

### Query 49: pajak spt tahunan npwp wajib pajak pelaporan

**Deskripsi**: Query perpajakan dengan SPT

**ERD Relevan**: perpajakan

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. perpajakan ✓
2. perpustakaan ✗
3. kantor ✗
4. sistem_informasi_akademik_universitas ✗
5. manajemen_sekolah ✗

---

### Query 50: ktp kk nik penduduk rt rw surat keterangan

**Deskripsi**: Query kelurahan dengan administrasi

**ERD Relevan**: kelurahan

**Jumlah Rekomendasi**: 10

**Metrik**:
- Precision@5: 0.200, Recall@5: 1.000, F1@5: 0.333
- Precision@10: 0.100, Recall@10: 1.000, F1@10: 0.182
- AP: 1.000, RR: 1.000

**Top-5 Rekomendasi**:
1. kelurahan ✓
2. ekspedisi ✗
3. bank ✗
4. laboratorium_klinik ✗
5. perpustakaan ✗

---

