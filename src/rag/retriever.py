import os
import sys
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import DB_PATH

class LocalRAGRetriever:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def retrieve_context(self, query: str, top_k: int = 2) -> list:
        """Kullanıcı sorgusuna en yakın doküman parçalarını SQLite'tan çeker."""
        if not os.path.exists(self.db_path):
            return ["Bilgi tabanı (veritabanı) henüz oluşturulmamış."]

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT chunk_text, embedding FROM knowledge_base")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return ["Veritabanında kayıtlı doküman bulunamadı."]

        chunk_texts = []
        embeddings = []
        for row in rows:
            chunk_texts.append(row[0])
            embeddings.append(np.frombuffer(row[1], dtype=np.float32))

        embeddings = np.array(embeddings)
        query_embedding = self.model.encode(query).astype(np.float32).reshape(1, -1)

        # Kosinüs benzerliği hesaplama
        similarities = cosine_similarity(query_embedding, embeddings)[0]
        
        # En yüksek skorlu top_k parçayı seç
        best_indices = np.argsort(similarities)[::-1][:top_k]
        
        retrieved_chunks = [chunk_texts[i] for i in best_indices]
        return retrieved_chunks

if __name__ == "__main__":
    retriever = LocalRAGRetriever()
    test_query = "Golf modelinin yağ bakımı kaç kilometrede bir yapılır?"
    print(f"[*] Soru: {test_query}")
    contexts = retriever.retrieve_context(test_query, top_k=2)
    print("\n--- [Bulunan İlgili Bağlamlar] ---")
    for idx, ctx in enumerate(contexts, 1):
        print(f"{idx}. {ctx}")