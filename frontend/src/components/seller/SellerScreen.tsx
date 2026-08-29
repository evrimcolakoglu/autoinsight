"use client";

import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Car,
  Sparkles,
  ArrowLeft,
  DollarSign,
  TrendingUp,
  ShieldCheck,
  Zap,
  MapPin,
  CheckCircle2,
  Percent,
} from "lucide-react";
import confetti from "canvas-confetti";
import metadata from "@/data/brands_hierarchy.json";
import { calculateValuation, ValuationResult } from "@/lib/valuationEngine";
import { formatPrice, formatKm } from "@/lib/utils";

interface SellerScreenProps {
  onBack: () => void;
}

export default function SellerScreen({ onBack }: SellerScreenProps) {
  const brands = metadata.brands as string[];
  const hierarchy = metadata.hierarchy as Record<string, Record<string, string[]>>;
  const cities = metadata.cities as string[];
  const fuels = metadata.fuels as string[];
  const gears = metadata.gears as string[];
  const bodies = metadata.bodies as string[];

  // Form State
  const [selectedBrand, setSelectedBrand] = useState<string>("Volkswagen");
  const [selectedSeries, setSelectedSeries] = useState<string>("");
  const [selectedModel, setSelectedModel] = useState<string>("");
  const [year, setYear] = useState<number>(2020);
  const [km, setKm] = useState<number>(65000);
  const [fuel, setFuel] = useState<string>("Benzin");
  const [gear, setGear] = useState<string>("Otomatik");
  const [body, setBody] = useState<string>("Sedan");
  const [city, setCity] = useState<string>("İstanbul");

  const [result, setResult] = useState<ValuationResult | null>(null);
  const [calculating, setCalculating] = useState<boolean>(false);

  // Cascaded series based on selected brand
  const availableSeries = useMemo(() => {
    if (selectedBrand && hierarchy[selectedBrand]) {
      return Object.keys(hierarchy[selectedBrand]);
    }
    return [];
  }, [selectedBrand, hierarchy]);

  // Cascaded models based on selected series
  const availableModels = useMemo(() => {
    if (selectedBrand && selectedSeries && hierarchy[selectedBrand]?.[selectedSeries]) {
      return hierarchy[selectedBrand][selectedSeries];
    }
    return [];
  }, [selectedBrand, selectedSeries, hierarchy]);

  const handleBrandChange = (brand: string) => {
    setSelectedBrand(brand);
    setSelectedSeries("");
    setSelectedModel("");
  };

  const handleSeriesChange = (series: string) => {
    setSelectedSeries(series);
    setSelectedModel("");
  };

  const handleCalculate = (e: React.FormEvent) => {
    e.preventDefault();
    setCalculating(true);

    setTimeout(() => {
      const res = calculateValuation({
        marka: selectedBrand,
        seri: selectedSeries || "Genel",
        model: selectedModel || "Standart",
        yil: year,
        kilometre: km,
        vites_tipi: gear,
        yakit_tipi: fuel,
        kasa_tipi: body,
        konum: city,
      });

      setResult(res);
      setCalculating(false);

      confetti({
        particleCount: 75,
        spread: 60,
        origin: { y: 0.65 },
        colors: ["#00ffb3", "#00c48c", "#38bdf8"],
      });
    }, 350);
  };

  return (
    <div className="min-h-screen pt-28 pb-20 px-4 max-w-6xl mx-auto">
      {/* Top Header & Back Button */}
      <div className="flex items-center justify-between mb-8 pb-4 border-b border-white/10">
        <button
          onClick={onBack}
          className="flex items-center gap-2.5 px-4 py-2 rounded-xl bg-white/5 hover:bg-[#00ffb3]/15 text-slate-300 hover:text-[#00ffb3] border border-white/10 hover:border-[#00ffb3]/40 transition-all font-semibold text-xs uppercase tracking-wider"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Ana Sayfaya Dön</span>
        </button>

        <div className="flex items-center gap-2 text-xs font-bold text-[#00ffb3] px-3 py-1 rounded-full bg-[#00ffb3]/10 border border-[#00ffb3]/30 uppercase">
          <Sparkles className="w-3.5 h-3.5" />
          <span>46 Marka &middot; 81 İl Analizi</span>
        </div>
      </div>

      {/* Main Grid: Form (Left) & Results HUD (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Form Container (7 Cols) */}
        <div className="lg:col-span-7 bg-gradient-to-br from-[#0c182c]/85 via-[#07101e]/90 to-[#040812] border border-white/10 rounded-3xl p-6 sm:p-8 shadow-2xl">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-[#00c48c]/15 border border-[#00ffb3]/40 flex items-center justify-center text-[#00ffb3]">
              <Car className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-2xl font-black text-white tracking-tight">
                Piyasa Değerleme Parametreleri
              </h2>
              <p className="text-xs text-slate-400">
                Aracınızın tam donanım bilgilerini girerek anlık yapay zeka pazar raporu alın.
              </p>
            </div>
          </div>

          <form onSubmit={handleCalculate} className="flex flex-col gap-5">
            {/* Marka (46 Brands Dropdown) */}
            <div>
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                Marka (Tüm 46 Marka)
              </label>
              <select
                value={selectedBrand}
                onChange={(e) => handleBrandChange(e.target.value)}
                className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-4 py-3 text-sm text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
              >
                {brands.map((b) => (
                  <option key={b} value={b} className="bg-[#081324] text-white">
                    {b}
                  </option>
                ))}
              </select>
            </div>

            {/* Cascaded Seri & Model */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                  Seri
                </label>
                <select
                  value={selectedSeries}
                  onChange={(e) => handleSeriesChange(e.target.value)}
                  className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-4 py-3 text-sm text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
                >
                  <option value="">(Tüm Seriler)</option>
                  {availableSeries.map((s) => (
                    <option key={s} value={s} className="bg-[#081324] text-white">
                      {s}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                  Model
                </label>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  disabled={availableModels.length === 0}
                  className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-4 py-3 text-sm text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer disabled:opacity-50"
                >
                  <option value="">(Tüm Modeller)</option>
                  {availableModels.map((m) => (
                    <option key={m} value={m} className="bg-[#081324] text-white">
                      {m}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Model Yılı & Kilometre Inputs */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <div className="flex justify-between text-xs font-bold text-slate-400 mb-2">
                  <span>Model Yılı</span>
                  <span className="font-mono text-[#00ffb3]">{year}</span>
                </div>
                <input
                  type="range"
                  min={1990}
                  max={2024}
                  value={year}
                  onChange={(e) => setYear(Number(e.target.value))}
                  className="w-full accent-[#00ffb3] cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between text-xs font-bold text-slate-400 mb-2">
                  <span>Kilometre</span>
                  <span className="font-mono text-[#00ffb3]">{formatKm(km)}</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={450000}
                  step={5000}
                  value={km}
                  onChange={(e) => setKm(Number(e.target.value))}
                  className="w-full accent-[#00ffb3] cursor-pointer"
                />
              </div>
            </div>

            {/* Vites & Yakıt */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                  Vites Türü
                </label>
                <select
                  value={gear}
                  onChange={(e) => setGear(e.target.value)}
                  className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-4 py-3 text-sm text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
                >
                  {gears.map((g) => (
                    <option key={g} value={g} className="bg-[#081324] text-white">
                      {g}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                  Yakıt Tipi
                </label>
                <select
                  value={fuel}
                  onChange={(e) => setFuel(e.target.value)}
                  className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-4 py-3 text-sm text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
                >
                  {fuels.map((f) => (
                    <option key={f} value={f} className="bg-[#081324] text-white">
                      {f}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Kasa Tipi & Şehir */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                  Kasa Tipi
                </label>
                <select
                  value={body}
                  onChange={(e) => setBody(e.target.value)}
                  className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-4 py-3 text-sm text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
                >
                  {bodies.map((k) => (
                    <option key={k} value={k} className="bg-[#081324] text-white">
                      {k}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                  Şehir (81 İl)
                </label>
                <select
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-4 py-3 text-sm text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
                >
                  {cities.map((c) => (
                    <option key={c} value={c} className="bg-[#081324] text-white">
                      {c}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={calculating}
              className="w-full mt-3 py-4 rounded-xl bg-[#00ffb3] text-[#040812] font-black text-sm uppercase tracking-wider hover:bg-[#22ffa8] transition-all hover:scale-[1.01] shadow-[0_0_25px_rgba(0,255,179,0.35)] disabled:opacity-50"
            >
              {calculating ? "Hesaplanıyor..." : "Piyasa Değerini Hesapla →"}
            </button>
          </form>
        </div>

        {/* Results HUD Container (5 Cols) */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-br from-[#0c1a2e] to-[#050c18] border border-[#00ffb3]/35 shadow-[0_25px_80px_rgba(0,0,0,0.7)] flex flex-col justify-between min-h-[480px]">
            {result ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4 }}
                className="flex flex-col gap-5"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-extrabold uppercase tracking-wider text-[#00ffb3]">
                    Tahmini Piyasa Değer Aralığı
                  </span>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-[#00ffb3]/15 text-[#00ffb3] border border-[#00ffb3]/30">
                    %94 GÜVEN ARALIĞI
                  </span>
                </div>

                {/* Primary Price Range Display */}
                <div>
                  <div className="font-mono text-3xl sm:text-4xl font-black text-[#00ffb3] tracking-tight drop-shadow-[0_0_30px_rgba(0,255,179,0.35)] leading-tight mb-2">
                    {formatPrice(result.alt_limit)} &mdash; {formatPrice(result.ust_limit)}
                  </div>
                  <div className="text-xs text-slate-400 font-medium flex items-center gap-2">
                    <span>Model Medyan Değeri:</span>
                    <span className="text-white font-bold font-mono">{formatPrice(result.tahmin)}</span>
                    <span>&middot;</span>
                    <span className="text-[#00ffb3] font-semibold">%11.09 MAPE Güven Koridoru</span>
                  </div>
                </div>

                {/* Percentile Position */}
                <div className="p-4 rounded-2xl bg-[#060f1c] border border-white/10">
                  <div className="flex justify-between text-xs font-semibold text-slate-300 mb-2">
                    <span>Emsal Pazar Dağılım Konumu</span>
                    <span className="font-mono text-[#00ffb3] font-bold">%{result.percentile}</span>
                  </div>
                  <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-[#00c48c] to-[#00ffb3] rounded-full transition-all duration-700"
                      style={{ width: `${result.percentile}%` }}
                    />
                  </div>
                </div>

                {/* Local Diverse AI Rationale */}
                <div className="p-5 rounded-2xl bg-[#09182d] border border-[#00ffb3]/30 text-xs sm:text-sm text-slate-300 leading-relaxed shadow-inner">
                  <div className="flex items-center gap-2 font-bold text-[#00ffb3] uppercase tracking-wider mb-2 text-xs">
                    <Sparkles className="w-4 h-4" />
                    <span>Yapay Zeka Pazar Analizi &amp; Gerekçesi</span>
                  </div>
                  <p>{result.ai_insight}</p>
                </div>
              </motion.div>
            ) : (
              <div className="flex flex-col items-center justify-center text-center my-auto py-12 text-slate-400">
                <div className="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-slate-500 mb-4">
                  <Car className="w-8 h-8" />
                </div>
                <div className="text-lg font-bold text-white mb-1">Değerleme Bekleniyor</div>
                <p className="text-xs text-slate-400 max-w-xs">
                  Soldaki formdan araç özelliklerini seçip &quot;Piyasa Değerini Hesapla&quot; butonuna basın.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
