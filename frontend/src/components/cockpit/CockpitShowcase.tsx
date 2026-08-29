"use client";

import { motion } from "framer-motion";
import Image from "next/image";
import { Compass, Database, Cpu, TrendingUp } from "lucide-react";

export default function CockpitShowcase() {
  return (
    <section className="max-w-6xl mx-auto px-4 py-20">
      <div className="relative rounded-3xl bg-gradient-to-br from-[#0c1a2e]/80 via-[#060e1c]/90 to-[#040812] border border-white/10 p-8 sm:p-12 lg:p-16 shadow-[0_30px_90px_rgba(0,0,0,0.7)] overflow-hidden">
        {/* Ambient Top Glow */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-[#00ffb3]/10 rounded-full blur-[100px] pointer-events-none" />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
          {/* Left: Market Intelligence Lab Visual Stage */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="lg:col-span-7 relative aspect-[16/10] rounded-2xl overflow-hidden border border-[#00ffb3]/30 shadow-[0_20px_50px_rgba(0,0,0,0.8)] group"
          >
            <Image
              src="/assets/market_intelligence_hub.jpg"
              alt="AutoInsight Otomotiv Pazar İstihbarat Merkezi"
              fill
              className="object-cover transition-transform duration-1000 group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-[#040812] via-transparent to-transparent opacity-60" />
          </motion.div>

          {/* Right: Telemetry Details */}
          <motion.div
            initial={{ opacity: 0, x: 25 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="lg:col-span-5 flex flex-col gap-6"
          >
            <div className="inline-flex items-center gap-2 text-xs font-extrabold tracking-widest text-[#00ffb3] uppercase">
              <Compass className="w-4 h-4" />
              <span>PAZAR İSTİHBARAT MERKEZİ</span>
            </div>

            <h3 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold text-white tracking-tight leading-snug">
              Canlı Pazar Hacmi &amp; İkinci El Fiyat Dağılımları
            </h3>

            <p className="text-sm sm:text-base text-slate-400 leading-relaxed font-normal">
              53.514 gerçek ilan verisiyle beslenen yapay zeka analiz merkezimiz,
              81 ildeki bölgesel fiyat dalgalanmalarını ve segment fırsatlarını
              anlık olarak haritalandırır.
            </p>

            {/* Live Regional & Engine Status Rows */}
            <div className="flex flex-col gap-3 mt-2">
              <div className="flex items-center justify-between p-4 rounded-xl bg-[#091526]/80 border border-white/5 shadow-inner">
                <div className="flex items-center gap-3 text-xs sm:text-sm font-semibold text-slate-300">
                  <div className="w-2 h-2 rounded-full bg-[#00ffb3] animate-pulse" />
                  <span>İstanbul İkinci El Pazar Hacmi</span>
                </div>
                <span className="font-mono text-xs sm:text-sm font-bold text-[#00ffb3]">
                  18.420 İlan
                </span>
              </div>

              <div className="flex items-center justify-between p-4 rounded-xl bg-[#091526]/80 border border-white/5 shadow-inner">
                <div className="flex items-center gap-3 text-xs sm:text-sm font-semibold text-slate-300">
                  <div className="w-2 h-2 rounded-full bg-[#00ffb3] animate-pulse" />
                  <span>Ankara &amp; İzmir Pazar Dağılımı</span>
                </div>
                <span className="font-mono text-xs sm:text-sm font-bold text-[#00ffb3]">
                  14.150 İlan
                </span>
              </div>

              <div className="flex items-center justify-between p-4 rounded-xl bg-[#091526]/80 border border-white/5 shadow-inner">
                <div className="flex items-center gap-3 text-xs sm:text-sm font-semibold text-slate-300">
                  <Cpu className="w-4 h-4 text-[#00ffb3]" />
                  <span>Çıkarım Modeli &amp; RAG</span>
                </div>
                <span className="font-mono text-xs sm:text-sm font-bold text-[#00ffb3]">
                  Lokal / Çevrimdışı
                </span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
