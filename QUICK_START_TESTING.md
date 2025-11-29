# Quick Start: Testing Sistem Rekomendasi ERD

## 🚀 Panduan Cepat (5 Menit)

### Langkah 1: Persiapan

Pastikan:
- ✅ MongoDB running
- ✅ Database sudah terisi dengan ERD
- ✅ File `ground_truth_dataset.json` ada (sudah disediakan dengan 30 test queries)

### Langkah 2: Jalankan Pengujian

```bash
# Dari root directory project
python test_recommendation_metrics.py
```

**Output yang dihasilkan:**
- `test_results_metrics_YYYYMMDD_HHMMSS.json` - Hasil detail dalam JSON
- `test_report_metrics_YYYYMMDD_HHMMSS.md` - Laporan readable dalam Markdown

### Langkah 3: Analisis Hasil

```bash
# Jalankan analisis lanjutan
python analyze_test_results.py
```

**Output:**
- Confusion Matrix
- Failure Cases Analysis (False Positives & False Negatives)
- Best/Worst Performing Queries
- Performance by Query Difficulty
- `test_results_metrics_*_analysis.txt` - Full analysis report

### Langkah 4: Lihat Hasil

Buka file laporan Markdown untuk membaca hasil:
```bash
# Windows
notepad test_report_metrics_*.md

# Or open in IDE/text editor
```

---

## 📊 Metrik yang Diukur

| Metrik | Penjelasan Singkat |
|--------|-------------------|
| **Precision@K** | Seberapa akurat rekomendasi (% relevan dari yang direkomendasikan) |
| **Recall@K** | Seberapa lengkap rekomendasi (% relevan yang berhasil ditemukan) |
| **F1-Score@K** | Keseimbangan antara Precision dan Recall |
| **MAP** | Kualitas ranking secara keseluruhan |
| **MRR** | Seberapa cepat menemukan hasil relevan pertama |

---

## 📈 Interpretasi Hasil Cepat

### Precision@5
- `> 0.7` ✅ Excellent - Hampir semua rekomendasi relevan
- `0.5 - 0.7` ✔️ Good - Sebagian besar rekomendasi relevan
- `0.3 - 0.5` ⚠️ Fair - Banyak rekomendasi tidak relevan
- `< 0.3` ❌ Poor - Sistem perlu improvement

### Recall@5
- `> 0.6` ✅ Excellent - Sistem menemukan sebagian besar ERD relevan
- `0.4 - 0.6` ✔️ Good - Sistem menemukan banyak ERD relevan
- `0.2 - 0.4` ⚠️ Fair - Sistem melewatkan banyak ERD relevan
- `< 0.2` ❌ Poor - Sistem miss banyak hasil relevan

### MAP (Mean Average Precision)
- `> 0.7` ✅ Excellent - ERD relevan selalu di posisi atas
- `0.5 - 0.7` ✔️ Good - Ranking cukup baik
- `0.3 - 0.5` ⚠️ Fair - Ranking perlu improvement
- `< 0.3` ❌ Poor - ERD relevan sering di posisi bawah

---

## 🔧 Kustomisasi

### Ubah Nilai K

Edit `test_recommendation_metrics.py` baris ~433:

```python
# Default: K=[5, 10]
results = tester.run_test(k_values=[5, 10], min_similarity=0.0)

# Ubah menjadi: K=[3, 5, 10, 20]
results = tester.run_test(k_values=[3, 5, 10, 20], min_similarity=0.0)
```

### Ubah Similarity Threshold

```python
# Hanya tampilkan rekomendasi dengan similarity >= 0.1
results = tester.run_test(k_values=[5, 10], min_similarity=0.1)
```

### Tambah Test Query Baru

Edit `ground_truth_dataset.json`:

```json
{
  "query_id": 31,
  "query": "query baru anda",
  "description": "Deskripsi query",
  "relevant_erds": [
    "nama_erd_yang_relevan"
  ],
  "irrelevant_erds": [
    "nama_erd_yang_tidak_relevan"
  ]
}
```

---

## 🐛 Troubleshooting

### Problem: Semua metrik = 0.0

**Solusi:**
1. Cek nama ERD di `ground_truth_dataset.json` match dengan database
2. Pastikan database tidak kosong
3. Turunkan `min_similarity` ke 0.0

### Problem: "No module named 'services'"

**Solusi:**
```bash
# Pastikan menjalankan dari root directory
cd C:\Users\DhafL\Desktop\ERD-Recommendation-With-TF-IDF
python test_recommendation_metrics.py
```

### Problem: MongoDB Connection Error

**Solusi:**
1. Pastikan MongoDB running
2. Check `config.py` untuk URI yang benar
3. Test koneksi manual

---

## 📖 Dokumentasi Lengkap

Untuk penjelasan detail tentang setiap metrik dan best practices:
👉 **Baca `TESTING_METRICS_README.md`**

---

## 💡 Tips untuk Skripsi/Paper

### Yang Harus Dilaporkan:

1. **Metodologi**
   - Jumlah test queries: 30 queries
   - Sumber ground truth: Manual labeling berdasarkan analisis ERD
   - K values yang diuji: 5 dan 10

2. **Hasil Utama** (dalam tabel)
   ```
   | Metrik    | K=5   | K=10  |
   |-----------|-------|-------|
   | Precision | 0.XXX | 0.XXX |
   | Recall    | 0.XXX | 0.XXX |
   | F1-Score  | 0.XXX | 0.XXX |
   | MAP       | 0.XXX |   -   |
   | MRR       | 0.XXX |   -   |
   ```

3. **Error Analysis**
   - Contoh False Positives dengan penjelasan
   - Contoh False Negatives dengan penjelasan
   - Insight: Kenapa sistem gagal di kasus tertentu

4. **Perbandingan** (jika ada)
   - Baseline: TF-IDF tanpa preprocessing
   - Proposed: TF-IDF dengan advanced preprocessing
   - Improvement: XX% peningkatan MAP

### Visualisasi yang Bagus:

1. Bar chart: Precision@K, Recall@K, F1@K
2. Line chart: Metrik vs K (K=1,3,5,10,20)
3. Heatmap: Confusion matrix
4. Scatter plot: Precision vs Recall

---

## ✅ Checklist Sebelum Laporan

- [ ] Jalankan `test_recommendation_metrics.py`
- [ ] Jalankan `analyze_test_results.py`
- [ ] Review hasil di file Markdown
- [ ] Catat metrik utama untuk tabel
- [ ] Screenshot atau copy confusion matrix
- [ ] Pilih 3-5 best/worst cases untuk dibahas
- [ ] Interpretasikan hasil (kenapa good/bad)
- [ ] Bandingkan dengan target/baseline

---

**Good luck dengan pengujian! 🎯**

Jika ada pertanyaan, refer ke `TESTING_METRICS_README.md` untuk dokumentasi lengkap.
