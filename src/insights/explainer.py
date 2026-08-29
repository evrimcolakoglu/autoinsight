"""
AutoInsight — Yerel Yapay Zeka Pazar Açıklama Motoru (Data-Grounded Market Explainer)
Tamamen yerel, ücretsiz ve veri setindeki gerçek piyasa metriklerine sadık kalarak
araçların değerleme ve öneri gerekçelerini tam 3-4 cümlelik uzman özetlerine dönüştürür.
"""
import pandas as pd
from typing import Dict, Any, Optional


class MarketInsightExplainer:
    """Veri tabanlı pazar dinamiklerini doğal dil açıklamalarına dönüştüren motor."""

    @staticmethod
    def _format_model_name(brand: str, seri: str, model: str) -> str:
        """Marka, seri ve model isimlerini tekrarsız ve temiz biçimde birleştirir."""
        brand_clean = str(brand or "").strip()
        seri_clean = str(seri or "").strip()
        model_clean = str(model or "").strip()

        if seri_clean and seri_clean.lower() in model_clean.lower():
            full_name = f"{brand_clean} {model_clean}".strip()
        elif seri_clean:
            full_name = f"{brand_clean} {seri_clean} {model_clean}".strip()
        else:
            full_name = f"{brand_clean} {model_clean}".strip()
        return full_name

    @staticmethod
    def _format_km_display(km: float) -> str:
        return f"{int(round(km)):,}".replace(",", ".")

    @staticmethod
    def _analyze_km_status(year: int, km: float) -> str:
        current_year = 2026
        age = max(1, current_year - year)
        annual_km = km / age

        if km <= 15000 and age <= 2:
            return "neredeyse sıfır ayarında olan çok düşük kilometresiyle mekanik yıpranma riskini tamamen minimize etmektedir"
        elif annual_km < 12000:
            return f"yıllık ortalama {int(annual_km):,} km ile pazar ortalamasının (15.000-20.000 km/yıl) belirgin şekilde altında kalarak kondisyonunu korumaktadır".replace(",", ".")
        elif annual_km <= 22000:
            return "ülke şartlarındaki ideal yıllık kullanım bareminde dengeli bir geçmişe sahiptir"
        else:
            return "yoğun ve uzun yol odaklı kullanılmış olmasına karşın sınıfının dayanıklı mekanik standartlarında pazar değerini korumaktadır"

    @staticmethod
    def _analyze_powertrain(fuel: str, transmission: str) -> str:
        fuel_clean = str(fuel or "").strip().lower()
        trans_clean = str(transmission or "").strip().lower()

        is_auto = "otomatik" in trans_clean or "yarı" in trans_clean
        is_diesel = "dizel" in fuel_clean
        is_hybrid = "hibrit" in fuel_clean
        is_electric = "elektrik" in fuel_clean
        is_gasoline = "benzin" in fuel_clean

        if is_auto and is_diesel:
            return "Dizel motorun uzun yol yakıt ekonomisi ile otomatik şanzımanın sürüş konforu, modelin ikinci el pazarındaki likiditesini ve değer koruma potansiyelini artıran başlıca etkendir."
        elif is_auto and is_hybrid:
            return "Hibrit teknolojisinin şehir içi düşük yakıt tüketimi ile otomatik vites uyumu, modern çevre ve verimlilik normlarında güçlü bir pazar avantajı yaratmaktadır."
        elif is_electric:
            return "Elektrikli güç ünitesinin sıfır emisyon avantajı ve anlık tork karakteristiği, modern otomotiv trendlerinde öncü bir değer koridoru oluşturmaktadır."
        elif is_auto and is_gasoline:
            return "Benzinli motorun sessiz çalışma karakteri ve otomatik şanzıman kombinasyonu, özellikle şehir içi konfor odaklı kullanıcı profilinde yüksek talep görmektedir."
        elif not is_auto and is_diesel:
            return "Dizel motorun yüksek torku ve manuel şanzımanın düşük bakım maliyeti, aracın işletme giderlerini optimize ederek rasyonel bir pazar dengesi kurmaktadır."
        else:
            return "Mekanik aktarma organlarının sadeliği ve ekonomik yedek parça erişimi, aracın genel pazar talebini ve maliyet avantajını doğrudan desteklemektedir."

    @staticmethod
    def _analyze_body_utility(body: str, brand: str) -> str:
        body_clean = str(body or "").strip().lower()

        if "suv" in body_clean:
            return "Yüksek sürüş pozisyonu, ferah kabin mimarisi ve geniş yükleme alanı sunan SUV karoseri, günümüz pazarında aileler ve seyahat odaklı kullanıcılar için en popüler gövde tipidir."
        elif "sedan" in body_clean:
            return "Geniş bagaj hacmi, prestijli hatları ve dengeli yol tutuşuyla bilinen Sedan gövde formu, kurumsal ve geniş aile kullanımlarında oturmuş güçlü bir pazar karşılığına sahiptir."
        elif "hatchback" in body_clean:
            return "Kompakt dış boyutları ve pratik bagaj erişimiyle öne çıkan Hatchback yapısı, yoğun şehir trafiğinde kolay manevra ve park avantajı sağlayan dinamik bir seçenektir."
        elif "station" in body_clean or "wagon" in body_clean or "mpv" in body_clean:
            return "Maksimum fonksiyonellik ve modüler iç hacim sunan bu karoser tipi, çok amaçlı yükleme ve geniş aile yolculukları için üst düzey kullanım değeri sağlar."
        else:
            return f"{brand} markasının sınıfındaki mühendislik ve tasarım çizgisi, modelin genel pazar algısını ve segment gücünü pekiştirmektedir."

    @classmethod
    def generate_seller_explanation(
        cls,
        df: pd.DataFrame,
        car_data: Dict[str, Any],
        predicted_price: float,
        comparison: Dict[str, Any]
    ) -> str:
        """
        Piyasa Değerleme (Satıcı) ekranı için aracın tahmin edilen değer koridorunun
        nedenlerini açıklayan tam 3-4 cümlelik veri tabanlı uzman analizi üretir.
        """
        brand = car_data.get("marka", "Araç")
        seri = car_data.get("seri", "")
        model = car_data.get("model", "")
        year = int(car_data.get("yil", 2020))
        km = float(car_data.get("kilometre", 100000))
        fuel = car_data.get("yakit_tipi", "Benzin")
        trans = car_data.get("vites_tipi", "Düz")
        body = car_data.get("kasa_tipi", "Sedan")

        full_car_name = cls._format_model_name(brand, seri, model)
        km_formatted = cls._format_km_display(km)

        # 1. Cümle: Araç kimliği, model yılı ve kilometre kondisyon analizi
        km_desc = cls._analyze_km_status(year, km)
        sentence_1 = f"{year} model {full_car_name}, {km_formatted} km'lik mevcut kullanımıyla {km_desc}."

        # 2. Cümle: Yakıt ve vites aktarma organı analizi
        sentence_2 = cls._analyze_powertrain(fuel, trans)

        # 3. Cümle: Kasa tipi ve kullanım amacı analizi
        sentence_3 = cls._analyze_body_utility(body, brand)

        # 4. Cümle: Pazar verisi emsal kıyaslaması ve fiyat koridoru sonucu
        if comparison and comparison.get("sufficient"):
            count = comparison.get("count", 0)
            avg_price = comparison.get("avg_price", predicted_price)
            diff_pct = ((predicted_price - avg_price) / avg_price) * 100

            if abs(diff_pct) <= 5:
                sentence_4 = f"Sistemimizdeki {count} adet aktif emsal ilan verisine göre aracınız, piyasa ortalamasına ({int(round(avg_price)):,} TL) tam uyumlu ve dengeli bir değerleme koridorunda yer almaktadır.".replace(",", ".")
            elif diff_pct > 5:
                sentence_4 = f"Veritabanımızdaki {count} adet benzer ilanla yapılan kıyaslamada araç, düşük kullanım yıpranması sayesinde pazar ortalamasının %{abs(diff_pct):.0f} üzerinde, üst segment fiyat bandında değerlenmektedir."
            else:
                sentence_4 = f"İncelenen {count} adet emsal ilana kıyasla araç, alıcılar için rekabetçi ve hızlı satılabilir avantajlı bir fiyat koridorunda bulunmaktadır."
        else:
            sentence_4 = "53.000'i aşkın gerçek pazar verisinin regresyon analizine göre belirlenen bu fiyat aralığı, aracın donanım ve kondisyon kombinasyonunun güncel piyasa karşılığını objektif biçimde yansıtmaktadır."

        return f"{sentence_1} {sentence_2} {sentence_3} {sentence_4}"

    @classmethod
    def generate_buyer_explanation(
        cls,
        df: pd.DataFrame,
        car_dict: Dict[str, Any],
        market_value: Optional[float] = None
    ) -> str:
        """
        Akıllı Araç Keşfi (Alıcı) ekranında önerilen her araç için
        fiyatının o seviyede olmasının gerekçelerini aktaran tam 3-4 cümlelik özet üretir.
        """
        brand = car_dict.get("marka", "Araç")
        seri = car_dict.get("seri", "")
        model = car_dict.get("model", "")
        year = int(car_dict.get("yil", 2020))
        km = float(car_dict.get("km", 100000))
        fuel = car_dict.get("yakit", "Benzin")
        trans = car_dict.get("vites", "Düz")
        body = car_dict.get("kasa", "Sedan")

        full_car_name = cls._format_model_name(brand, seri, model)
        km_formatted = cls._format_km_display(km)

        # 1. Cümle: Segment ve kilometre konumu
        km_desc = cls._analyze_km_status(year, km)
        sentence_1 = f"Bu {year} model {full_car_name}, {km_formatted} km ile {km_desc}."

        # 2. Cümle: Güç ünitesi & ekonomi avantajı
        sentence_2 = cls._analyze_powertrain(fuel, trans)

        # 3. Cümle: Karoser & kullanım amacı
        sentence_3 = cls._analyze_body_utility(body, brand)

        # 4. Cümle: Fiyat/Performans ve segment sonucu
        if market_value is not None and market_value > 2_000_000:
            sentence_4 = "Sunduğu yüksek donanım seviyesi, güncel model yılı ve pazar prestiji, aracın bütçeniz dahilindeki en seçkin üst segment alternatifler arasında yer almasını sağlamaktadır."
        elif market_value is not None and market_value < 750_000:
            sentence_4 = "Ekonomik yürütme maliyetleri ve yüksek parça bulunabilirliği, bu aracı belirlenen bütçede rasyonel bir fiyat/performans fırsatı haline getirmektedir."
        else:
            sentence_4 = "Piyasa standartlarındaki dengeli değer koridoru ve güçlü ikinci el talep yapısı sayesinde bütçenizi en verimli şekilde değerlendiren ideal bir seçenektir."

        return f"{sentence_1} {sentence_2} {sentence_3} {sentence_4}"
