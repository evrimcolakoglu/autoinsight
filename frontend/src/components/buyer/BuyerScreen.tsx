"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  ArrowLeft,
  Filter,
  Sparkles,
  SlidersHorizontal,
  Car,
  MapPin,
  Calendar,
  Gauge,
  Fuel,
  CheckCircle2,
} from "lucide-react";
import metadata from "@/data/brands_hierarchy.json";
import { recommendVehicles, VehicleMatch } from "@/lib/recommenderEngine";
import { formatPrice, formatKm } from "@/lib/utils";

interface BuyerScreenProps {
  onBack: () => void;
}

export default function BuyerScreen({ onBack }: BuyerScreenProps) {
  const brands = ["Tümü", ...(metadata.brands as string[])];
  const cities = ["Tümü", ...(metadata.cities as string[])];
  const fuels = ["Tümü", ...(metadata.fuels as string[])];
  const gears = ["Tümü", ...(metadata.gears as string[])];
  const bodies = ["Tümü", ...(metadata.bodies as string[])];

  // Search Mode
  const [searchMode, setSearchMode] = useState<"budget" | "flexible">("budget");

  // Filters State
  const [budget, setBudget] = useState<number>(1400000);
  const [minYear, setMinYear] = useState<number>(2016);
  const [maxKm, setMaxKm] = useState<number>(150000);
  const [preferredBrand, setPreferredBrand] = useState<string>("Tümü");
  const [fuel, setFuel] = useState<string>("Tümü");
  const [gear, setGear] = useState<string>("Tümü");
  const [body, setBody] = useState<string>("Tümü");
  const [city, setCity] = useState<string>("Tümü");

  // Results State
  const [results, setResults] = useState<VehicleMatch[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    setTimeout(() => {
      const matches = recommendVehicles({
        max_budget: searchMode === "budget" ? budget : undefined,
        min_year: minYear,
        max_km: maxKm,
        fuel_type: fuel,
        gear_type: gear,
        body_type: body,
        preferred_brand: preferredBrand,
        city: city,
      });

      setResults(matches);
      setLoading(false);
    }, 300);
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
          <span>Akıllı Öneri &middot; İlk 20 Eşleşme</span>
        </div>
      </div>

      {/* Mode Switcher */}
      <div className="flex justify-center mb-8">
        <div className="p-1.5 rounded-2xl bg-[#081324] border border-white/10 flex gap-2 shadow-2xl">
          <button
            onClick={() => setSearchMode("budget")}
            className={`flex items-center gap-2 px-6 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${
              searchMode === "budget"
                ? "bg-[#00ffb3] text-[#040812] shadow-[0_0_20px_rgba(0,255,179,0.35)]"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <span>Bütçeli Akıllı Arama</span>
          </button>
          <button
            onClick={() => setSearchMode("flexible")}
            className={`flex items-center gap-2 px-6 py-2.5 rounded-xl font-bold text-xs uppercase tracking-wider transition-all ${
              searchMode === "flexible"
                ? "bg-[#00ffb3] text-[#040812] shadow-[0_0_20px_rgba(0,255,179,0.35)]"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <span>Bütçesiz Esnek Arama</span>
          </button>
        </div>
      </div>

      {/* Filter Form Card */}
      <form
        onSubmit={handleSearch}
        className="p-6 sm:p-8 rounded-3xl bg-gradient-to-br from-[#0c182c]/85 via-[#07101e]/90 to-[#040812] border border-white/10 shadow-2xl mb-12 flex flex-col gap-6"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#00c48c]/15 border border-[#00ffb3]/40 flex items-center justify-center text-[#00ffb3]">
            <Filter className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
              {searchMode === "budget" ? "Bütçeli Akıllı Keşif Kriterleri" : "Esnek Arama Kriterleri"}
            </h2>
            <p className="text-xs text-slate-400">
              Kriterlerinizi belirleyin; algoritma en avantajlı fırsat ilanlarını saniyeler içinde puanlasın.
            </p>
          </div>
        </div>

        {/* Sliders Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {searchMode === "budget" && (
            <div>
              <div className="flex justify-between text-xs font-bold text-slate-400 mb-2">
                <span>Maksimum Bütçe</span>
                <span className="font-mono text-[#00ffb3]">{formatPrice(budget)}</span>
              </div>
              <input
                type="range"
                min={300000}
                max={4500000}
                step={50000}
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value))}
                className="w-full accent-[#00ffb3] cursor-pointer"
              />
            </div>
          )}

          <div>
            <div className="flex justify-between text-xs font-bold text-slate-400 mb-2">
              <span>Minimum Model Yılı</span>
              <span className="font-mono text-[#00ffb3]">{minYear}</span>
            </div>
            <input
              type="range"
              min={2000}
              max={2024}
              value={minYear}
              onChange={(e) => setMinYear(Number(e.target.value))}
              className="w-full accent-[#00ffb3] cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs font-bold text-slate-400 mb-2">
              <span>Maksimum Kilometre</span>
              <span className="font-mono text-[#00ffb3]">{formatKm(maxKm)}</span>
            </div>
            <input
              type="range"
              min={20000}
              max={350000}
              step={10000}
              value={maxKm}
              onChange={(e) => setMaxKm(Number(e.target.value))}
              className="w-full accent-[#00ffb3] cursor-pointer"
            />
          </div>
        </div>

        {/* Dropdowns Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <div>
            <label className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 block">
              Tercih Edilen Marka
            </label>
            <select
              value={preferredBrand}
              onChange={(e) => setPreferredBrand(e.target.value)}
              className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-3 py-2.5 text-xs text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
            >
              {brands.map((b) => (
                <option key={b} value={b} className="bg-[#081324] text-white">
                  {b}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 block">
              Yakıt Tipi
            </label>
            <select
              value={fuel}
              onChange={(e) => setFuel(e.target.value)}
              className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-3 py-2.5 text-xs text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
            >
              {fuels.map((f) => (
                <option key={f} value={f} className="bg-[#081324] text-white">
                  {f}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 block">
              Vites Türü
            </label>
            <select
              value={gear}
              onChange={(e) => setGear(e.target.value)}
              className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-3 py-2.5 text-xs text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
            >
              {gears.map((g) => (
                <option key={g} value={g} className="bg-[#081324] text-white">
                  {g}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 block">
              Kasa Tipi
            </label>
            <select
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-3 py-2.5 text-xs text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
            >
              {bodies.map((k) => (
                <option key={k} value={k} className="bg-[#081324] text-white">
                  {k}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1.5 block">
              Şehir
            </label>
            <select
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="w-full bg-[#060f1c] border border-white/15 rounded-xl px-3 py-2.5 text-xs text-white font-medium focus:border-[#00ffb3] focus:outline-none transition-colors cursor-pointer"
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
          disabled={loading}
          className="w-full py-4 rounded-xl bg-[#00ffb3] text-[#040812] font-black text-sm uppercase tracking-wider hover:bg-[#22ffa8] transition-all hover:scale-[1.01] shadow-[0_0_25px_rgba(0,255,179,0.35)] disabled:opacity-50"
        >
          {loading ? "Fırsat Araçlar Taranıyor..." : "En Uygun Araçları Keşfet (İlk 20 Eşleşme) →"}
        </button>
      </form>

      {/* Results Section */}
      {results && (
        <div className="flex flex-col gap-6">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-extrabold text-white">
              Eşleşen Fırsat Araçlar ({results.length} İlan Bulundu)
            </h3>
          </div>

          {results.length === 0 ? (
            <div className="p-12 text-center rounded-3xl bg-[#081222] border border-white/10 text-slate-400">
              <div className="text-lg font-bold text-white mb-2">Uygun Araç Bulunamadı</div>
              <p className="text-xs">Lütfen filtre kriterlerinizi genişleterek tekrar deneyin.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {results.map((car, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: idx * 0.05 }}
                  className="rounded-3xl bg-gradient-to-br from-[#0c182c] to-[#060e1c] border border-white/10 hover:border-[#00ffb3]/45 transition-all shadow-xl overflow-hidden flex flex-col justify-between"
                >
                  {/* Card Header & Specs */}
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-[10px] font-extrabold px-3 py-1 rounded-full bg-[#00ffb3]/15 text-[#00ffb3] border border-[#00ffb3]/30 uppercase tracking-wider">
                        #{idx + 1} &middot; {car.tag}
                      </span>
                      <div className="flex items-center gap-1.5 text-xs text-slate-400 font-semibold">
                        <MapPin className="w-3.5 h-3.5 text-[#00ffb3]" />
                        <span>{car.konum}</span>
                      </div>
                    </div>

                    <h4 className="text-lg font-black text-white mb-1">
                      {car.marka} {car.seri} {car.model}
                    </h4>

                    <div className="grid grid-cols-3 gap-2 my-4 p-3 rounded-xl bg-[#050b14] text-xs">
                      <div>
                        <span className="text-slate-500 block text-[10px] uppercase">Yıl</span>
                        <span className="text-slate-200 font-bold">{car.yil}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px] uppercase">Kilometre</span>
                        <span className="text-slate-200 font-bold">{formatKm(car.kilometre)}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[10px] uppercase">Vites / Yakıt</span>
                        <span className="text-slate-200 font-bold">{car.vites_tipi} &middot; {car.yakit_tipi}</span>
                      </div>
                    </div>

                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 pt-2">
                      <span className="text-xs font-semibold text-slate-400">Tahmini Değer Aralığı:</span>
                      <span className="font-mono text-lg sm:text-xl font-black text-[#00ffb3] drop-shadow-[0_0_20px_rgba(0,255,179,0.3)]">
                        {formatPrice(car.alt_limit)} &mdash; {formatPrice(car.ust_limit)}
                      </span>
                    </div>
                  </div>

                  {/* Individual Distinct AI Rationale Box */}
                  <div className="p-4 bg-[#040812] border-t border-white/5 text-xs text-slate-300 leading-relaxed">
                    <div className="flex items-center gap-1.5 font-bold text-[#00ffb3] uppercase tracking-wider mb-1.5 text-[11px]">
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Yapay Zeka Pazar Analizi &amp; Gerekçesi</span>
                    </div>
                    <p>{car.ai_insight}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
