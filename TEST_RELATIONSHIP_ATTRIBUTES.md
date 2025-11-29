# Test Case: Relationship Attributes untuk Many-to-Many

## Fitur Baru
Relasi dengan kardinalitas **many-to-many** kini dapat memiliki atribut sendiri yang akan ditampilkan di sekitar diamond shape.

## Cara Menggunakan

### 1. Buat Relasi Many-to-Many
- Tambah minimal 2 entitas (misal: `Mahasiswa` dan `Mata_Kuliah`)
- Buat relasi baru
- Pilih kardinalitas: **Many to Many**

### 2. Tambahkan Atribut Relasi
Setelah memilih many-to-many, akan muncul section baru:
```
⚡ Atribut Relasi (Many-to-Many):
Atribut yang melekat pada relasi ini

[Input field untuk atribut baru] [+]
```

### 3. Contoh Penggunaan

**Skenario: Mahasiswa mengambil Mata Kuliah**
- Entitas 1: `Mahasiswa` (id_mahasiswa, nama, jurusan)
- Entitas 2: `Mata_Kuliah` (kode_mk, nama_mk, sks)
- Relasi: `Mengambil` (many-to-many)
- **Atribut Relasi**: `nilai`, `semester`, `tahun_ajaran`

Hasilnya: Atribut `nilai`, `semester`, dan `tahun_ajaran` akan muncul di sekitar diamond "Mengambil"

## Visualisasi
```
Mahasiswa --N-- [Mengambil] --N-- Mata_Kuliah
                    |
            (nilai) (semester)
              (tahun_ajaran)
```

## Validasi Backend
- Atribut relasi **hanya diizinkan** untuk kardinalitas many-to-many
- Validasi otomatis di `ERDModel.validate()`
- Atribut relasi disertakan dalam TF-IDF untuk rekomendasi

## Test Steps

1. **Test UI Muncul**
   - Buat relasi dengan tipe selain many-to-many → UI atribut TIDAK muncul
   - Ubah ke many-to-many → UI atribut MUNCUL

2. **Test Tambah/Hapus Atribut**
   - Tambahkan atribut: `nilai`
   - Tambahkan atribut: `semester`
   - Hapus atribut: `nilai`
   - Hasil: Hanya `semester` yang tersisa

3. **Test Visualisasi**
   - Update preview
   - Atribut harus muncul sebagai ellipse di sekitar diamond
   - Garis penghubung: dashed line dengan warna abu-abu

4. **Test Persistence**
   - Simpan ERD dengan atribut relasi
   - Reload/Edit ERD
   - Atribut relasi harus tetap ada

5. **Test Validasi Backend**
   - Coba simpan relasi non-many-to-many dengan atribut → Harus ditolak
   - Coba simpan many-to-many dengan atribut → Harus berhasil

## Backend Changes
- `erd_model.py`: Validasi + TF-IDF processing
- `erd-builder.js`: UI form + visualisasi DOT

## Frontend Changes
- `addRelationship()`: Inisialisasi array `attributes`
- `renderRelationshipsForm()`: Conditional UI untuk many-to-many
- `addRelationshipAttribute()` & `removeRelationshipAttribute()`: Manajemen atribut
- `generateDOT()`: Render atribut relasi
- `distributeRelationshipAttributes()`: Positioning algoritma
- `loadERDForEdit()`: Load atribut dari database
