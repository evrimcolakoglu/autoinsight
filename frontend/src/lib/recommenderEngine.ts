import sampleCars from "@/data/sample_cars.json";
import { calculateValuation, generateDiverseAIInsight } from "@/lib/valuationEngine";

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
  alt_limit: number;
  ust_limit: number;
  tahmin: number;
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
    // Run real ML valuation model to obtain predicted range for this specific car
    const valResult = calculateValuation({
      marka: car.marka,
      seri: car.seri,
      model: car.model,
      yil: car.yil,
      kilometre: car.kilometre,
      vites_tipi: car.vites_tipi,
      yakit_tipi: car.yakit_tipi,
      kasa_tipi: car.kasa_tipi,
      konum: car.konum,
    });

    let score = 0;
    const yearNorm = Math.max(0, Math.min(1, (car.yil - minYear) / (maxYear - minYear)));
    const kmNorm = Math.max(0, Math.min(1, 1 - car.kilometre / 300000));

    if (filters.max_budget && filters.max_budget > 0) {
      // Budget-aware scoring: favors cars close to budget without exceeding
      const budgetEfficiency = valResult.tahmin / filters.max_budget;
      score = budgetEfficiency * 0.65 + yearNorm * 0.22 + kmNorm * 0.13;
    } else {
      // Criteria-based flexible scoring
      score = yearNorm * 0.45 + kmNorm * 0.35 + (1 - Math.min(1, valResult.tahmin / 4000000)) * 0.20;
    }

    // Assign dynamic tags
    let tag = "FİYAT / PERFORMANS";
    if (car.kilometre < 40000) tag = "DÜŞÜK KM AVANTAJI";
    else if (filters.max_budget && valResult.tahmin >= filters.max_budget * 0.88) tag = "BÜTÇE OPTİMİZE";
    else if (car.yil >= 2022) tag = "YENİ NESİL MODEL";
    else if (car.yakit_tipi === "Hibrit" || car.yakit_tipi === "Elektrik") tag = "ÇEVRECİ TEKNOLOJİ";

    const ai_insight = valResult.ai_insight;

    return {
      ...car,
      tahmin: valResult.tahmin,
      alt_limit: valResult.alt_limit,
      ust_limit: valResult.ust_limit,
      score,
      tag,
      ai_insight,
    };
  });

  // Sort descending by score and pick top 20
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, 20);
}
