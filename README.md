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

## 👥 Geliştirici Kurulum Rehberi

> Bu bölüm, repoya erişimi olan geliştiriciler için hazırlanmıştır.

### Ön Gereksinimler

Başlamadan önce aşağıdakilerin bilgisayarınızda kurulu olduğundan emin olun:

| Araç | Versiyon | İndirme |
|------|----------|---------|
| Python | 3.10 veya üzeri | [python.org](https://www.python.org/downloads/) |
| Git | Herhangi | [git-scm.com](https://git-scm.com/) |

### 1. Repoyu Klonlayın

```bash
git clone https://github.com/evrimcolakoglu/autoinsight.git
cd autoinsight
```

### 2. Sanal Ortam Oluşturun ve Aktif Edin

```bash
# Sanal ortam oluştur
python -m venv venv

# Aktif et — Windows:
.\venv\Scripts\activate

# Aktif et — macOS/Linux:
source venv/bin/activate
```

> Aktivasyon sonrası terminal satırınızın başında (venv) görünmesi gerekir.

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

> ⚠️ sentence-transformers paketi ilk yüklemede ~500 MB boyutunda model indirebilir. Bu normaldir.

### 4. Eğitilmiş Modeli İndirin (Google Drive)

Fiyatlandırma modeli (pricing_pipeline.joblib) boyutu nedeniyle (~350 MB) GitHub'da bulunmamaktadır.

**a)** Aşağıdaki bağlantıdan model dosyasını indirin:

> 📦 **[pricing_pipeline.joblib — Google Drive'dan İndir](https://drive.google.com/drive/folders/1ifLAcUbWEbOvHWeJnqaV68JAtO4aQPdb?usp=sharing)**
>
> *(Bağlantıyı proje sahibinden talep edin)*

**b)** İndirilen dosyayı projenin models/ klasörüne taşıyın:

```
autoinsight/
└── models/
    └── pricing_pipeline.joblib   ✅ buraya koyun
```

**c)** Alternatif: Modeli sıfırdan eğitmek için (~2-3 dakika):

```bash
python src/pricing/pipeline.py
```

### 5. RAG Vektör Veritabanını Oluşturun

```bash
python src/rag/ingest.py
```

> Bu adım data/processed/ klasöründe knowledge_base.db dosyasını oluşturur.

### 6. Uygulamayı Başlatın

```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak **http://localhost:8501** adresi açılacaktır.

---

## 🐳 Docker ile Hızlı Başlangıç (Opsiyonel)

```bash
# Docker imajını derle
docker build -t autoinsight .

# Konteyneri başlat
docker run -p 8501:8501 autoinsight
```

> ⚠️ Docker yöntemiyle models/pricing_pipeline.joblib dosyasının mevcut olması gerekir.

---

## 📊 Model Başarım Metrikleri

53,514 araçlık kapsamlı veri seti (`cars1.csv`) üzerinde yapılan test (%20 test ayrımı - 10,703 araç) sonuçları:

| Metrik | Skor | Açıklama |
| :--- | :--- | :--- |
| **R² (Belirleme Katsayısı)** | **0.9511** | Fiyat varyansını açıklama başarımı (~%95.1) |
| **MAE (Ortalama Mutlak Hata)** | **64,802 TL** | Gerçek fiyattan ortalama mutlak sapma tutarı |
| **RMSE (Kareli Ortalama Hata)**| **103,597 TL** | Büyük sapmaları cezalandıran hata metriği |
| **MAPE (Yüzdesel Hata)** | **%10.17** | Ortalama yüzdesel sapma oranı |

---

## 📁 Proje Dizin Yapısı

```text
autoinsight/
├── data/
│   ├── raw/
│   │   └── cars1.csv         # 53K+ araçlık ham eğitim veri seti (~7 MB)
│   └── processed/            # SQLite yerel vektör veri tabanı (knowledge_base.db)
├── docs/                     # RAG için teknik bülten ve bakım kılavuzları
├── models/                   # Eğitilen model dosyası — git'te YOK, Drive'dan indirin (bkz. Adım 4)
├── src/
│   ├── config.py             # Dinamik şema ve merkezi dizin yapılandırması
│   ├── pricing/              # Fiyat tahmin modeli ve eğitim hattı
│   ├── rag/                  # Vektörleme ve anlamsal arama modülü
│   └── recommender/          # Filtreleme ve kosinüs benzerlik motoru
├── app.py                    # Streamlit dashboard arayüzü
├── Dockerfile                # Konteynerizasyon konfigürasyonu
└── requirements.txt          # Proje bağımlılıkları
```

---

## 🔧 Sık Karşılaşılan Sorunlar

| Sorun | Çözüm |
|-------|-------|
| `ModuleNotFoundError` | `venv`'i aktive ettiğinizden ve `pip install -r requirements.txt` çalıştırdığınızdan emin olun |
| `FileNotFoundError: pricing_pipeline.joblib` | Model dosyasını Google Drive'dan indirip `models/` klasörüne koyun (bkz. Adım 4) veya `python src/pricing/pipeline.py` ile eğitin |
| `FileNotFoundError: knowledge_base.db` | `python src/rag/ingest.py` komutunu çalıştırın (bkz. Adım 5) |
| Streamlit açılmıyor | `streamlit run app.py` komutunu `venv` aktifken çalıştırın |

---

## 🤝 Katkıda Bulunma

Bu repo özel (private) olup davetli geliştiricilere açıktır. Değişiklik yapmadan önce bir branch oluşturun:

```bash
git checkout -b feature/ozellik-adi
git add .
git commit -m "feat: kısa açıklama"
git push origin feature/ozellik-adi
```
