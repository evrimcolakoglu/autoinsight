import os
import sys
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

from src.config import DB_PATH

def create_vector_database(docs_dir="docs", db_path=DB_PATH):
    """Metin dokümanlarını okur, parçalar, vektörleştirir ve SQLite'a kaydeder."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Yerel hafif embedding modeli (İnternet gerektirmez, ilk indirmeden sonra tamamen offline çalışır)
    print("[*] Yerel embedding modeli yükleniyor...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabloyu oluştur
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chunk_text TEXT,
            embedding BLOB
        )
    """)
    cursor.execute("DELETE FROM knowledge_base") # Eski verileri temizle

    chunk_count = 0
    if os.path.exists(docs_dir):
        for filename in os.listdir(docs_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(docs_dir, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Paragraflara veya cümle bloklarına bölme (Chunking)
                paragraphs = [p.strip() for p in content.split("\n") if p.strip()]
                for para in paragraphs:
                    embedding = model.encode(para).astype(np.float32).tobytes()
                    cursor.execute(
                        "INSERT INTO knowledge_base (chunk_text, embedding) VALUES (?, ?)",
                        (para, embedding)
                    )
                    chunk_count += 1

    conn.commit()
    conn.close()
    print(f"[✓] RAG Veritabanı oluşturuldu. Toplam {chunk_count} metin parçası (chunk) indexlendi.")

if __name__ == "__main__":
    create_vector_database()