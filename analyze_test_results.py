"""
Script untuk analisis lanjutan hasil pengujian sistem rekomendasi:
- Confusion Matrix
- Detailed Error Analysis
- Per-Domain Performance Analysis

Author: ERD Recommendation Testing Team
Date: 2025-11-29
"""

import json
import sys
from collections import defaultdict


class ResultAnalyzer:
    """Class untuk analisis hasil pengujian"""
    
    def __init__(self, results_file):
        """
        Inisialisasi analyzer
        
        Args:
            results_file: Path ke file hasil pengujian JSON
        """
        self.results_file = results_file
        self.results = self._load_results()
        
    def _load_results(self):
        """Load hasil pengujian dari JSON file"""
        with open(self.results_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def calculate_confusion_matrix(self, k=5):
        """
        Hitung confusion matrix untuk top-K rekomendasi
        
        Args:
            k: Nilai K untuk top-K rekomendasi
            
        Returns:
            dict: Confusion matrix (TP, FP, TN, FN)
        """
        tp = 0  # True Positive: Recommended & Relevant
        fp = 0  # False Positive: Recommended & Not Relevant
        fn = 0  # False Negative: Not Recommended & Relevant
        tn = 0  # True Negative: Not Recommended & Not Relevant
        
        # Get all ERD names from first query to determine universe
        # In practice, you'd get this from database
        all_erds_set = set()
        for query_result in self.results['query_results']:
            all_erds_set.update(query_result['relevant_erds'])
            all_erds_set.update(query_result['recommended_erds'])
        
        for query_result in self.results['query_results']:
            relevant_set = set(query_result['relevant_erds'])
            recommended_set = set(query_result['recommended_erds'][:k])
            
            # True Positive: In both recommended and relevant
            tp += len(recommended_set & relevant_set)
            
            # False Positive: In recommended but not in relevant
            fp += len(recommended_set - relevant_set)
            
            # False Negative: In relevant but not in recommended
            fn += len(relevant_set - recommended_set)
            
            # True Negative: Not in recommended and not in relevant
            # (semua ERD lain yang tidak direkomendasikan dan tidak relevan)
            not_recommended = all_erds_set - recommended_set
            not_relevant = all_erds_set - relevant_set
            tn += len(not_recommended & not_relevant)
        
        return {
            'TP': tp,
            'FP': fp,
            'TN': tn,
            'FN': fn
        }
    
    def print_confusion_matrix(self, k=5):
        """Print confusion matrix dengan format yang readable"""
        cm = self.calculate_confusion_matrix(k)
        
        print(f"\n{'='*80}")
        print(f"CONFUSION MATRIX (Top-{k} Recommendations)")
        print(f"{'='*80}")
        print(f"\n                     Predicted Relevant  |  Predicted Not Relevant")
        print(f"                     -------------------|------------------------")
        print(f"Actual Relevant      TP = {cm['TP']:4d}          |  FN = {cm['FN']:4d}")
        print(f"Actual Not Relevant  FP = {cm['FP']:4d}          |  TN = {cm['TN']:4d}")
        print(f"\n{'='*80}")
        
        # Hitung additional metrics
        total = cm['TP'] + cm['FP'] + cm['TN'] + cm['FN']
        accuracy = (cm['TP'] + cm['TN']) / total if total > 0 else 0
        
        # Precision and Recall dari confusion matrix
        precision = cm['TP'] / (cm['TP'] + cm['FP']) if (cm['TP'] + cm['FP']) > 0 else 0
        recall = cm['TP'] / (cm['TP'] + cm['FN']) if (cm['TP'] + cm['FN']) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"\nDerived Metrics:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"{'='*80}\n")
    
    def analyze_failure_cases(self, k=5):
        """
        Analisis kasus-kasus dimana sistem gagal (false negatives dan false positives)
        
        Args:
            k: Nilai K untuk top-K rekomendasi
        """
        print(f"\n{'='*80}")
        print(f"FAILURE CASES ANALYSIS (Top-{k})")
        print(f"{'='*80}\n")
        
        fn_cases = []  # False Negatives: ERD relevan yang tidak direkomendasikan
        fp_cases = []  # False Positives: ERD tidak relevan yang direkomendasikan
        
        for query_result in self.results['query_results']:
            query_id = query_result['query_id']
            query = query_result['query']
            relevant_set = set(query_result['relevant_erds'])
            recommended_set = set(query_result['recommended_erds'][:k])
            
            # False Negatives
            missed = relevant_set - recommended_set
            if missed:
                fn_cases.append({
                    'query_id': query_id,
                    'query': query,
                    'missed_erds': list(missed)
                })
            
            # False Positives
            wrong = recommended_set - relevant_set
            if wrong:
                fp_cases.append({
                    'query_id': query_id,
                    'query': query,
                    'wrong_erds': list(wrong)
                })
        
        # Print False Negatives
        print(f"FALSE NEGATIVES: {len(fn_cases)} queries")
        print(f"{'-'*80}")
        if fn_cases:
            for i, case in enumerate(fn_cases[:10], 1):  # Show top 10
                print(f"\n{i}. Query {case['query_id']}: {case['query']}")
                print(f"   Missed ERDs: {', '.join(case['missed_erds'])}")
        else:
            print("No false negatives - Perfect recall!")
        
        # Print False Positives
        print(f"\n\nFALSE POSITIVES: {len(fp_cases)} queries")
        print(f"{'-'*80}")
        if fp_cases:
            for i, case in enumerate(fp_cases[:10], 1):  # Show top 10
                print(f"\n{i}. Query {case['query_id']}: {case['query']}")
                print(f"   Wrong ERDs: {', '.join(case['wrong_erds'])}")
        else:
            print("No false positives - Perfect precision!")
        
        print(f"\n{'='*80}\n")
    
    def analyze_by_query_difficulty(self):
        """Analisis performa berdasarkan kesulitan query (berdasarkan jumlah ERD relevan)"""
        print(f"\n{'='*80}")
        print(f"PERFORMANCE BY QUERY DIFFICULTY")
        print(f"{'='*80}\n")
        
        # Kelompokkan berdasarkan jumlah ERD relevan
        difficulty_groups = defaultdict(list)
        
        for query_result in self.results['query_results']:
            num_relevant = len(query_result['relevant_erds'])
            
            # Ambil F1@5 sebagai metrik utama
            f1_score = query_result['metrics'].get('f1@5', 0)
            
            difficulty_groups[num_relevant].append({
                'query_id': query_result['query_id'],
                'query': query_result['query'],
                'f1@5': f1_score,
                'precision@5': query_result['metrics'].get('precision@5', 0),
                'recall@5': query_result['metrics'].get('recall@5', 0)
            })
        
        # Print analysis
        for num_relevant in sorted(difficulty_groups.keys()):
            queries = difficulty_groups[num_relevant]
            avg_f1 = sum(q['f1@5'] for q in queries) / len(queries)
            avg_p = sum(q['precision@5'] for q in queries) / len(queries)
            avg_r = sum(q['recall@5'] for q in queries) / len(queries)
            
            print(f"Queries with {num_relevant} relevant ERD(s): {len(queries)} queries")
            print(f"  Average P@5: {avg_p:.4f}")
            print(f"  Average R@5: {avg_r:.4f}")
            print(f"  Average F1@5: {avg_f1:.4f}")
            
            # Show worst performing query in this group
            worst = min(queries, key=lambda x: x['f1@5'])
            print(f"  Worst case: Query {worst['query_id']} (F1={worst['f1@5']:.3f}): {worst['query'][:60]}...")
            print()
        
        print(f"{'='*80}\n")
    
    def analyze_best_and_worst(self, k=5, top_n=5):
        """
        Analisis queries dengan performa terbaik dan terburuk
        
        Args:
            k: Nilai K untuk metrik
            top_n: Jumlah queries yang ditampilkan
        """
        print(f"\n{'='*80}")
        print(f"BEST AND WORST PERFORMING QUERIES (Top-{k})")
        print(f"{'='*80}\n")
        
        # Sortir berdasarkan F1@k
        queries = []
        for query_result in self.results['query_results']:
            f1_key = f'f1@{k}'
            queries.append({
                'query_id': query_result['query_id'],
                'query': query_result['query'],
                'description': query_result['description'],
                'f1': query_result['metrics'].get(f1_key, 0),
                'precision': query_result['metrics'].get(f'precision@{k}', 0),
                'recall': query_result['metrics'].get(f'recall@{k}', 0),
                'relevant_erds': query_result['relevant_erds'],
                'recommended_erds': query_result['recommended_erds'][:k]
            })
        
        # Sort by F1 score
        queries.sort(key=lambda x: x['f1'], reverse=True)
        
        # Best performing
        print(f"TOP {top_n} BEST PERFORMING QUERIES:")
        print(f"{'-'*80}")
        for i, q in enumerate(queries[:top_n], 1):
            print(f"\n{i}. Query {q['query_id']}: {q['query']}")
            print(f"   Description: {q['description']}")
            print(f"   P@{k}={q['precision']:.3f}, R@{k}={q['recall']:.3f}, F1@{k}={q['f1']:.3f}")
            print(f"   Relevant: {', '.join(q['relevant_erds'])}")
            print(f"   Recommended: {', '.join(q['recommended_erds'])}")
        
        # Worst performing
        print(f"\n\nTOP {top_n} WORST PERFORMING QUERIES:")
        print(f"{'-'*80}")
        for i, q in enumerate(queries[-top_n:], 1):
            print(f"\n{i}. Query {q['query_id']}: {q['query']}")
            print(f"   Description: {q['description']}")
            print(f"   P@{k}={q['precision']:.3f}, R@{k}={q['recall']:.3f}, F1@{k}={q['f1']:.3f}")
            print(f"   Relevant: {', '.join(q['relevant_erds'])}")
            print(f"   Recommended: {', '.join(q['recommended_erds']) if q['recommended_erds'] else 'NONE'}")
        
        print(f"\n{'='*80}\n")
    
    def generate_detailed_report(self, output_file=None):
        """Generate detailed analysis report"""
        if output_file is None:
            output_file = self.results_file.replace('.json', '_analysis.txt')
        
        # Redirect print to file
        original_stdout = sys.stdout
        with open(output_file, 'w', encoding='utf-8') as f:
            sys.stdout = f
            
            # Print all analyses
            self.print_confusion_matrix(k=5)
            self.analyze_failure_cases(k=5)
            self.analyze_by_query_difficulty()
            self.analyze_best_and_worst(k=5, top_n=5)
            
            # Print summary statistics
            print(f"{'='*80}")
            print(f"SUMMARY STATISTICS")
            print(f"{'='*80}\n")
            print(f"Total Queries: {self.results['total_queries']}")
            print(f"Timestamp: {self.results['timestamp']}")
            print(f"K Values: {self.results['k_values']}")
            
            avg_metrics = self.results['average_metrics']
            print(f"\nAverage Metrics:")
            for metric, value in sorted(avg_metrics.items()):
                print(f"  {metric}: {value:.4f}")
            
            print(f"\n{'='*80}")
        
        sys.stdout = original_stdout
        print(f"Detailed analysis report saved to: {output_file}")


def main():
    """Main function"""
    import glob
    
    # Find the latest test results file
    result_files = glob.glob("test_results_metrics_*.json")
    
    if not result_files:
        print("Error: No test results file found!")
        print("Please run test_recommendation_metrics.py first.")
        return
    
    # Use the latest file
    latest_file = max(result_files)
    print(f"Analyzing: {latest_file}\n")
    
    # Initialize analyzer
    analyzer = ResultAnalyzer(latest_file)
    
    # Run all analyses
    analyzer.print_confusion_matrix(k=5)
    analyzer.analyze_failure_cases(k=5)
    analyzer.analyze_by_query_difficulty()
    analyzer.analyze_best_and_worst(k=5, top_n=5)
    
    # Generate detailed report
    analyzer.generate_detailed_report()
    
    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
