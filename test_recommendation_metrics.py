"""
Script untuk menguji sistem rekomendasi ERD menggunakan metrik:
- Precision@K
- Recall@K
- F1-Score
- Mean Average Precision (MAP)
- Mean Reciprocal Rank (MRR)

Author: ERD Recommendation Testing Team
Date: 2025-11-29
"""

import json
import sys
import os
from datetime import datetime
from collections import defaultdict

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.recommendation_service import recommendation_service


class RecommendationMetrics:
    """Class untuk menghitung berbagai metrik evaluasi sistem rekomendasi"""
    
    @staticmethod
    def precision_at_k(recommended_erds, relevant_erds, k):
        """
        Hitung Precision@K
        
        Precision@K = (Jumlah ERD relevan dalam top-K rekomendasi) / K
        
        Args:
            recommended_erds: List ERD yang direkomendasikan (urut berdasarkan similarity)
            relevant_erds: List ERD yang relevan (ground truth)
            k: Jumlah top-K yang dipertimbangkan
            
        Returns:
            float: Nilai Precision@K (0.0 - 1.0)
        """
        if k == 0 or len(recommended_erds) == 0:
            return 0.0
        
        # Ambil top-K rekomendasi
        top_k = recommended_erds[:k]
        
        # Hitung berapa banyak yang relevan
        relevant_count = sum(1 for erd in top_k if erd in relevant_erds)
        
        return relevant_count / k
    
    @staticmethod
    def recall_at_k(recommended_erds, relevant_erds, k):
        """
        Hitung Recall@K
        
        Recall@K = (Jumlah ERD relevan dalam top-K rekomendasi) / (Total ERD relevan)
        
        Args:
            recommended_erds: List ERD yang direkomendasikan (urut berdasarkan similarity)
            relevant_erds: List ERD yang relevan (ground truth)
            k: Jumlah top-K yang dipertimbangkan
            
        Returns:
            float: Nilai Recall@K (0.0 - 1.0)
        """
        if len(relevant_erds) == 0:
            return 0.0
        
        # Ambil top-K rekomendasi
        top_k = recommended_erds[:k]
        
        # Hitung berapa banyak yang relevan
        relevant_count = sum(1 for erd in top_k if erd in relevant_erds)
        
        return relevant_count / len(relevant_erds)
    
    @staticmethod
    def f1_score(precision, recall):
        """
        Hitung F1-Score
        
        F1 = 2 * (Precision * Recall) / (Precision + Recall)
        
        Args:
            precision: Nilai precision
            recall: Nilai recall
            
        Returns:
            float: Nilai F1-Score (0.0 - 1.0)
        """
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
    
    @staticmethod
    def average_precision(recommended_erds, relevant_erds):
        """
        Hitung Average Precision (AP) untuk satu query
        
        AP = (1/|relevant|) * Σ(Precision@k * rel(k))
        dimana rel(k) = 1 jika item ke-k relevan, 0 jika tidak
        
        Args:
            recommended_erds: List ERD yang direkomendasikan
            relevant_erds: List ERD yang relevan (ground truth)
            
        Returns:
            float: Nilai Average Precision (0.0 - 1.0)
        """
        if len(relevant_erds) == 0:
            return 0.0
        
        precision_sum = 0.0
        relevant_count = 0
        
        for i, erd in enumerate(recommended_erds, 1):
            if erd in relevant_erds:
                relevant_count += 1
                precision_at_i = relevant_count / i
                precision_sum += precision_at_i
        
        return precision_sum / len(relevant_erds)
    
    @staticmethod
    def reciprocal_rank(recommended_erds, relevant_erds):
        """
        Hitung Reciprocal Rank (RR) untuk satu query
        
        RR = 1 / rank_of_first_relevant_item
        
        Args:
            recommended_erds: List ERD yang direkomendasikan
            relevant_erds: List ERD yang relevan (ground truth)
            
        Returns:
            float: Nilai Reciprocal Rank (0.0 - 1.0)
        """
        for i, erd in enumerate(recommended_erds, 1):
            if erd in relevant_erds:
                return 1.0 / i
        
        return 0.0


