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
        # Kilometre anomalilerini elen (1M+ km'li araclar veri seti hatasi)
        filtered = filtered[filtered['kilometre'] <= 999_999]
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

        # Fiyat/Bütçe, Model Yılı ve Kilometre Ağırlıklı Puanlama Fonksiyonu
        def normalize_series(series, invert=False):
            min_val, max_val = series.min(), series.max()
            if max_val == min_val:
                return pd.Series(1.0, index=series.index)
            if invert:
                return (max_val - series) / (max_val - min_val)
            return (series - min_val) / (max_val - min_val)

        year_score = normalize_series(filtered['yil'], invert=False)
        km_score = normalize_series(filtered['kilometre'], invert=True)

        if max_budget is not None and max_budget > 0:
            # Bütçe odaklı arama: Kullanıcının bütçesini en verimli kullanan üst segment/değerli araçları önceliklendir
            price_norm = normalize_series(filtered[TARGET_COLUMN], invert=False)
            budget_ratio = (filtered[TARGET_COLUMN] / max_budget).clip(upper=1.0)
            budget_score = budget_ratio * 0.35 + price_norm * 0.65

            filtered['match_score'] = (
                budget_score * 0.65 +
                year_score * 0.22 +
                km_score * 0.13
            ) * 100
        else:
            # Esnek arama: Yıl ve kilometre ağırlıklı dengeli sıralama
            budget_norm = normalize_series(filtered[TARGET_COLUMN], invert=False)
            filtered['match_score'] = (
                year_score * 0.45 +
                km_score * 0.35 +
                budget_norm * 0.20
            ) * 100

        result_cols = ['marka', 'seri', 'model', 'yil', 'kilometre', 'yakit_tipi', 'vites_tipi', TARGET_COLUMN, 'match_score']
        return filtered[result_cols].sort_values(by='match_score', ascending=False).head(top_n)

    def find_comparable_listings(
        self,
        marka: str,
        model: str,
        yil: int,
        km: float,
        predicted_price: float
    ) -> dict:
        """
        Benzer ilanları filtreler ve piyasa karşılaştırması verisi döner.
        Filtre: Aynı marka + model, yıl ±1, km ±%30.
        En az 10 eşleşme gerekir.
        """
        filtered = self.df[
            (self.df['marka'] == marka) &
            (self.df['model'] == model) &
            (self.df['yil'].between(yil - 1, yil + 1)) &
            (self.df['kilometre'].between(km * 0.7, km * 1.3))
        ].copy()

        if len(filtered) < 10:
            return {"sufficient": False, "count": len(filtered)}

        prices = filtered[TARGET_COLUMN].values
        avg_price = float(np.mean(prices))
        median_price = float(np.median(prices))
        count = len(filtered)

        # Yüzdelik konum: tahmin edilen fiyatın benzer ilanlar arasındaki yeri
        percentile = float(np.mean(prices <= predicted_price) * 100)

        # Ortalamadan sapma yüzdesi
        deviation_pct = ((predicted_price - avg_price) / avg_price) * 100

        # Yorum cümlesi üret
        if abs(deviation_pct) <= 5:
            comment = "Benzer ilanların ortalamasına yakın."
        elif deviation_pct > 5:
            if km < np.mean(filtered['kilometre']):
                comment = f"Benzer ilanlar içinde ortalamanın %{abs(deviation_pct):.0f} üzerinde. Kilometresi düşük olduğu için makul seviyede."
            else:
                comment = f"Benzer ilanlar içinde ortalamanın %{abs(deviation_pct):.0f} üzerinde."
        else:
            comment = f"Benzer ilanlar içinde ortalamanın %{abs(deviation_pct):.0f} altında."

        return {
            "sufficient": True,
            "count": count,
            "avg_price": avg_price,
            "median_price": median_price,
            "percentile": percentile,
            "deviation_pct": deviation_pct,
            "comment": comment
        }

    def find_similar_vehicles(self, car_index: int, top_n: int = 5) -> pd.DataFrame:
        """Seçilen bir araca en yakın alternatifleri Cosine Similarity ile bulur."""
        features = ['yil', 'kilometre', TARGET_COLUMN]
        
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