"""
AutoInsight — Veri ve Model Yükleme Katmanı
Streamlit cache dekoratörlü veri/model yükleme fonksiyonları.
"""
import os
import joblib
import pandas as pd
import streamlit as st

from src.config import DATA_RAW_PATH, MODEL_SAVE_PATH


@st.cache_data
def load_app_data() -> pd.DataFrame:
    """
    Ham araç veri setini yükler ve önbelleğe alır.
    Uygulama yeniden başlamadıkça tekrar okunmaz.
    """
    return pd.read_csv(DATA_RAW_PATH)


@st.cache_resource
def load_app_model():
    """
    Eğitilmiş fiyatlandırma pipeline'ını yükler ve önbelleğe alır.
    Model dosyası bulunamazsa None döner.
    """
    return joblib.load(MODEL_SAVE_PATH) if os.path.exists(MODEL_SAVE_PATH) else None
