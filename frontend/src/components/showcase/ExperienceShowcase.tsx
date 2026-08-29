"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Car, Search, Sparkles, ArrowRight, ShieldCheck, Zap, Database, Sliders } from "lucide-react";

export default function ExperienceShowcase() {
  return (
    <section id="deneyim" className="max-w-6xl mx-auto px-4 py-24">
      {/* Header */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 text-xs font-extrabold tracking-widest text-[#00ffb3] uppercase mb-3">
          <Sliders className="w-4 h-4" />
          <span>İKİ GÜÇLÜ MODÜL &middot; TEK PLATFORM</span>
        </div>
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-black text-white tracking-tight">
          İhtiyacınıza Uygun Deneyimi Seçin
        </h2>
        <p className="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto mt-3">
          Tüm 46 marka, 81 il ve 53.514 gerçek pazar verisiyle desteklenen tam kapsamlı değerleme ve akıllı araç keşfi modüllerine hemen geçiş yapın.
        </p>
      </div>

      {/* 2 Massive Apple Pro Showcase Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Card 1: Piyasa Değerleme */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="relative rounded-3xl bg-gradient-to-br from-[#0e1d33]/90 via-[#081220] to-[#040812] border border-[#00ffb3]/30 p-8 sm:p-10 shadow-[0_25px_70px_rgba(0,0,0,0.7)] flex flex-col justify-between group hover:border-[#00ffb3]/60 transition-all hover:-translate-y-2"
        >
          <div>
            <div className="flex items-center justify-between mb-6">
              <div className="w-14 h-14 rounded-2xl bg-[#00c48c]/15 border border-[#00ffb3]/40 flex items-center justify-center text-[#00ffb3] shadow-[0_0_25px_rgba(0,196,140,0.2)] group-hover:scale-110 transition-transform">
                <Car className="w-7 h-7" />
              </div>
              <span className="text-xs font-black uppercase tracking-wider px-3.5 py-1.5 rounded-full bg-[#00ffb3]/15 text-[#00ffb3] border border-[#00ffb3]/30">
                Satıcı Modülü
              </span>
            </div>

            <h3 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-3">
              Piyasa Değerleme
            </h3>

            <p className="text-sm text-slate-300 leading-relaxed font-normal mb-8">
              46 marka, seri, model, yıl, kilometre ve donanım parametrelerini girin; yapay zeka modelimiz aracınızın piyasa değer koridorunu, %11.09 MAPE güven aralığını ve emsal pazar konumunu anında hesaplasın.
            </p>

            <div className="grid grid-cols-2 gap-3 mb-8 text-xs font-bold text-slate-300">
              <div className="p-3 rounded-xl bg-[#060e1a] border border-white/5 flex items-center gap-2">
                <Zap className="w-4 h-4 text-[#00ffb3]" />
                <span>Anlık Değerleme</span>
              </div>
              <div className="p-3 rounded-xl bg-[#060e1a] border border-white/5 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-[#00ffb3]" />
                <span>%94 Model R²</span>
              </div>
              <div className="p-3 rounded-xl bg-[#060e1a] border border-white/5 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#00ffb3]" />
                <span>AI Pazar Raporu</span>
              </div>
              <div className="p-3 rounded-xl bg-[#060e1a] border border-white/5 flex items-center gap-2">
                <Database className="w-4 h-4 text-[#00ffb3]" />
                <span>46 Marka &middot; 81 İl</span>
              </div>
            </div>
          </div>

          <Link
            href="/degerleme"
            className="w-full py-4 rounded-2xl bg-[#00ffb3] text-[#040812] font-black text-sm uppercase tracking-wider flex items-center justify-center gap-2 hover:bg-[#22ffa8] transition-all hover:scale-[1.02] shadow-[0_0_30px_rgba(0,255,179,0.4)]"
          >
            <span>Değerleme Sayfasına Git</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </motion.div>

        {/* Card 2: Akıllı Araç Keşfi */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="relative rounded-3xl bg-gradient-to-br from-[#0e1d33]/90 via-[#081220] to-[#040812] border border-[#00ffb3]/30 p-8 sm:p-10 shadow-[0_25px_70px_rgba(0,0,0,0.7)] flex flex-col justify-between group hover:border-[#00ffb3]/60 transition-all hover:-translate-y-2"
        >
          <div>
            <div className="flex items-center justify-between mb-6">
              <div className="w-14 h-14 rounded-2xl bg-[#00c48c]/15 border border-[#00ffb3]/40 flex items-center justify-center text-[#00ffb3] shadow-[0_0_25px_rgba(0,196,140,0.2)] group-hover:scale-110 transition-transform">
                <Search className="w-7 h-7" />
              </div>
              <span className="text-xs font-black uppercase tracking-wider px-3.5 py-1.5 rounded-full bg-[#00ffb3]/15 text-[#00ffb3] border border-[#00ffb3]/30">
                Alıcı Modülü
              </span>
            </div>

            <h3 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-3">
              Akıllı Araç Keşfi
            </h3>

            <p className="text-sm text-slate-300 leading-relaxed font-normal mb-8">
              Bütçeli veya esnek kriterlerinizi belirleyin; bütçe-ağırlıklı akıllı keşif motorumuz kriterlerinize en uygun fırsat ilanlarını 3-4 cümlelik yapay zeka pazar gerekçeleriyle ilk 20 araç olarak listelesin.
            </p>

            <div className="grid grid-cols-2 gap-3 mb-8 text-xs font-bold text-slate-300">
              <div className="p-3 rounded-xl bg-[#060e1a] border border-white/5 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#00ffb3]" />
                <span>Akıllı Eşleşme</span>
              </div>
              <div className="p-3 rounded-xl bg-[#060e1a] border border-white/5 flex items-center gap-2">
                <Zap className="w-4 h-4 text-[#00ffb3]" />
                <span>Bütçe Optimizasyonu</span>
              </div>
              <div className="p-3 rounded-xl bg-[#060e1a] border border-white/5 flex items-center gap-2">
                <Car className="w-4 h-4 text-[#00ffb3]" />
                <span>İlk 20 Eşleşme</span>
              </div>
              <div className="p-3 rounded-xl bg-[#060e1a] border border-white/5 flex items-center gap-2">
                <Database className="w-4 h-4 text-[#00ffb3]" />
                <span>Geniş Filtreler</span>
              </div>
            </div>
          </div>

          <Link
            href="/kesif"
            className="w-full py-4 rounded-2xl bg-[#00ffb3] text-[#040812] font-black text-sm uppercase tracking-wider flex items-center justify-center gap-2 hover:bg-[#22ffa8] transition-all hover:scale-[1.02] shadow-[0_0_30px_rgba(0,255,179,0.4)]"
          >
            <span>Araç Keşfi Sayfasına Git</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
