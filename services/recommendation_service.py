from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from models.database import db
from utils.text_processing import remove_stopwords, get_stop_words, advanced_normalize_text
from config import Config

class ERDRecommendationService:
    """ERD Recommendation System using TF-IDF"""
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words=list(get_stop_words()),
            lowercase=True,
            ngram_range=Config.TFIDF_NGRAM_RANGE,
            max_features=Config.TFIDF_MAX_FEATURES
        )
        self.erd_documents = []
        self.erd_data = []
        self.tfidf_matrix = None
        self.load_and_process_erds()
    
    def create_erd_document(self, erd):
        """
        Create text document from ERD data for TF-IDF with advanced normalization
        Applies: CamelCase splitting, special char removal, whitespace normalization, 
                 lowercase conversion, and Indonesian stemming
        """
        doc_parts = []
        
        # Add ERD name (normalized with advanced processing)
        doc_parts.append(advanced_normalize_text(erd['name']))
        
        # Add entity names and attributes (normalized with advanced processing)
        for entity in erd['entities']:
            doc_parts.append(advanced_normalize_text(entity['name']))
            # Normalize all attributes with advanced processing
            normalized_attrs = [advanced_normalize_text(attr) for attr in entity['attributes']]
            doc_parts.extend(normalized_attrs)
        
        # Add relationship information (normalized with advanced processing)
        for rel in erd['relationships']:
            entity1 = advanced_normalize_text(rel['entity1'])
            entity2 = advanced_normalize_text(rel['entity2'])
            rel_type = advanced_normalize_text(rel['type'])
            doc_parts.append(f"{entity1} {entity2} {rel_type}")
        
        return ' '.join(doc_parts)
    
    def load_and_process_erds(self):
        """Load ERD data from database and process for TF-IDF"""
        erds = db.get_all_erds()
        self.erd_data = erds
        self.erd_documents = [self.create_erd_document(erd) for erd in erds]
        
        if self.erd_documents:
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.erd_documents)
    
    def recommend_erds(self, query, top_k=None, min_similarity=None):
        """
        Recommend ERDs based on query using TF-IDF
        
        Args:
            query (str): User query
            top_k (int): Maximum number of recommendations
            min_similarity (float): Minimum similarity threshold
            
        Returns:
            list: List of recommended ERDs with similarity scores
        """
        if top_k is None:
            top_k = Config.DEFAULT_TOP_K
        if min_similarity is None:
            min_similarity = Config.DEFAULT_MIN_SIMILARITY
            
        if not self.erd_documents or self.tfidf_matrix is None:
            return []
        
        # Advanced normalize and preprocess query
        # Applies: CamelCase splitting, special char removal, whitespace normalization,
        #          lowercase conversion, Indonesian stemming, and stopwords removal
        normalized_query = advanced_normalize_text(query)
        processed_query = remove_stopwords(normalized_query)
        
        # Transform query using same TF-IDF vectorizer
        query_vector = self.tfidf_vectorizer.transform([processed_query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Create results with similarity scores
        results = []
        for i, similarity in enumerate(similarities):
            if similarity >= min_similarity:
                results.append({
                    'erd': self.erd_data[i],
                    'similarity': float(similarity),
                    'rank': i
                })
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return results[:top_k]
    
    def reload_system(self):
        """Reload recommendation system (useful when data changes)"""
        self.load_and_process_erds()

# Global recommendation service instance
recommendation_service = ERDRecommendationService()