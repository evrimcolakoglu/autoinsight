# 🚗 AutoInsight: RAG Destekli Akıllı Araç Değerleme ve Tavsiye Sistemi

AutoInsight, ikinci el otomotiv pazarı için geliştirilmiş; dinamik fiyat tahmini, bütçe ve ihtiyaç odaklı araç eşleştirme ile çevrimdışı (offline) RAG mimarisini tek çatı altında toplayan uçtan uca bir makine öğrenmesi asistanıdır.

---

## 📌 Temel Özellikler

* **Dinamik Fiyatlandırma (ML Engine):** Araçların teknik özellikleri, hasar geçmişi ve kilometre verilerini analiz ederek piyasa değerini tahmin eden regresyon boru hattı (Random Forest + Target Encoding).
* **Akıllı Araç Tavsiyesi (Recommender):** Kullanıcının bütçe, yakıt ve vites tercihlerine göre filtreleme yapan; fiyat/performans uyum puanı ve Kosinüs Benzerliği (Cosine Similarity) ile en uygun alternatifleri sıralayan hibrit algoritma.
* **Çevrimdışı RAG ve Teknik Asistan:** Harici API veya internet bağımlılığı olmadan araç bakım bültenleri ve kullanım kılavuzlarından anlamsal bilgi çeken yerel vektör arama motoru (SQLite + Sentence Transformers).

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
```

---

## 🚀 Hızlı Başlangıç (Docker ile)

Projeyi bilgisayarınızda herhangi bir Python veya kütüphane bağımlılığı kurmadan doğrudan Docker üzerinden çalıştırabilirsiniz:

```bash
# 1. Depoyu klonlayın
git clone [https://github.com/evrimcolakoglu/autoinsight.git](https://github.com/evrimcolakoglu/autoinsight.git)
cd autoinsight

# 2. Docker imajını derleyin
docker build -t autoinsight .

# 3. Konteyneri başlatın
docker run -p 8501:8501 autoinsight
```

Tarayıcınızdan **`http://localhost:8501`** adresine gidin.

---

## 💻 Manuel Kurulum (Lokal Geliştirme)

Sanal ortam (venv) ile yerel geliştirme yapmak için:

```bash
# Sanal ortam oluşturma ve aktif etme
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Bağımlılıkları yükleme
pip install -r requirements.txt

# Modeli eğitme ve RAG veritabanını oluşturma
python src/pricing/pipeline.py
python src/rag/ingest.py

# Arayüzü başlatma
streamlit run app.py
```

---

## 📊 Model Başarım Metrikleri

152 araçlık heterojen veri seti üzerinde yapılan test sonuçları:

| Metrik | Skor | Açıklama |
| :--- | :--- | :--- |
| **R² (Belirleme Katsayısı)** | **0.7868** | Fiyat varyansını açıklama başarımı (~%79) |
| **MAE (Ortalama Mutlak Hata)** | **129,763 TL** | Gerçek fiyattan ortalama sapma tutarı |
| **RMSE (Kareli Ortalama Hata)**| **170,673 TL** | Büyük sapmaları cezalandıran hata metriği |
| **MAPE (Yüzdesel Hata)** | **%20.40** | Ortalama yüzdesel sapma oranı |

---

## 📁 Proje Dizin Yapısı

```text
autoinsight/
├── data/
│   ├── raw/                  # Ham araç CSV verileri ve kılavuz dokümanları (.txt/.pdf)
│   └── processed/            # SQLite yerel vektör veri tabanı (knowledge_base.db)
├── docs/                     # RAG için teknik bülten ve bakım kılavuzları
├── models/                   # Eğitilen scikit-learn pipeline dosyaları (.joblib)
├── src/
│   ├── config.py             # Dinamik şema ve merkezi dizin yapılandırması
│   ├── pricing/              # Fiyat tahmin modeli ve eğitim hattı
│   ├── rag/                  # Vektörleme ve anlamsal arama modülü
│   └── recommender/          # Filtreleme ve kosinüs benzerlik motoru
├── app.py                    # Streamlit dashboard arayüzü
├── Dockerfile                # Konteynerizasyon konfigürasyonu
└── requirements.txt          # Proje bağımlılıkları
```
