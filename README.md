# 🚗 AutoInsight: Akıllı Otomotiv Karar ve Değerleme Platformu

AutoInsight, ikinci el otomotiv pazarı için geliştirilmiş; yapay zeka tabanlı dinamik piyasa fiyat tahmini, bütçe ve donanım odaklı akıllı araç eşleştirme ile çevrimdışı (offline) RAG mimarisini modern ve profesyonel bir web arayüzünde buluşturan uçtan uca makine öğrenmesi platformudur.

---

## 📌 Temel Yetenekler & Modüller

* **🎯 Dinamik Piyasa Değerleme (ML Engine):** 53.000+ gerçek pazar verisi üzerinden eğitilmiş Random Forest + Target Encoding regresyon boru hattı ile marka, model, yıl, kilometre ve donanım kombinasyonlarına göre anlık değerleme koridoru (%11 MAPE) ve emsal analizi sunar.
* **🏎️ Akıllı Araç Keşfi (Recommender):** Kullanıcının bütçe sınırına, yakıt, vites, kasa ve model yılı tercihlerine göre piyasa fırsatlarını bütçe-ağırlıklı ve benzerlik tabanlı skorlama algoritmalarıyla listeleyen akıllı öneri motoru.
* **🎨 Modern & Modüler UI (Streamlit Custom Engine):** Özel tasarlanmış Dark Glassmorphism tema, canlı radar ticker, simetrik donanım kartları ve duyarlı mikro animasyonlar.
* **📚 Çevrimdışı RAG Teknik Asistanı:** Harici API veya internet bağımlılığı olmaksızın teknik kılavuzlardan ve bakım bültenlerinden anlamsal bilgi getiren yerel vektör arama motoru (SQLite + Sentence Transformers `all-MiniLM-L6-v2`).

---

## 🏗️ Sistem ve Proje Mimarisi

```text
AutoInsight Platform
│
├── [ UI & Sunum Katmanı ] ───► (Streamlit + Özel Glassmorphism CSS + Vektörel İkonlar)
│        │
│        ├── Welcome Ekranı   ──► (Hero, Canlı Radar, Bento Grid, İstatistikler)
│        ├── Seller Ekranı    ──► (Dinamik Parametrik Form + Değerleme Raporu HUD)
│        └── Buyer Ekranı     ──► (Bütçe & Donanım Filtreleri + Eşleşen Araç Kartları)
│
├── [ ML Fiyatlandırma ]   ───► (Scikit-Learn Pipeline: TargetEncoder + StandardScaler + RandomForest)
│
├── [ Öneri Motoru ]       ───► (Bütçe Optimizasyonu + Min-Max Normalizasyonu + Cosine Similarity)
│
└── [ Yerel RAG Modülü ]   ───► (SQLite Vektör Deposu + all-MiniLM-L6-v2 Embedding)
```

---

## 👥 Geliştirici Kurulum Rehberi

> Farklı bir bilgisayara projeyi kurarken aşağıdaki adımları sırasıyla takip ediniz.

### Ön Gereksinimler

