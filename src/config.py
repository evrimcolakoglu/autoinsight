import os

# Temel Dizin Yolları
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "cars1.csv")
MODEL_SAVE_PATH = os.path.join(BASE_DIR, "models", "pricing_pipeline.joblib")
DB_PATH = os.path.join(BASE_DIR, "data", "processed", "knowledge_base.db")

# Dinamik Veri Şeması (Yeni veri seti geldiğinde sadece burası değişir)
TARGET_COLUMN = "fiyat"

NUMERIC_FEATURES = [
    "yil",
    "kilometre",
    "motor_hacmi",
    "motor_gucu",
    "ortalama_yakit_tuketimi",
    "yakit_deposu",
    "tramer",
    "degisen",
    "boyali"
]

CATEGORICAL_FEATURES = [
    "marka",
    "seri",
    "model",
    "vites_tipi",
    "yakit_tipi",
    "kasa_tipi",
    "cekis",
    "konum"
]

# Model performans metriği — fiyat aralığı hesaplamasında kullanılır
# tahmin × (1 - MAPE) ... tahmin × (1 + MAPE)
MODEL_MAPE = 0.101