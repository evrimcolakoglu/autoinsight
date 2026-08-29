"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Car,
  Search,
  Sparkles,
  DollarSign,
  CheckCircle2,
  Sliders,
  TrendingUp,
  Tag,
} from "lucide-react";
import confetti from "canvas-confetti";
import { formatPrice, formatKm } from "@/lib/utils";

export default function DualSimulator() {
  const [activeTab, setActiveTab] = useState<"seller" | "buyer">("seller");

  // Seller Simulator State
  const [brand, setBrand] = useState("Volkswagen");
  const [modelYear, setModelYear] = useState(2020);
  const [km, setKm] = useState(65000);
  const [fuel, setFuel] = useState("Benzin");
  const [transmission, setTransmission] = useState("Otomatik");

  // Dynamic Valuation Calculation Formula based on dataset patterns
  const basePrices: Record<string, number> = {
    Volkswagen: 1350000,
    Honda: 1250000,
    Renault: 980000,
    BMW: 2450000,
    Toyota: 1400000,
    Fiat: 780000,
  };

  const yearDiff = 2024 - modelYear;
  const kmDepreciation = (km / 10000) * 0.015;
  const yearDepreciation = yearDiff * 0.055;
  const fuelMultiplier = fuel === "Dizel" ? 1.05 : fuel === "Hibrit" ? 1.12 : 1.0;
  const transMultiplier = transmission === "Otomatik" ? 1.08 : 0.95;

  const calculatedBase =
    (basePrices[brand] || 1200000) *
    (1 - yearDepreciation) *
    (1 - kmDepreciation) *
    fuelMultiplier *
    transMultiplier;

  const estimatedPrice = Math.max(350000, Math.round(calculatedBase / 1000) * 1000);
  const lowerBound = Math.round((estimatedPrice * 0.89) / 1000) * 1000;
  const upperBound = Math.round((estimatedPrice * 1.11) / 1000) * 1000;

  // Buyer Simulator State
  const [budget, setBudget] = useState(1250000);
  const [bodyType, setBodyType] = useState("Sedan");

  const triggerConfetti = () => {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 },
      colors: ["#00ffb3", "#00c48c", "#38bdf8"],
    });
  };

  return (
    <section id="simulasyon" className="max-w-6xl mx-auto px-4 py-24">
      {/* Section Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 text-xs font-extrabold tracking-widest text-[#00ffb3] uppercase mb-3">
          <Sliders className="w-4 h-4" />
          <span>CANLI SİMÜLATÖR DENEYİMİ</span>
        </div>
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-black text-white tracking-tight">
          İki Güçlü Deneyim. Tek Platform.
        </h2>
      </div>

      {/* Experience Switcher Tabs */}
      <div className="flex justify-center mb-10">
        <div className="p-1.5 rounded-2xl bg-[#081324] border border-white/10 flex gap-2 shadow-2xl">
          <button
            onClick={() => setActiveTab("seller")}
            className={`flex items-center gap-2.5 px-6 py-3 rounded-xl font-bold text-sm transition-all ${
              activeTab === "seller"
                ? "bg-[#00ffb3] text-[#040812] shadow-[0_0_20px_rgba(0,255,179,0.35)]"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Car className="w-4 h-4" />
            <span>Piyasa Değerleme (Satıcı)</span>
          </button>
          <button
            onClick={() => setActiveTab("buyer")}
            className={`flex items-center gap-2.5 px-6 py-3 rounded-xl font-bold text-sm transition-all ${
              activeTab === "buyer"
                ? "bg-[#00ffb3] text-[#040812] shadow-[0_0_20px_rgba(0,255,179,0.35)]"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <Search className="w-4 h-4" />
            <span>Akıllı Araç Keşfi (Alıcı)</span>
          </button>
        </div>
      </div>

      {/* Tab Panels */}
      <AnimatePresence mode="wait">
        {activeTab === "seller" ? (
          <motion.div
            key="seller-panel"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
            className="grid grid-cols-1 lg:grid-cols-12 gap-8 p-8 sm:p-10 rounded-3xl bg-gradient-to-br from-[#0c1a2e]/90 via-[#07101e] to-[#040812] border border-[#00ffb3]/30 shadow-[0_30px_90px_rgba(0,0,0,0.75)]"
          >
            {/* Form Inputs (7 Cols) */}
            <div className="lg:col-span-7 flex flex-col gap-6">
              <div className="text-xl font-black text-white tracking-tight">
                Araç Parametrelerini Belirleyin
              </div>

              {/* Brand Picker */}
              <div>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                  Marka
                </label>
                <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
                  {Object.keys(basePrices).map((b) => (
                    <button
                      key={b}
                      onClick={() => setBrand(b)}
                      className={`p-2.5 rounded-xl text-xs font-bold border transition-all ${
                        brand === b
                          ? "bg-[#00ffb3]/15 border-[#00ffb3] text-[#00ffb3] shadow-[0_0_15px_rgba(0,255,179,0.2)]"
                          : "bg-[#060e1a] border-white/10 text-slate-400 hover:border-white/25"
                      }`}
                    >
                      {b}
                    </button>
                  ))}
                </div>
              </div>

              {/* Sliders Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                {/* Year Slider */}
                <div>
                  <div className="flex justify-between text-xs font-bold text-slate-400 mb-2">
                    <span>Model Yılı</span>
                    <span className="font-mono text-[#00ffb3]">{modelYear}</span>
                  </div>
                  <input
                    type="range"
                    min={2010}
                    max={2024}
                    value={modelYear}
                    onChange={(e) => setModelYear(Number(e.target.value))}
                    className="w-full accent-[#00ffb3] cursor-pointer"
                  />
                </div>

                {/* Km Slider */}
                <div>
                  <div className="flex justify-between text-xs font-bold text-slate-400 mb-2">
                    <span>Kilometre</span>
                    <span className="font-mono text-[#00ffb3]">{formatKm(km)}</span>
                  </div>
                  <input
                    type="range"
                    min={0}
                    max={250000}
                    step={5000}
                    value={km}
                    onChange={(e) => setKm(Number(e.target.value))}
                    className="w-full accent-[#00ffb3] cursor-pointer"
                  />
                </div>
              </div>

              {/* Fuel & Transmission */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                  <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                    Yakıt Tipi
                  </label>
                  <div className="flex gap-2">
                    {["Benzin", "Dizel", "Hibrit"].map((f) => (
                      <button
                        key={f}
                        onClick={() => setFuel(f)}
                        className={`flex-1 py-2 rounded-xl text-xs font-bold border transition-all ${
                          fuel === f
                            ? "bg-[#00ffb3]/15 border-[#00ffb3] text-[#00ffb3]"
                            : "bg-[#060e1a] border-white/10 text-slate-400"
                        }`}
                      >
                        {f}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                    Vites Türü
                  </label>
                  <div className="flex gap-2">
                    {["Otomatik", "Manuel"].map((t) => (
                      <button
                        key={t}
                        onClick={() => setTransmission(t)}
                        className={`flex-1 py-2 rounded-xl text-xs font-bold border transition-all ${
                          transmission === t
                            ? "bg-[#00ffb3]/15 border-[#00ffb3] text-[#00ffb3]"
                            : "bg-[#060e1a] border-white/10 text-slate-400"
                        }`}
                      >
                        {t}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Calculated Result HUD (5 Cols) */}
            <div className="lg:col-span-5 flex flex-col justify-between p-6 rounded-2xl bg-[#060f1c] border border-[#00ffb3]/30 shadow-2xl">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-extrabold uppercase tracking-wider text-[#00ffb3]">
                    Tahmini Piyasa Değeri
                  </span>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-[#00ffb3]/10 text-[#00ffb3]">
                    %94 GÜVEN ARALIĞI
                  </span>
                </div>

                <div className="font-mono text-3xl sm:text-4xl font-black text-white tracking-tight mb-2">
                  {formatPrice(estimatedPrice)}
                </div>

                <div className="text-xs text-slate-400 mb-6">
                  Piyasa Koridoru:{" "}
                  <span className="text-slate-200 font-semibold font-mono">
                    {formatPrice(lowerBound)} - {formatPrice(upperBound)}
                  </span>
                </div>

                {/* AI Rationale Box */}
                <div className="p-4 rounded-xl bg-[#091628] border border-white/5 text-xs text-slate-300 leading-relaxed">
                  <div className="flex items-center gap-1.5 font-bold text-[#00ffb3] uppercase tracking-wider mb-2 text-[11px]">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Yapay Zeka Pazar Gerekçesi</span>
                  </div>
                  {brand} {modelYear} model, {formatKm(km)} seviyesindeki araç pazar
                  ortalamasına göre dengeli bir amortisman sergilemektedir. {fuel}{" "}
                  yakıt ve {transmission.toLowerCase()} vites kombinasyonu ikinci el
                  piyasasında yüksek likidite avantajı sağlamaktadır.
                </div>
              </div>

              <button
                onClick={triggerConfetti}
                className="w-full mt-6 py-3.5 rounded-xl bg-[#00ffb3] text-[#040812] font-black text-xs uppercase tracking-wider hover:bg-[#22ffa8] transition-all hover:scale-[1.02] shadow-[0_0_25px_rgba(0,255,179,0.35)]"
              >
                Tam Raporu Oluştur →
              </button>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="buyer-panel"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
            className="p-8 sm:p-10 rounded-3xl bg-gradient-to-br from-[#0c1a2e]/90 via-[#07101e] to-[#040812] border border-[#00ffb3]/30 shadow-[0_30px_90px_rgba(0,0,0,0.75)]"
          >
            {/* Buyer Controls */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              <div>
                <div className="flex justify-between text-xs font-bold text-slate-400 mb-2">
                  <span>Maksimum Bütçe</span>
                  <span className="font-mono text-base font-extrabold text-[#00ffb3]">
                    {formatPrice(budget)}
                  </span>
                </div>
                <input
                  type="range"
                  min={400000}
                  max={3500000}
                  step={50000}
                  value={budget}
                  onChange={(e) => setBudget(Number(e.target.value))}
                  className="w-full accent-[#00ffb3] cursor-pointer"
                />
              </div>

              <div>
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 block">
                  Kasa Tipi
                </label>
                <div className="flex gap-2">
                  {["Sedan", "SUV", "Hatchback"].map((k) => (
                    <button
                      key={k}
                      onClick={() => setBodyType(k)}
                      className={`flex-1 py-2.5 rounded-xl text-xs font-bold border transition-all ${
                        bodyType === k
                          ? "bg-[#00ffb3]/15 border-[#00ffb3] text-[#00ffb3]"
                          : "bg-[#060e1a] border-white/10 text-slate-400"
                      }`}
                    >
                      {k}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Smart Matches Simulation Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {[
                {
                  title: `${bodyType === "SUV" ? "Peugeot 3008" : bodyType === "Hatchback" ? "Volkswagen Golf" : "Honda Civic"}`,
                  year: 2021,
                  km: 48000,
                  price: Math.round((budget * 0.94) / 10000) * 10000,
                  tag: "BÜTÇE OPTİMİZE",
                  badgeColor: "bg-[#00ffb3]/15 text-[#00ffb3] border-[#00ffb3]/30",
                },
                {
                  title: `${bodyType === "SUV" ? "Nissan Qashqai" : bodyType === "Hatchback" ? "Renault Clio" : "Toyota Corolla"}`,
                  year: 2022,
                  km: 32000,
                  price: Math.round((budget * 0.88) / 10000) * 10000,
                  tag: "DÜŞÜK KM AVANTAJI",
                  badgeColor: "bg-[#38bdf8]/15 text-[#38bdf8] border-[#38bdf8]/30",
                },
                {
                  title: `${bodyType === "SUV" ? "Hyundai Tucson" : bodyType === "Hatchback" ? "Seat Leon" : "Skoda Octavia"}`,
                  year: 2020,
                  km: 74000,
                  price: Math.round((budget * 0.82) / 10000) * 10000,
                  tag: "FİYAT/PERFORMANS",
                  badgeColor: "bg-[#a855f7]/15 text-[#a855f7] border-[#a855f7]/30",
                },
              ].map((car, i) => (
                <div
                  key={i}
                  className="p-5 rounded-2xl bg-[#060f1c] border border-white/10 hover:border-[#00ffb3]/40 transition-all flex flex-col justify-between shadow-lg"
                >
                  <div>
                    <span
                      className={`text-[10px] font-extrabold uppercase tracking-wider px-2.5 py-1 rounded-full border ${car.badgeColor} inline-block mb-3`}
                    >
                      {car.tag}
                    </span>
                    <div className="font-extrabold text-base text-white mb-1">
                      {car.title}
                    </div>
                    <div className="text-xs text-slate-400 font-medium">
                      {car.year} &middot; {formatKm(car.km)}
                    </div>
                  </div>
                  <div className="font-mono text-lg font-black text-[#00ffb3] mt-4">
                    {formatPrice(car.price)}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