* **Python:** 3.10 veya üzeri ([python.org](https://www.python.org/downloads/))
* **Git:** Herhangi bir güncel sürüm ([git-scm.com](https://git-scm.com/))

---

### 1. Repoyu Klonlayın

```bash
git clone https://github.com/evrimcolakoglu/autoinsight.git
cd autoinsight
```

---

### 2. Sanal Ortamı (venv) Oluşturun ve Aktif Edin

**Windows (PowerShell / CMD):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 Aktivasyon başarılı olduğunda terminal satırınızın başında `(venv)` ibaresi görünür.

---

### 3. Bağımlılıkları Yükleyin

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Eğitilmiş Modeli Hazırlayın

Fiyatlandırma model dosyası (`pricing_pipeline.joblib`) dosya boyutu (~350 MB) nedeniyle Git takibinde değildir. İki yöntemden birini seçebilirsiniz:

#### Yöntem A: Hazır Modeli İndirin (Önerilen)
1. Model dosyasını indirin:  
   👉 **[pricing_pipeline.joblib — Google Drive İndirme Bağlantısı](https://drive.google.com/drive/folders/1ifLAcUbWEbOvHWeJnqaV68JAtO4aQPdb?usp=sharing)**
2. İndirilen `pricing_pipeline.joblib` dosyasını projedeki `models/` klasörünün içine yerleştirin:
   ```text
   autoinsight/
   └── models/
       └── pricing_pipeline.joblib   ✅
   ```

#### Yöntem B: Modeli Sıfırdan Eğitin
Mevcut `cars1.csv` veri seti üzerinden modeli yerel olarak eğitmek için:
```bash
python -m src.pricing.pipeline
```
*(Eğitim donanımınıza bağlı olarak ~1-2 dakika sürer ve modeli otomatik olarak `models/` dizinine kaydeder.)*

---

### 5. RAG Vektör Bilgi Tabanını Oluşturun (Opsiyonel)

Doküman tabanını vektörleştirip yerel SQLite veritabanına işlemek için:
```bash
python -m src.rag.ingest
```
*(Bu komut `data/processed/knowledge_base.db` dosyasını oluşturur.)*

---

### 6. Uygulamayı Başlatın 🚀

```bash
streamlit run app.py
```
*(Veya: `python -m streamlit run app.py`)*

Tarayıcınızda otomatik olarak **http://localhost:8501** adresi açılacaktır.

---

## 📁 Modüler Kod & Dizin Hiyerarşisi

```text
autoinsight/
├── app.py                         # Ana giriş noktası & ekran yönlendirici (Router)
├── Dockerfile                     # Docker konteyner konfigürasyonu
├── requirements.txt               # Python kütüphane bağımlılıkları
├── README.md                      # Proje dokümantasyonu
│
├── data/
│   ├── raw/
│   │   └── cars1.csv              # 53.514 satırlık ham araç pazar veri seti (~7 MB)
│   └── processed/
│       └── knowledge_base.db      # RAG yerel SQLite vektör veritabanı
│
├── models/
│   └── pricing_pipeline.joblib    # Eğitilmiş RandomForest fiyatlandırma pipeline'ı
│
├── docs/                          # RAG için teknik bülten ve kılavuz dokümanları
│
└── src/
    ├── __init__.py
    ├── config.py                  # Merkezi konfigürasyon, dinamik veri şeması ve yollar
    │
    ├── ui/                        # Kullanıcı Arayüzü & Sunum Katmanı
    │   ├── __init__.py
    │   ├── icons.py               # Vektörel SVG ikonlar ve Logo kütüphanesi
    │   ├── components.py          # format_price, format_km, raw_html ve navigasyon
    │   ├── styles.py              # Merkezi CSS motoru & Glassmorphism teması
    │   ├── data_loader.py         # @st.cache destekli veri ve model yükleyici
    │   └── screens/               # İzole Ekran Modülleri
    │       ├── __init__.py
    │       ├── welcome.py         # Vitrin, Hero ve Canlı Radar Ekranı
    │       ├── seller.py          # Araç Değerleme & Emsal Analiz Ekranı
    │       └── buyer.py           # Akıllı Araç Keşfi & Öneri Listesi Ekranı
    │
    ├── pricing/
    │   ├── __init__.py
    │   └── pipeline.py            # ML model eğitim ve kayıt hattı
    │
    ├── recommender/
    │   ├── __init__.py
    │   └── engine.py              # Bütçe-ağırlıklı öneri ve karşılaştırma algoritması
    │
    └── rag/
        ├── __init__.py
        ├── ingest.py              # Doküman parçalama (chunking) ve vektörleme
        └── retriever.py           # Kosinüs benzerliğiyle yerel doküman arama
```

---

## 📊 Model Performans ve Doğrulama Metrikleri

53.514 araçlık veri seti üzerinde %20 test ayrımı (10.703 test örneği) ile elde edilen başarım metrikleri:

| Metrik | Değer | Açıklama |
| :--- | :--- | :--- |
| **R² (Belirleme Katsayısı)** | **0.9398** | Fiyat varyansını açıklama oranı (~%94.0) |
| **MAE (Ortalama Mutlak Hata)** | **72.524 TL** | Gerçek ve tahmin edilen fiyat arası ortalama mutlak fark |
| **RMSE (Kök Ortalama Kare Hata)**| **114.963 TL**| Uç sapmaları cezalandıran kareli hata |
| **MAPE (Ortalama Yüzdesel Hata)**| **%11.09** | Tahmin güven koridoru aralığı |

---

## 🔧 Sık Karşılaşılan Sorunlar ve Çözümleri

| Hata / Durum | Olası Neden | Çözüm |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'src'` | Çalışma dizini yanlış veya Python yolu tanımsız | Komutları projenin kök dizininde (`autoinsight/`) çalıştırın. |
| `FileNotFoundError: pricing_pipeline.joblib` | Model dosyası eksik | Google Drive'dan indirip `models/` içine koyun veya `python -m src.pricing.pipeline` çalıştırın. |
| `Streamlit command not found` | Sanal ortam aktif değil | Windows için `.\venv\Scripts\activate`, Linux/Mac için `source venv/bin/activate` yapın. |
| Port çakışması (`Port 8501 is already in use`) | Başka bir Streamlit örneği çalışıyor | `streamlit run app.py --server.port 8502` ile farklı portta başlatın. |

---

## 📄 Lisans & Katkı

Bu proje özel bir çalışma olup tüm hakları saklıdır.
İletişim ve sorularınız için proje yöneticisi ile irtibata geçebilirsiniz.
