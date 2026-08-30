# 🚗 AutoInsight: Akıllı Otomotiv Karar ve Değerleme Platformu

AutoInsight, ikinci el otomotiv pazarı için geliştirilmiş; yapay zeka tabanlı dinamik piyasa fiyat tahmini, bütçe ve donanım odaklı akıllı araç keşfi, veri tabanlı pazar analiz motoru ve çevrimdışı (offline) RAG mimarisini modern Apple Pro Scrollytelling web vitrini ve analitik platformunda buluşturan uçtan uca bir makine öğrenmesi sistemidir.

---

## 📌 Temel Yetenekler & Modüller

* **🎯 Dinamik Piyasa Değerleme (ML Engine):** 53.514 gerçek pazar verisi üzerinden eğitilmiş Random Forest + Target Encoding regresyon boru hattı ile 46 marka, model, yıl, kilometre ve donanım kombinasyonlarına göre anlık **Piyasa Değer Aralığı** (%11.09 MAPE güven koridoru), emsal yüzdelik konumu ve araca özel yapay zeka pazar gerekçesi sunar.
* **🏎️ Akıllı Araç Keşfi (Recommender):** Kullanıcının bütçe sınırına veya esnek donanım tercihlerine göre piyasa fırsatlarını bütçe-ağırlıklı puanlama algoritmalarıyla listeleyen ve her araç için modelin tahmin ettiği değer aralığını ve özel analizini aktaran akıllı öneri motoru (İlk 20 Eşleşme).
* **🍏 Apple Pro Scrollytelling Web Vitrini (Next.js 14 + Lenis):** Pürüzsüz ataletli kaydırma (Lenis Scroll), scroll-pinned genişleyen araç sahnesi, hareketli lazer tarayıcı, canlı telemetri göstergeleri, etkileşimli imleç ışığı (cursor spotlight) ve 4'lü mühendislik bento ızgarası.
* **🎨 Modüler Streamlit Platformu (Python):** Özel tasarlanmış Dark Glassmorphism tema, canlı radar ticker, simetrik donanım kartları ve izole ekran mimarisi.
* **📚 Çevrimdışı RAG Teknik Asistanı:** Harici API veya internet bağımlılığı olmaksızın teknik kılavuzlardan ve pazar bültenlerinden anlamsal bilgi getiren yerel vektör arama motoru (SQLite + Sentence Transformers `all-MiniLM-L6-v2`).
* **🧠 Veri Tabanlı Yapay Zeka Pazar Açıklaması (NLG):** Her aracın marka mirası, yaşı, kilometresi, yakıt/vites kombinasyonu ve şehrine göre tamamen dinamik ve özelleştirilmiş 3-4 cümlelik pazar analizleri.

---

## 🏗️ Sistem ve Proje Mimarisi

```text
AutoInsight Platform
│
├── [ Next.js 14 Web Vitrini ] ────► (App Router + Tailwind CSS + Framer Motion + Lenis Scroll)
│        │
│        ├── Ana Sayfa (/)      ──► (Hero Pinned Stage, Canlı Telemetri, Bento Grid, Süreç)
│        ├── Değerleme (/degerleme) ► (Tüm 46 Marka, Kademeli Seçim, Değer Aralığı HUD, AI Raporu)
│        └── Keşif (/kesif)     ──► (Bütçeli/Esnek Arama, İlk 20 Araç, Tahmini Değer Aralığı, AI Analizi)
│
├── [ Streamlit Analitik UI ]  ────► (app.py + İzole Ekranlar + Glassmorphism Teması)
│        │
│        ├── Welcome Ekranı     ──► (Sinematik Hero, Telemetri Barı, Bento Mimari)
│        ├── Seller Ekranı      ──► (Dinamik Parametrik Form + Değerleme Raporu HUD)
│        └── Buyer Ekranı       ──► (Bütçe & Donanım Filtreleri + Eşleşen Araç Kartları)
│
├── [ ML Fiyatlandırma ]       ────► (Scikit-Learn: TargetEncoder + StandardScaler + RandomForest)
│
├── [ Öneri Motoru ]           ────► (Bütçe Optimizasyonu + Min-Max Normalizasyonu + Sıralama)
│
└── [ Yerel RAG Modülü ]       ────► (SQLite Vektör Deposu + all-MiniLM-L6-v2 Embedding)
```

