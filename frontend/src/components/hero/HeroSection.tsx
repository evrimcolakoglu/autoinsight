"use client";

import { useRef } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { Sparkles, Gauge, Activity, ShieldCheck, Cpu } from "lucide-react";
import Image from "next/image";

export default function HeroSection() {
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"],
  });

  // Scroll pinning & expansion transforms
  const scale = useTransform(scrollYProgress, [0, 0.6], [0.88, 1]);
  const borderRadius = useTransform(scrollYProgress, [0, 0.6], ["32px", "16px"]);
  const opacity = useTransform(scrollYProgress, [0, 0.15, 0.85, 1], [0.95, 1, 1, 0.8]);

  return (
    <section ref={containerRef} className="relative min-h-[170vh] w-full pt-32 pb-20">
      {/* Sticky Pinned Hero Content */}
      <div className="sticky top-20 flex flex-col items-center justify-center max-w-6xl mx-auto px-4">
        {/* Category Pill */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#00c48c]/10 border border-[#00ffb3]/30 text-[#00ffb3] text-xs font-extrabold uppercase tracking-widest mb-6 shadow-[0_0_20px_rgba(0,196,140,0.15)]"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>YAPAY ZEKA DESTEKLİ ARAÇ DEĞERLEME PLATFORMU</span>
        </motion.div>

        {/* Super Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
          className="text-center font-black text-4xl sm:text-6xl md:text-7xl lg:text-8xl tracking-tight leading-[1.06] mb-6 max-w-5xl"
        >
          <span className="text-titanium">Otomotiv Zekâsının.</span>
          <br />
          <span className="text-emerald-glow drop-shadow-[0_0_35px_rgba(0,255,179,0.35)]">
            En İleri Seviyesi.
          </span>
        </motion.h1>

        {/* Subtitle Description */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-center text-slate-400 text-base sm:text-lg md:text-xl max-w-3xl leading-relaxed mb-10 font-normal"
        >
          53.000&apos;den fazla gerçek pazar verisi, anlık varyans analizleri ve
          makine öğrenmesi boru hattıyla aracınızın gerçek piyasa değerini ve en
          avantajlı fırsatları saniyeler içinde keşfedin.
        </motion.p>

        {/* Pinned Scrollytelling Stage: Expanding Valuation Lab Canvas */}
        <motion.div
          style={{ scale, borderRadius, opacity }}
          className="relative w-full aspect-[16/9] max-h-[520px] overflow-hidden border border-[#00ffb3]/30 shadow-[0_35px_100px_rgba(0,0,0,0.8),0_0_60px_rgba(0,196,140,0.15)] bg-[#040914] group"
        >
          {/* Laser Scanner Beam */}
          <div className="laser-scanner" />

          {/* Targeted Valuation Studio Visual */}
          <Image
            src="/assets/valuation_lab_hero.jpg"
            alt="AutoInsight Yapay Zeka Araç Değerleme Laboratuvarı"
            fill
            priority
            className="object-cover transition-transform duration-1000 group-hover:scale-105 filter brightness-95 contrast-105"
          />

          {/* Cinematic Overlay & Live Telemetry HUD */}
          <div className="absolute inset-0 bg-gradient-to-t from-[#040914] via-[#040914]/40 to-transparent flex flex-col justify-end p-6 sm:p-10 pointer-events-none">
            <div className="text-xl sm:text-2xl font-black text-white tracking-tight">
              Yapay Zeka Destekli Hassas Değerleme Laboratuvarı
            </div>
            <p className="text-xs sm:text-sm text-slate-300 max-w-xl mt-1 mb-4">
              Gelişmiş Random Forest algoritmamız; kilometre amortismanı, pazar talebi ve
              emsal fiyat varyasyonlarını anlık olarak tarar.
            </p>

            {/* Live Telemetry Chips */}
            <div className="flex flex-wrap gap-3">
              <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#060f1c]/85 backdrop-blur-md border border-[#00ffb3]/40 shadow-lg">
                <Cpu className="w-4 h-4 text-[#00ffb3]" />
                <span className="text-[11px] font-bold text-slate-400 uppercase">Hesaplama:</span>
                <span className="font-mono text-sm font-extrabold text-[#00ffb3]">&lt;15ms</span>
              </div>
              <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#060f1c]/85 backdrop-blur-md border border-[#00ffb3]/40 shadow-lg">
                <ShieldCheck className="w-4 h-4 text-[#00ffb3]" />
                <span className="text-[11px] font-bold text-slate-400 uppercase">Model Doğruluğu:</span>
                <span className="font-mono text-sm font-extrabold text-[#00ffb3]">%94.0 R²</span>
              </div>
              <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#060f1c]/85 backdrop-blur-md border border-[#00ffb3]/40 shadow-lg">
                <Gauge className="w-4 h-4 text-[#00ffb3]" />
                <span className="text-[11px] font-bold text-slate-400 uppercase">Hata Payı:</span>
                <span className="font-mono text-sm font-extrabold text-[#00ffb3]">%11.09 MAPE</span>
              </div>
              <div className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#060f1c]/85 backdrop-blur-md border border-[#00ffb3]/40 shadow-lg">
                <Activity className="w-4 h-4 text-[#00ffb3] animate-pulse" />
                <span className="font-mono text-xs font-bold text-[#00ffb3]">AKTİF PİYASA RADARI</span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