class RecommendationTester:
    """Class untuk menjalankan pengujian sistem rekomendasi"""
    
    def __init__(self, ground_truth_file):
        """
        Inisialisasi tester
        
        Args:
            ground_truth_file: Path ke file ground truth JSON
        """
        self.ground_truth_file = ground_truth_file
        self.ground_truth_data = self._load_ground_truth()
        self.metrics = RecommendationMetrics()
        self.results = []
        
    def _load_ground_truth(self):
        """Load ground truth data dari JSON file"""
        with open(self.ground_truth_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run_test(self, k_values=[5, 10], min_similarity=0.0):
        """
        Jalankan pengujian untuk semua queries
        
        Args:
            k_values: List nilai K untuk Precision@K dan Recall@K
            min_similarity: Minimum similarity threshold untuk rekomendasi
            
        Returns:
            dict: Hasil pengujian lengkap
        """
        print(f"\n{'='*80}")
        print(f"PENGUJIAN SISTEM REKOMENDASI ERD")
        print(f"{'='*80}")
        print(f"Total test queries: {len(self.ground_truth_data)}")
        print(f"K values: {k_values}")
        print(f"Min similarity: {min_similarity}")
        print(f"{'='*80}\n")
        
        all_metrics = defaultdict(list)
        query_results = []
        
        for i, test_case in enumerate(self.ground_truth_data, 1):
            query_id = test_case['query_id']
            query = test_case['query']
            relevant_erds = test_case['relevant_erds']
            description = test_case.get('description', '')
            
            print(f"[{i}/{len(self.ground_truth_data)}] Testing Query {query_id}: {query[:50]}...")
            
            # Dapatkan rekomendasi dari sistem
            recommendations = recommendation_service.recommend_erds(
                query=query,
                top_k=max(k_values) if k_values else 10,
                min_similarity=min_similarity
            )
            
            # Extract ERD names dari hasil rekomendasi
            recommended_erd_names = [rec['erd']['name'] for rec in recommendations]
            
            # Hitung metrik untuk setiap nilai K
            query_result = {
                'query_id': query_id,
                'query': query,
                'description': description,
                'relevant_erds': relevant_erds,
                'recommended_erds': recommended_erd_names,
                'total_recommendations': len(recommended_erd_names),
                'metrics': {}
            }
            
            # Hitung Precision@K, Recall@K, dan F1@K untuk setiap K
            for k in k_values:
                precision = self.metrics.precision_at_k(recommended_erd_names, relevant_erds, k)
                recall = self.metrics.recall_at_k(recommended_erd_names, relevant_erds, k)
                f1 = self.metrics.f1_score(precision, recall)
                
                query_result['metrics'][f'precision@{k}'] = precision
                query_result['metrics'][f'recall@{k}'] = recall
                query_result['metrics'][f'f1@{k}'] = f1
                
                all_metrics[f'precision@{k}'].append(precision)
                all_metrics[f'recall@{k}'].append(recall)
                all_metrics[f'f1@{k}'].append(f1)
            
            # Hitung Average Precision dan Reciprocal Rank
            ap = self.metrics.average_precision(recommended_erd_names, relevant_erds)
            rr = self.metrics.reciprocal_rank(recommended_erd_names, relevant_erds)
            
            query_result['metrics']['average_precision'] = ap
            query_result['metrics']['reciprocal_rank'] = rr
            
            all_metrics['average_precision'].append(ap)
            all_metrics['reciprocal_rank'].append(rr)
            
            query_results.append(query_result)
            
            # Print hasil untuk query ini
            print(f"  - Recommendations: {len(recommended_erd_names)}")
            for k in k_values:
                print(f"  - P@{k}: {query_result['metrics'][f'precision@{k}']:.3f} | "
                      f"R@{k}: {query_result['metrics'][f'recall@{k}']:.3f} | "
                      f"F1@{k}: {query_result['metrics'][f'f1@{k}']:.3f}")
            print(f"  - AP: {ap:.3f} | RR: {rr:.3f}\n")
        
        # Hitung rata-rata metrik
        avg_metrics = {}
        for metric_name, values in all_metrics.items():
            avg_metrics[metric_name] = sum(values) / len(values) if values else 0.0
        
        # Tambahkan MAP dan MRR
        avg_metrics['MAP'] = avg_metrics.get('average_precision', 0.0)
        avg_metrics['MRR'] = avg_metrics.get('reciprocal_rank', 0.0)
        
        # Compile hasil akhir
        final_results = {
            'timestamp': datetime.now().isoformat(),
            'total_queries': len(self.ground_truth_data),
            'k_values': k_values,
            'min_similarity': min_similarity,
            'average_metrics': avg_metrics,
            'query_results': query_results
        }
        
        self.results = final_results
        return final_results
    
    def print_summary(self):
        """Print ringkasan hasil pengujian"""
        if not self.results:
            print("Belum ada hasil pengujian. Jalankan run_test() terlebih dahulu.")
            return
        
        avg_metrics = self.results['average_metrics']
        
        print(f"\n{'='*80}")
        print(f"RINGKASAN HASIL PENGUJIAN")
        print(f"{'='*80}")
        print(f"Total Queries: {self.results['total_queries']}")
        print(f"K Values: {self.results['k_values']}")
        print(f"\nRata-rata Metrik:")
        print(f"{'-'*80}")
        
        # Print metrik untuk setiap K
        k_values = self.results['k_values']
        for k in k_values:
            print(f"\nTop-{k} Recommendations:")
            print(f"  Precision@{k}: {avg_metrics.get(f'precision@{k}', 0):.4f}")
            print(f"  Recall@{k}:    {avg_metrics.get(f'recall@{k}', 0):.4f}")
            print(f"  F1-Score@{k}:  {avg_metrics.get(f'f1@{k}', 0):.4f}")
        
        # Print MAP dan MRR
        print(f"\nOverall Metrics:")
        print(f"  MAP (Mean Average Precision): {avg_metrics.get('MAP', 0):.4f}")
        print(f"  MRR (Mean Reciprocal Rank):   {avg_metrics.get('MRR', 0):.4f}")
        print(f"{'='*80}\n")
    
    def save_results(self, output_file=None):
        """
        Simpan hasil pengujian ke file JSON
        
        Args:
            output_file: Path output file (default: test_results_TIMESTAMP.json)
        """
        if not self.results:
            print("Belum ada hasil pengujian. Jalankan run_test() terlebih dahulu.")
            return
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_results_metrics_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"Hasil pengujian disimpan ke: {output_file}")
    
    def generate_report(self, output_file=None):
        """
        Generate laporan pengujian dalam format Markdown
        
        Args:
            output_file: Path output file (default: test_report_TIMESTAMP.md)
        """
        if not self.results:
            print("Belum ada hasil pengujian. Jalankan run_test() terlebih dahulu.")
            return
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_report_metrics_{timestamp}.md"
        
        avg_metrics = self.results['average_metrics']
        k_values = self.results['k_values']
        
        # Generate markdown content
        md_content = f"""# Laporan Pengujian Sistem Rekomendasi ERD

## Informasi Pengujian

- **Tanggal**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Total Queries**: {self.results['total_queries']}
- **Nilai K**: {k_values}
- **Minimum Similarity**: {self.results['min_similarity']}

## Ringkasan Hasil

### Metrik Rata-rata untuk Setiap K

"""
        
        # Table untuk metrik per K
        md_content += "| K | Precision@K | Recall@K | F1-Score@K |\n"
        md_content += "|---|-------------|----------|------------|\n"
        for k in k_values:
            p = avg_metrics.get(f'precision@{k}', 0)
            r = avg_metrics.get(f'recall@{k}', 0)
            f1 = avg_metrics.get(f'f1@{k}', 0)
            md_content += f"| {k} | {p:.4f} | {r:.4f} | {f1:.4f} |\n"
        
        # Overall metrics
        md_content += f"""
### Metrik Overall

- **MAP (Mean Average Precision)**: {avg_metrics.get('MAP', 0):.4f}
- **MRR (Mean Reciprocal Rank)**: {avg_metrics.get('MRR', 0):.4f}

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

"""
        
        # Tambahkan detail per query
        for query_result in self.results['query_results']:
            md_content += f"### Query {query_result['query_id']}: {query_result['query']}\n\n"
            md_content += f"**Deskripsi**: {query_result['description']}\n\n"
            md_content += f"**ERD Relevan**: {', '.join(query_result['relevant_erds'])}\n\n"
            md_content += f"**Jumlah Rekomendasi**: {query_result['total_recommendations']}\n\n"
            
            # Metrik untuk query ini
            md_content += "**Metrik**:\n"
            for k in k_values:
                p = query_result['metrics'][f'precision@{k}']
                r = query_result['metrics'][f'recall@{k}']
                f1 = query_result['metrics'][f'f1@{k}']
                md_content += f"- Precision@{k}: {p:.3f}, Recall@{k}: {r:.3f}, F1@{k}: {f1:.3f}\n"
            
            ap = query_result['metrics']['average_precision']
            rr = query_result['metrics']['reciprocal_rank']
            md_content += f"- AP: {ap:.3f}, RR: {rr:.3f}\n\n"
            
            # Top-5 rekomendasi
            md_content += "**Top-5 Rekomendasi**:\n"
            for i, erd_name in enumerate(query_result['recommended_erds'][:5], 1):
                is_relevant = "✓" if erd_name in query_result['relevant_erds'] else "✗"
                md_content += f"{i}. {erd_name} {is_relevant}\n"
            md_content += "\n---\n\n"
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Laporan pengujian disimpan ke: {output_file}")


def main():
    """Main function untuk menjalankan pengujian"""
    # Path ke ground truth file
    ground_truth_file = "ground_truth_dataset.json"
    
    if not os.path.exists(ground_truth_file):
        print(f"Error: File {ground_truth_file} tidak ditemukan!")
        print("Pastikan file ground_truth_dataset.json ada di direktori yang sama.")
        return
    
    # Inisialisasi tester
    print("Menginisialisasi recommendation tester...")
    tester = RecommendationTester(ground_truth_file)
    
    # Jalankan pengujian dengan K=[5, 10]
    print("Menjalankan pengujian...")
    results = tester.run_test(k_values=[5, 10], min_similarity=0.0)
    
    # Print ringkasan
    tester.print_summary()
    
    # Simpan hasil
    tester.save_results()
    
    # Generate laporan
    tester.generate_report()
    
    print("\nPengujian selesai!")


if __name__ == "__main__":
    main()
