import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, TargetEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error

from src.config import DATA_RAW_PATH, MODEL_SAVE_PATH, TARGET_COLUMN, NUMERIC_FEATURES, CATEGORICAL_FEATURES

def build_dynamic_pipeline(num_cols, cat_cols):
    """Veri setindeki eksik değerleri yöneten ve dinamik şemaya göre eğitilen boru hattı."""
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('encoder', TargetEncoder(target_type='continuous', smooth="auto", cv=3))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_cols),
            ('cat', cat_transformer, cat_cols)
        ]
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    return pipeline

def train_and_save():
    if not os.path.exists(DATA_RAW_PATH):
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {DATA_RAW_PATH}")

    df = pd.read_csv(DATA_RAW_PATH)
    print(f"[*] Veri yüklendi. Toplam kayıt: {len(df)}")

    # Gerekli sütunların kontrolü
    available_num_cols = [col for col in NUMERIC_FEATURES if col in df.columns]
    available_cat_cols = [col for col in CATEGORICAL_FEATURES if col in df.columns]

    X = df[available_num_cols + available_cat_cols]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = build_dynamic_pipeline(available_num_cols, available_cat_cols)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100

    print("\n--- [Model Değerlendirme Sonuçları] ---")
    print(f"R² Skoru (Belirleme Katsayısı) : {r2:.4f}")
    print(f"MAE (Ortalama Mutlak Hata)    : {mae:,.2f} TL")
    print(f"RMSE (Kareli Ortalama Hata)   : {rmse:,.2f} TL")
    print(f"MAPE (Yüzdesel Hata)          : %{mape:.2f}")
    print("---------------------------------------")

    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_SAVE_PATH)
    print(f"[OK] Model basariyla kaydedildi: {MODEL_SAVE_PATH}\n")

if __name__ == "__main__":
    train_and_save()