---

## 👥 Geliştirici Kurulum Rehberi

### Ön Gereksinimler

* **Python:** 3.10 veya üzeri ([python.org](https://www.python.org/downloads/))
* **Node.js:** v18.0 veya üzeri ([nodejs.org](https://nodejs.org/))
* **Git:** Herhangi bir güncel sürüm ([git-scm.com](https://git-scm.com/))

---

### 1. Repoyu Klonlayın

```bash
git clone https://github.com/evrimcolakoglu/autoinsight.git
cd autoinsight
```

---

### 2. Python Backend & Streamlit Kurulumu

#### A) Sanal Ortamı (venv) Oluşturun ve Aktif Edin:

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

#### B) Python Bağımlılıklarını Yükleyin:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### C) Eğitilmiş Modeli Hazırlayın:
Fiyatlandırma model dosyası (`pricing_pipeline.joblib`) dosya boyutu (~350 MB) nedeniyle Git takibinde değildir. İki yöntemden birini seçebilirsiniz:

* **Yöntem 1 (Önerilen - İndirme):**  
  👉 **[pricing_pipeline.joblib — Google Drive İndirme Bağlantısı](https://drive.google.com/drive/folders/1ifLAcUbWEbOvHWeJnqaV68JAtO4aQPdb?usp=sharing)** dosyasını indirip `models/` klasörüne yerleştirin.
* **Yöntem 2 (Sıfırdan Eğitme):**  
  ```bash
  python -m src.pricing.pipeline
  ```

#### D) Streamlit Uygulamasını Başlatın:
```bash
streamlit run app.py
```
*(Tarayıcınızda otomatik olarak **http://localhost:8501** açılacaktır.)*

---

### 3. Next.js 14 Scrollytelling Web Uygulaması Kurulumu

```bash
cd frontend
npm install
npm run dev
```
*(Tarayıcınızda **http://localhost:3000** adresini açınız.)*

* **Üretim Derlemesi (Production Build):**
```bash
npm run build
npm run start
```

---

### 4. RAG Vektör Bilgi Tabanını Oluşturun (Opsiyonel)

Doküman tabanını vektörleştirip yerel SQLite veritabanına işlemek için:
```bash
python -m src.rag.ingest
```

---

## 📁 Modüler Kod & Dizin Hiyerarşisi

```text
autoinsight/
├── app.py                         # Streamlit ana giriş noktası & Router
├── requirements.txt               # Python kütüphane bağımlılıkları
├── README.md                      # Proje dokümantasyonu
│
├── frontend/                      # Next.js 14 Apple Pro Web Vitrini
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx         # Root Layout, fontlar & SmoothScrollProvider
│   │   │   ├── page.tsx           # Scrollytelling Ana Sayfa
│   │   │   ├── degerleme/         # Tüm 46 Markalı Piyasa Değerleme Sayfası
│   │   │   └── kesif/             # Akıllı Araç Keşfi & Öneri Sayfası
│   │   ├── components/
│   │   │   ├── hero/              # Pinned expanding hero & lazer HUD
│   │   │   ├── background/        # Dinamik ambient gradyan orbları & imleç ışığı
│   │   │   ├── navbar/            # StickySubNav cam navigasyon
│   │   │   ├── seller/            # SellerScreen değerleme bileşeni
│   │   │   ├── buyer/             # BuyerScreen araç keşfi bileşeni
│   │   │   ├── bento/             # BentoGridSection mimari paneli
│   │   │   ├── cockpit/           # CockpitShowcase telemetri merkezi
│   │   │   └── metrics/           # HighlightsSection sayaçları
│   │   └── lib/
│   │       ├── valuationEngine.ts # İstemci tarafı değerleme & çeşitli AI analiz motoru
│   │       └── recommenderEngine.ts # İlk 20 araç puanlama & filtreleme motoru
│   └── package.json
│
├── assets/                        # Görsel varlıklar (Değerleme stüdyosu, Pazar merkezi)
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
    ├── config.py                  # Merkezi konfigürasyon ve veri yolları
    ├── ui/                        # Streamlit Kullanıcı Arayüzü
    │   ├── icons.py               # Vektörel SVG ikon kütüphanesi
    │   ├── components.py          # Yardımcı UI fonksiyonları
    │   ├── styles.py              # CSS & Animasyon motoru
    │   ├── data_loader.py         # Önbellekli veri ve model yükleyici
    │   └── screens/               # Welcome, Seller, Buyer ekran modülleri
    ├── insights/
    │   └── explainer.py           # Veri tabanlı pazar açıklama ve gerekçe motoru
    ├── pricing/
    │   └── pipeline.py            # ML model eğitim ve kayıt hattı
    ├── recommender/
    │   └── engine.py              # Bütçe-ağırlıklı öneri algoritması
    └── rag/
        ├── ingest.py              # Doküman parçalama ve vektörleme
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
| `ModuleNotFoundError: No module named 'src'` | Çalışma dizini yanlış | Komutları projenin kök dizininde (`autoinsight/`) çalıştırın. |
| `FileNotFoundError: pricing_pipeline.joblib` | Model dosyası eksik | Google Drive'dan indirip `models/` içine koyun veya `python -m src.pricing.pipeline` çalıştırın. |
| `Port 3000 is already in use` | Başka bir Next.js örneği açık | `npx kill-port 3000` çalıştırın veya `npm run dev -- -p 3001` ile farklı portta açın. |
| `WinError 10054` Soket Logu | Tarayıcı sekmesi kapatıldı/yenilendi | `app.py` içine Windows Selector EventLoop politikası eklenmiştir; uygulamanın çalışmasını etkilemez. |

---

## 👥 Geliştiriciler & Telif Hakkı (Authors & Copyright)

Bu proje **Evrim Çolakoğlu** ve **Ayşenur Çelik** tarafından geliştirilmiştir.

* **Evrim Çolakoğlu** — [GitHub](https://github.com/evrimcolakoglu)
* **Ayşenur Çelik** — [GitHub](https://github.com/aysenurcelik-swe)

---

## 📜 Lisans & Atıf (License & Citation)

Bu proje **GNU General Public License v3.0 (GPL-3.0)** altında lisanslanmıştır. Detaylı bilgi için [LICENSE](LICENSE) dosyasını inceleyebilirsiniz.

Bu projeyi akademik çalışmalarda, araştırmalarda veya açık kaynak projelerinizde kullanırken veya referans gösterirken aşağıdaki şekilde atıfta bulunmanız rica olunur:

```bibtex
@misc{autoinsight2024,
  author = {Çolakoğlu, Evrim and Çelik, Ayşenur},
  title = {AutoInsight: Akıllı Otomotiv Karar ve Değerleme Platformu},
  year = {2024},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/evrimcolakoglu/autoinsight}}
}
```

> ⚠️ **Telif ve Kullanım Koşulları:** GNU GPLv3 lisansı uyarınca bu projenin kaynak kodlarını kullanan, dağıtan veya türeten tüm çalışmalar açık kaynak kalmak ve orijinal geliştiricileri (**Evrim Çolakoğlu & Ayşenur Çelik**) açıkça belirtmek zorundadır. Projenin kaynak gösterilmeden veya kapalı kaynaklı ticari mülk olarak sahiplenilmesi yasal olarak yasaktır.
