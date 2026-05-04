import json
import os
from typing import Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SQLResponseCache:
    def __init__(self, cache_file: str = "unamed_user_cache.json"):
        self.cache_file = "history_chat_users/" + cache_file
        self.cache: Dict[str, Dict[str, Any]] = self._load_cache()
        self.vectorizer = TfidfVectorizer()
        self._initialize_vectorizer()

    def _load_cache(self) -> Dict[str, Dict[str, Any]]:
        """Load cache from JSON file or create new if doesn't exist"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Save cache to JSON file"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)

    def _initialize_vectorizer(self):
        """Initialize the vectorizer with existing questions"""
        if self.cache:
            questions = list(self.cache.keys())
            self.vectorizer.fit(questions)

    def _get_similar_question(self, question: str, threshold: float = 0.8) -> Optional[str]:
        """Find similar question in cache using cosine similarity"""
        if not self.cache:
            return None

        questions = list(self.cache.keys())
        if not questions:
            return None

        # Transform the input question
        question_vec = self.vectorizer.transform([question])
        
        # Transform all cached questions
        cached_vecs = self.vectorizer.transform(questions)
        
        # Calculate similarities
        similarities = cosine_similarity(question_vec, cached_vecs)[0]
        
        # Find the most similar question
        max_similarity_idx = np.argmax(similarities)
        max_similarity = similarities[max_similarity_idx]
        
        if max_similarity >= threshold:
            return questions[max_similarity_idx]
        return None

    def get(self, question: str) -> Optional[Dict[str, Any]]:
        """Get cached response for a question or similar question"""
        # First check exact match
        if question in self.cache:
            return self.cache[question]
        
        # Then check for similar questions
        similar_question = self._get_similar_question(question)
        if similar_question:
            return self.cache[similar_question]
        
        return None

    def set(self, question: str, response: Dict[str, Any]):
        """Cache a new response"""
        self.cache[question] = response
        self._save_cache()
        
        # Update vectorizer with new question
        self._initialize_vectorizer()

    def clear(self):
        """Clear the cache"""
        self.cache = {}
        self._save_cache()
        self._initialize_vectorizer() 