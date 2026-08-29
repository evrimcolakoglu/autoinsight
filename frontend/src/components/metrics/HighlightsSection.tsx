"use client";

import { motion } from "framer-motion";
import { TrendingUp, Database, Zap, Car } from "lucide-react";

interface MetricCardProps {
  val: string;
  label: string;
  sub: string;
  icon: React.ReactNode;
  delay?: number;
}

function MetricCard({ val, label, sub, icon, delay = 0 }: MetricCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.7, delay, ease: [0.16, 1, 0.3, 1] }}
      className="relative flex flex-col items-center text-center p-8 rounded-3xl bg-gradient-to-b from-[#091424] to-[#060d1a] border border-white/10 hover:border-[#00ffb3]/40 transition-all duration-300 hover:-translate-y-1.5 shadow-2xl group"
    >
      <div className="w-12 h-12 rounded-2xl bg-[#00c48c]/10 border border-[#00ffb3]/30 flex items-center justify-center text-[#00ffb3] mb-5 shadow-[0_0_20px_rgba(0,196,140,0.15)] group-hover:scale-110 transition-transform">
        {icon}
      </div>
      <div className="font-mono font-black text-4xl sm:text-5xl lg:text-6xl text-white tracking-tight mb-2 group-hover:text-[#00ffb3] transition-colors drop-shadow-[0_0_25px_rgba(0,255,179,0.3)]">
        {val}
      </div>
      <div className="text-xs sm:text-sm font-bold uppercase tracking-wider text-slate-300 mb-1">
        {label}
      </div>
      <div className="text-xs text-slate-500 font-medium">{sub}</div>
    </motion.div>
  );
}

export default function HighlightsSection() {
  return (
    <section id="telemetri" className="max-w-6xl mx-auto px-4 py-24">
      {/* Section Header */}
      <div className="text-center mb-14">
        <div className="inline-flex items-center gap-2 text-xs font-extrabold tracking-widest text-[#00ffb3] uppercase mb-3">
          <span>CANLI TELEMETRİ GÖSTERGELERİ</span>
        </div>
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-black text-white tracking-tight">
          Piyasa Verileriyle Güçlendirilmiş Doğruluk
        </h2>
      </div>

      {/* Metric 4-Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          val="%94.0"
          label="R² Pazar Doğruluğu"
          sub="Yüksek Varyans Açıklama Gücü"
          icon={<TrendingUp className="w-6 h-6" />}
          delay={0.1}
        />
        <MetricCard
          val="53.514"
          label="İncelenen İlan"
          sub="Türkiye Geneli Canlı Pazar Verisi"
          icon={<Database className="w-6 h-6" />}
          delay={0.2}
        />
        <MetricCard
          val="<15ms"
          label="Hesaplama Hızı"
          sub="Anlık Yerel Çıkarım Süresi"
          icon={<Zap className="w-6 h-6" />}
          delay={0.3}
        />
        <MetricCard
          val="46 Marka"
          label="1.100+ Model"
          sub="Geniş Kapsamlı Segment Havuzu"
          icon={<Car className="w-6 h-6" />}
          delay={0.4}
        />
      </div>
    </section>
  );
}
