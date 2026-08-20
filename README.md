# 🚗 AutoInsight: RAG Destekli Akıllı Araç Değerleme ve Tavsiye Sistemi

AutoInsight, ikinci el otomotiv piyasası için geliştirilmiş; dinamik fiyat tahmini, bütçe ve ihtiyaç odaklı araç eşleştirme ile çevrimdışı (offline) RAG mimarisini tek çatı altında toplayan uçtan uca bir yapay zeka asistanıdır.

---

## 📌 Temel Özellikler

* **Dinamik Fiyatlandırma (ML Engine):** Araçların teknik parametreleri, geçmiş hasar ve kilometre verilerini analiz ederek piyasa değerini yüksek doğrulukla tahmin eden regresyon boru hattı (Random Forest + Target Encoding).
* **Akıllı Araç Tavsiyesi (Recommender):** Kullanıcının bütçe, yakıt ve vites tercihlerine göre filtreleme yapan; fiyat/performans uyum skoru ve Kosinüs Benzerliği (Cosine Similarity) ile en mantıklı alternatifleri sıralayan hibrit algoritma.
* **Çevrimdışı RAG ve Teknik Asistan:** Harici yapay zeka API'larına ve internete ihtiyaç duymadan, araç kılavuzları ve periyodik bakım raporlarından bilgi çeken yerel vektör arama motoru (SQLite + Sentence Transformers).

---

## 🏗️ Sistem Mimarisi

```text
[ Streamlit Web Kullanıcı Arayüzü ]
        │
        ├──► [ Modül 1: Fiyatlandırma Pipeline ] ──► (Scikit-Learn / Random Forest Regressor)
        │
        ├──► [ Modül 2: Akıllı Öneri Motoru ]   ──► (Kural Tabanlı Filtreleme + Kosinüs Benzerliği)
        │
        └──► [ Modül 3: Yerel RAG Asistanı ]     ──► (SQLite Vektör Tabanı + all-MiniLM-L6-v2)
