import sampleCars from "@/data/sample_cars.json";

export interface RecommenderFilters {
  max_budget?: number;
  min_year?: number;
  max_km?: number;
  fuel_type?: string;
  gear_type?: string;
  body_type?: string;
  preferred_brand?: string;
  city?: string;
}

export interface VehicleMatch {
  marka: string;
  seri: string;
  model: string;
  yil: number;
  kilometre: number;
  vites_tipi: string;
  yakit_tipi: string;
  kasa_tipi: string;
  konum: string;
  fiyat: number;
  score: number;
  tag: string;
  ai_insight: string;
}

export function recommendVehicles(filters: RecommenderFilters): VehicleMatch[] {
  let candidates = [...sampleCars];

  // Hard filter criteria
  if (filters.preferred_brand && filters.preferred_brand !== "Tümü") {
    candidates = candidates.filter((c) => c.marka.toLowerCase() === filters.preferred_brand!.toLowerCase());
  }

  if (filters.fuel_type && filters.fuel_type !== "Tümü") {
    candidates = candidates.filter((c) => c.yakit_tipi.toLowerCase() === filters.fuel_type!.toLowerCase());
  }

  if (filters.gear_type && filters.gear_type !== "Tümü") {
    candidates = candidates.filter((c) => c.vites_tipi.toLowerCase() === filters.gear_type!.toLowerCase());
  }

  if (filters.body_type && filters.body_type !== "Tümü") {
    candidates = candidates.filter((c) => c.kasa_tipi.toLowerCase() === filters.body_type!.toLowerCase());
  }

  if (filters.city && filters.city !== "Tümü") {
    candidates = candidates.filter((c) => c.konum.toLowerCase() === filters.city!.toLowerCase());
  }

  if (filters.min_year) {
    candidates = candidates.filter((c) => c.yil >= filters.min_year!);
  }

  if (filters.max_km) {
    candidates = candidates.filter((c) => c.kilometre <= filters.max_km!);
  }

  if (filters.max_budget) {
    candidates = candidates.filter((c) => c.fiyat <= filters.max_budget!);
  }

  if (candidates.length === 0) {
    return [];
  }

  // Scoring and ranking
  const maxYear = 2024;
  const minYear = 2000;

  const scored = candidates.map((car) => {
    let score = 0;
    const yearNorm = Math.max(0, Math.min(1, (car.yil - minYear) / (maxYear - minYear)));
    const kmNorm = Math.max(0, Math.min(1, 1 - car.kilometre / 300000));

    if (filters.max_budget && filters.max_budget > 0) {
      // Budget-aware scoring: favors cars close to budget without exceeding
      const budgetEfficiency = car.fiyat / filters.max_budget;
      score = budgetEfficiency * 0.65 + yearNorm * 0.22 + kmNorm * 0.13;
    } else {
      // Criteria-based flexible scoring
      score = yearNorm * 0.45 + kmNorm * 0.35 + (1 - Math.min(1, car.fiyat / 4000000)) * 0.20;
    }

    // Assign dynamic tags
    let tag = "FİYAT / PERFORMANS";
    if (car.kilometre < 50000) tag = "DÜŞÜK KM AVANTAJI";
    else if (filters.max_budget && car.fiyat >= filters.max_budget * 0.88) tag = "BÜTÇE OPTİMİZE";
    else if (car.yil >= 2021) tag = "YENİ NESİL MODEL";

    // Generate 3-4 sentence Turkish local AI Market Rationale for each vehicle
    const kmText = car.kilometre < 70000
      ? `${car.kilometre.toLocaleString("tr-TR")} km seviyesi ile yaşıtlarına göre oldukça düşük yıpranmaya sahiptir`
      : `${car.kilometre.toLocaleString("tr-TR")} km seviyesiyle pazar ortalamasına uygun ve dengeli bir fiyat bandında yer almaktadır`;

    const fuelGearText = `${car.yakit_tipi} yakıt ve ${car.vites_tipi.toLowerCase()} vites kombinasyonu, ${car.konum} bölgesel pazarında yüksek alıcı talebi görmektedir.`;

    const bodyText = `${car.kasa_tipi} karoser yapısı konfor ve günlük kullanım dengesini mükemmel sağlarken, ${car.fiyat.toLocaleString("tr-TR")} TL fiyat etiketi emsal piyasa şartlarında güçlü bir yatırım koridoru oluşturmaktadır.`;

    const ai_insight = `${car.marka} ${car.seri} ${car.model} (${car.yil}), ${kmText}. ${fuelGearText} ${bodyText}`;

    return {
      ...car,
      score,
      tag,
      ai_insight,
    };
  });

  // Sort descending by score and pick top 20
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, 20);
}
