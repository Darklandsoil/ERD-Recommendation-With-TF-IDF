# Testing Framework untuk Sistem Rekomendasi ERD

## Overview

Framework ini digunakan untuk mengevaluasi performa sistem rekomendasi ERD menggunakan metrik-metrik standar Information Retrieval:
- **Precision@K** - Mengukur akurasi rekomendasi
- **Recall@K** - Mengukur kelengkapan rekomendasi
- **F1-Score@K** - Keseimbangan antara Precision dan Recall
- **MAP (Mean Average Precision)** - Kualitas ranking secara keseluruhan
- **MRR (Mean Reciprocal Rank)** - Seberapa cepat menemukan hasil relevan

## Struktur File

```
ERD-Recommendation-With-TF-IDF/
├── ground_truth_dataset.json         # Dataset ground truth (query + ERD relevan)
├── test_recommendation_metrics.py    # Script utama untuk pengujian
├── TESTING_METRICS_README.md         # Dokumentasi ini
└── test_results_metrics_*.json       # Hasil pengujian (generated)
└── test_report_metrics_*.md          # Laporan pengujian (generated)
```

## Ground Truth Dataset

### Format File: `ground_truth_dataset.json`

```json
[
  {
    "query_id": 1,
    "query": "sistem untuk mahasiswa dosen matakuliah nilai",
    "description": "Query tentang sistem akademik",
    "relevant_erds": [
      "sistem_informasi_akademik"
    ],
    "irrelevant_erds": [
      "perpustakaan",
      "rumah_sakit"
    ]
  }
]
```

### Field Explanation

- **query_id**: ID unik untuk setiap test query
- **query**: Text query yang akan diuji
- **description**: Deskripsi singkat tentang query
- **relevant_erds**: List ERD yang RELEVAN untuk query ini (ground truth)
- **irrelevant_erds**: List ERD yang TIDAK RELEVAN (untuk referensi)

### Cara Menambah Test Case Baru

1. Buka file `ground_truth_dataset.json`
2. Tambahkan object baru dengan format di atas
3. Pastikan `relevant_erds` berisi nama ERD yang benar-benar relevan

**Tips untuk membuat ground truth yang baik:**
- Pilih query yang representative dari use case nyata
- Labeling harus konsisten (jika A mirip B, keduanya harus di-label sama)
- Pertimbangkan partial relevance (ERD yang agak relevan)
- Minimal 20-30 test queries untuk hasil yang statistik signifikan

## Cara Menjalankan Pengujian

### 1. Persiapan

Pastikan database MongoDB sudah running dan berisi data ERD:

```bash
# Check MongoDB status
# Pastikan ada ERD di database
```

### 2. Jalankan Script

```bash
python test_recommendation_metrics.py
```

### 3. Output yang Dihasilkan

Script akan menghasilkan 2 file:

1. **`test_results_metrics_TIMESTAMP.json`** - Hasil lengkap dalam format JSON
2. **`test_report_metrics_TIMESTAMP.md`** - Laporan readable dalam Markdown

### 4. Kustomisasi Parameter

Edit di `test_recommendation_metrics.py` pada function `main()`:

```python
# Ubah nilai K
results = tester.run_test(k_values=[3, 5, 10], min_similarity=0.0)

# Ubah minimum similarity threshold
results = tester.run_test(k_values=[5, 10], min_similarity=0.1)
```

## Penjelasan Metrik

### 1. Precision@K

**Definisi**: Proporsi ERD relevan dalam top-K rekomendasi

**Formula**:
```
Precision@K = (Jumlah ERD relevan dalam top-K) / K
```

**Contoh**:
- Query: "mahasiswa dosen matakuliah"
- Top-5 rekomendasi: [sistem_akademik✓, perpustakaan✗, perpustakaan_kampus✓, rumah_sakit✗, bank✗]
- Precision@5 = 2/5 = 0.40

**Interpretasi**:
- P@5 = 1.0 → Semua 5 rekomendasi teratas relevan (sempurna)
- P@5 = 0.6 → 3 dari 5 rekomendasi relevan (cukup baik)
- P@5 = 0.2 → Hanya 1 dari 5 rekomendasi relevan (buruk)

**Kapan Precision Penting?**
- User hanya melihat beberapa hasil teratas
- False positive sangat tidak diinginkan
- Contoh: Rekomendasi produk e-commerce

### 2. Recall@K

**Definisi**: Proporsi ERD relevan yang berhasil ditemukan dalam top-K

