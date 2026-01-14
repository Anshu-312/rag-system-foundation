import faiss
import numpy as np
import os
from app.core.config import settings

def create_index(dim: int):
    index = faiss.IndexFlatL2(dim)
    return index
class VectorStore:
    def __init__(self, index):
        self.index = index
        self.texts: list[str] = []

    def add(self, vectors, texts):
         # Convert to numpy array and ensure float32
        vectors_np = np.array(vectors).astype('float32')

        if isinstance(self.index, faiss.IndexIVF):
            if not self.index.is_trained:
                self.index.train(vectors_np)

        # Use the converted numpy array
        self.index.add(vectors_np)
        self.texts.extend(texts)

    def search(self, query_vector, top_k: int):
        # Convert query to numpy array and reshape for FAISS (1, dim)
        query_np = np.array([query_vector]).astype('float32')
        
        # Actually perform the search
        scores, indices = self.index.search(query_np, top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1 or idx >= len(self.texts):
                continue
            results.append({
                "score": float(score), 
                "text": self.texts[idx]
            })
        
        return results
    
    def save(self):
        # Save the FAISS index to disk
        faiss.write_index(self.index, settings.faiss_index_path)
        # Also persist the list of texts so results can be retrieved survive restarts
        texts_path = settings.faiss_index_path + ".texts.json"
        try:
            with open(texts_path, 'w', encoding='utf-8') as f:
                import json
                json.dump(self.texts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving texts: {e}")

    @classmethod
    def load(cls, index_obj):
        if os.path.exists(settings.faiss_index_path):
            index = faiss.read_index(settings.faiss_index_path)
            vector_store = cls(index)
            texts_path = settings.faiss_index_path + ".texts.json"
            try:
                with open(texts_path, 'r', encoding='utf-8') as f:
                    import json
                    vector_store.texts = json.load(f)
            except Exception as e:
                print(f"Error loading texts: {e}")
            return vector_store
        return cls(index_obj)
    
