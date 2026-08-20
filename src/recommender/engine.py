import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_RAW_PATH, TARGET_COLUMN

class VehicleRecommender:
    def __init__(self, data_path: str = DATA_RAW_PATH):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Veri seti bulunamadı: {data_path}")
        self.df = pd.read_csv(data_path)

    def recommend_by_preferences(
        self,
        max_budget: float = None,
        preferred_fuel: str = None,
        preferred_transmission: str = None,
        preferred_kasa: str = None,
        max_km: float = None,
        min_year: int = None,
        top_n: int = 5
    ) -> pd.DataFrame:
        """Kullanıcı tercihlerine göre filtreleme yapar ve en avantajlı araçları puanlar."""
        filtered = self.df.copy()

        # Sert Filtreler (Hard Filtering)
        if max_budget is not None and max_budget > 0:
            filtered = filtered[filtered[TARGET_COLUMN] <= max_budget]
        if preferred_fuel and preferred_fuel != "Tümü":
            filtered = filtered[filtered['yakit_tipi'].str.contains(preferred_fuel, case=False, na=False)]
        if preferred_transmission and preferred_transmission != "Tümü":
            filtered = filtered[filtered['vites_tipi'].str.contains(preferred_transmission, case=False, na=False)]
        if preferred_kasa and preferred_kasa != "Tümü":
            filtered = filtered[filtered['kasa_tipi'].str.contains(preferred_kasa, case=False, na=False)]
        if max_km is not None and max_km > 0:
            filtered = filtered[filtered['kilometre'] <= max_km]
        if min_year is not None and min_year > 0:
            filtered = filtered[filtered['yil'] >= min_year]

        if filtered.empty:
            return pd.DataFrame()

        # Fiyat/Performans & Uyum Puanlama Fonksiyonu
        def normalize_series(series, invert=False):
            min_val, max_val = series.min(), series.max()
            if max_val == min_val:
                return pd.Series(1.0, index=series.index)
            if invert:
                return (max_val - series) / (max_val - min_val)
            return (series - min_val) / (max_val - min_val)

        # Genç yıl (+), Düşük KM (+), Düşük Tüketim (+), Düşük Tramer (+)
        year_score = normalize_series(filtered['yil'], invert=False)
        km_score = normalize_series(filtered['kilometre'], invert=True)
        fuel_score = normalize_series(filtered['ortalama_yakit_tuketimi'], invert=True)
        tramer_score = normalize_series(filtered['tramer'], invert=True)

        filtered['match_score'] = (
            year_score * 0.35 +
            km_score * 0.30 +
            fuel_score * 0.20 +
            tramer_score * 0.15
        ) * 100

        result_cols = ['marka', 'seri', 'model', 'yil', 'kilometre', 'yakit_tipi', 'vites_tipi', TARGET_COLUMN, 'match_score']
        return filtered[result_cols].sort_values(by='match_score', ascending=False).head(top_n)

    def find_similar_vehicles(self, car_index: int, top_n: int = 5) -> pd.DataFrame:
        """Seçilen bir araca en yakın alternatifleri Cosine Similarity ile bulur."""
        features = ['yil', 'kilometre', 'motor_gucu', 'ortalama_yakit_tuketimi', TARGET_COLUMN]
        
        scaler = MinMaxScaler()
        scaled_matrix = scaler.fit_transform(self.df[features])

        target_vector = scaled_matrix[car_index].reshape(1, -1)
        similarities = cosine_similarity(target_vector, scaled_matrix)[0]

        result = self.df.copy()
        result['similarity_score'] = similarities * 100

        # Kendisi hariç en benzerleri getir
        result = result.drop(index=car_index)
        result_cols = ['marka', 'seri', 'model', 'yil', 'kilometre', 'yakit_tipi', TARGET_COLUMN, 'similarity_score']
        return result[result_cols].sort_values(by='similarity_score', ascending=False).head(top_n)

if __name__ == "__main__":
    recommender = VehicleRecommender()
    print("--- [Bütçe & Kriter Tabanlı Öneri Testi] ---")
    recommendations = recommender.recommend_by_preferences(
        max_budget=1200000,
        preferred_transmission="Otomatik",
        top_n=3
    )
    print(recommendations.to_string(index=False))

    print("\n--- [Benzer Araç Bulma Testi (Index 0)] ---")
    similar_cars = recommender.find_similar_vehicles(car_index=0, top_n=3)
    print(similar_cars.to_string(index=False))