**Formula**:
```
Recall@K = (Jumlah ERD relevan dalam top-K) / (Total ERD relevan)
```

**Contoh**:
- Query: "peminjaman buku perpustakaan"
- ERD relevan (ground truth): 4 ERD
- Top-5 rekomendasi berhasil menemukan: 3 ERD relevan
- Recall@5 = 3/4 = 0.75

**Interpretasi**:
- R@5 = 1.0 → Semua ERD relevan ditemukan dalam top-5
- R@5 = 0.75 → 75% ERD relevan ditemukan
- R@5 = 0.25 → Hanya 25% ERD relevan ditemukan

**Kapan Recall Penting?**
- Penting menemukan semua hasil relevan
- False negative sangat tidak diinginkan
- Contoh: Medical diagnosis, legal search

### 3. F1-Score@K

**Definisi**: Harmonic mean dari Precision dan Recall

**Formula**:
```
F1@K = 2 × (Precision@K × Recall@K) / (Precision@K + Recall@K)
```

**Mengapa Harmonic Mean?**
- Tidak bisa "cheat" dengan extreme values
- Jika P=0.9 dan R=0.1 → F1=0.18 (tidak 0.5)
- Mendorong keseimbangan antara P dan R

**Interpretasi**:
- F1@5 = 0.8 → Sistem baik dalam precision dan recall
- F1@5 = 0.3 → Ada imbalance, salah satu metrik rendah

### 4. MAP (Mean Average Precision)

**Definisi**: Rata-rata dari Average Precision untuk semua queries

**Formula**:
```
AP = (1/|relevant|) × Σ(Precision@k × rel(k))
MAP = (1/Q) × Σ AP(q)

dimana:
- rel(k) = 1 jika item rank-k relevan, 0 jika tidak
- Q = total queries
```

**Contoh Perhitungan AP**:

Query: "sistem akademik"
Rekomendasi: [A✗, B✓, C✗, D✓, E✓]
Relevan: B, D, E

```
AP = (1/3) × [(1/2) + (2/4) + (3/5)]
   = (1/3) × [0.5 + 0.5 + 0.6]
   = (1/3) × 1.6
   = 0.533
```

**Interpretasi**:
- MAP = 0.9 → ERD relevan selalu muncul di posisi atas
- MAP = 0.5 → ERD relevan tersebar di berbagai posisi
- MAP = 0.1 → ERD relevan jarang muncul di atas

**Mengapa MAP Penting?**
- Mempertimbangkan **urutan** rekomendasi
- ERD relevan di rank-1 lebih baik dari rank-10
- Metrik standar untuk information retrieval

### 5. MRR (Mean Reciprocal Rank)

**Definisi**: Rata-rata dari reciprocal rank hasil relevan pertama

**Formula**:
```
RR = 1 / rank_of_first_relevant_item
MRR = (1/Q) × Σ RR(q)
```

**Contoh**:
- Query 1: Relevan pertama di rank-2 → RR = 1/2 = 0.5
- Query 2: Relevan pertama di rank-1 → RR = 1/1 = 1.0
- Query 3: Relevan pertama di rank-5 → RR = 1/5 = 0.2
- MRR = (0.5 + 1.0 + 0.2) / 3 = 0.567

**Interpretasi**:
- MRR = 1.0 → Hasil relevan selalu di rank-1
- MRR = 0.5 → Hasil relevan rata-rata di rank-2
- MRR = 0.1 → Hasil relevan rata-rata di rank-10

**Kapan MRR Penting?**
- User biasanya hanya klik hasil pertama yang relevan
- Fokus pada "time to success"
- Cocok untuk search engines, Q&A systems

## Trade-off Antar Metrik

### Precision vs Recall

```
High Precision, Low Recall:
→ Sistem konservatif, hanya merekomendasikan yang sangat yakin
→ Sedikit false positive, banyak false negative

Low Precision, High Recall:
→ Sistem agresif, merekomendasikan banyak hal
→ Banyak false positive, sedikit false negative
```

**Strategi**:
- Aplikasi e-commerce → Prioritaskan Precision (jangan ganggu user dengan produk tidak relevan)
- Aplikasi medical search → Prioritaskan Recall (jangan sampai miss informasi penting)
- General search → Balance dengan F1-Score

### Nilai K yang Optimal

- **K=3** → User sangat impatient, hanya lihat 3 hasil teratas
- **K=5** → Standard untuk mobile apps
- **K=10** → Standard untuk desktop web search
- **K=20+** → Academic research, comprehensive search

## Benchmark dan Target

### Target Performa yang Baik

Berdasarkan paper akademik di bidang Information Retrieval:

| Metrik | Poor | Fair | Good | Excellent |
|--------|------|------|------|-----------|
| P@5 | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| R@5 | < 0.2 | 0.2-0.4 | 0.4-0.6 | > 0.6 |
| F1@5 | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| MAP | < 0.3 | 0.3-0.5 | 0.5-0.7 | > 0.7 |
| MRR | < 0.4 | 0.4-0.6 | 0.6-0.8 | > 0.8 |

**Catatan**: Target ini bisa berbeda tergantung domain dan kesulitan task.

## Analisis Hasil

### 1. Jika Precision Tinggi, Recall Rendah

**Masalah**: Sistem terlalu konservatif

**Solusi**:
- Turunkan `min_similarity` threshold
- Perluas vocabulary TF-IDF (tambah features)
- Pertimbangkan query expansion

### 2. Jika Precision Rendah, Recall Tinggi

**Masalah**: Sistem terlalu agresif / noise

**Solusi**:
- Naikkan `min_similarity` threshold
- Improve text preprocessing (stopwords, stemming)
- Pertimbangkan re-ranking dengan model lain

### 3. Jika MAP Rendah tapi Recall Tinggi

**Masalah**: ERD relevan ada, tapi rankingnya buruk

**Solusi**:
- Improve scoring function (TF-IDF weights)
- Pertimbangkan learning to rank
- Add domain-specific boosting

### 4. Jika MRR Rendah

**Masalah**: User harus scroll banyak untuk menemukan hasil relevan

**Solusi**:
- Prioritaskan popular/high-quality ERDs
- Add click-through rate data untuk re-ranking
- Personalization based on user history

## Confusion Matrix untuk Rekomendasi

Untuk analisis lebih detail, hitung confusion matrix:

```
                    Predicted Relevant  |  Predicted Not Relevant
                    -------------------|------------------------
Actual Relevant     True Positive (TP)  |  False Negative (FN)
Actual Not Relevant False Positive (FP) |  True Negative (TN)
```

**Dari Precision & Recall**:
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)

## Best Practices

### 1. Ground Truth Quality

✅ **DO**:
- Minimal 20-30 queries untuk hasil statistik signifikan
- Diverse queries (berbagai domain ERD)
- Labeling konsisten
- Review oleh multiple annotators

❌ **DON'T**:
- Bias terhadap ERD tertentu
- Label based on ERD name saja (baca kontennya)
- Terlalu sedikit queries (< 10)

### 2. Interpretasi Hasil

✅ **DO**:
- Compare dengan baseline
- Lihat trend improvement over time
- Analyze failure cases
- Segment analysis (per domain, per query type)

❌ **DON'T**:
- Hanya lihat satu metrik
- Optimize untuk test set (overfitting)
- Ignore statistical significance

### 3. Reporting untuk Skripsi/Paper

**Include**:
1. Metodologi ground truth collection
2. Inter-annotator agreement (jika ada multiple annotators)
3. Table hasil untuk multiple K values
4. Statistical significance testing
5. Error analysis dengan contoh spesifik
6. Comparison dengan baseline methods

## Troubleshooting

### Error: "No module named 'services'"

**Solution**:
```bash
# Make sure you run from project root
cd ERD-Recommendation-With-TF-IDF
python test_recommendation_metrics.py
```

### Error: "File ground_truth_dataset.json not found"

**Solution**:
```bash
# Make sure ground_truth_dataset.json is in the same directory
ls ground_truth_dataset.json
```

### Semua metrics = 0.0

**Possible causes**:
1. ERD names di ground truth tidak match dengan database
2. min_similarity terlalu tinggi
3. Database kosong / tidak ada ERD

**Debug**:
```python
# Add debug print in test script
print("Recommended ERDs:", recommended_erd_names)
print("Expected ERDs:", relevant_erds)
```

## References

1. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.
2. Croft, W. B., Metzler, D., & Strohman, T. (2015). *Search Engines: Information Retrieval in Practice*. Pearson.
3. Baeza-Yates, R., & Ribeiro-Neto, B. (2011). *Modern Information Retrieval*. ACM Press.

## Contact & Support

Jika ada pertanyaan atau issues, silakan:
1. Check dokumentasi ini terlebih dahulu
2. Review code comments di `test_recommendation_metrics.py`
3. Contact development team

---

**Last Updated**: 2025-11-29
**Version**: 1.0
