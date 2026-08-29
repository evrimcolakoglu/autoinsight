"use client";

import { motion } from "framer-motion";
import { Shield, Zap, MapPin, MessageSquareText } from "lucide-react";

interface BentoItemProps {
  icon: React.ReactNode;
  title: string;
  desc: string;
  tag?: string;
  delay?: number;
}

function BentoItem({ icon, title, desc, tag, delay = 0 }: BentoItemProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 25 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.7, delay, ease: [0.16, 1, 0.3, 1] }}
      className="relative flex flex-col justify-between p-8 rounded-3xl bg-gradient-to-br from-[#0c172a]/70 via-[#070e1a]/85 to-[#040812] border border-white/10 hover:border-[#00ffb3]/50 transition-all duration-300 hover:-translate-y-1.5 shadow-[0_20px_50px_rgba(0,0,0,0.6)] group overflow-hidden"
    >
      {/* Top row */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <div className="w-12 h-12 rounded-2xl bg-[#00c48c]/10 border border-[#00ffb3]/30 flex items-center justify-center text-[#00ffb3] shadow-[0_0_20px_rgba(0,196,140,0.15)] group-hover:scale-110 transition-transform">
            {icon}
          </div>
          {tag && (
            <span className="text-[10px] font-extrabold uppercase tracking-wider px-3 py-1 rounded-full bg-[#00ffb3]/10 text-[#00ffb3] border border-[#00ffb3]/25">
              {tag}
            </span>
          )}
        </div>

        <h3 className="text-xl sm:text-2xl font-extrabold text-white tracking-tight mb-3">
          {title}
        </h3>

        <p className="text-sm text-slate-400 leading-relaxed font-normal">
          {desc}
        </p>
      </div>
    </motion.div>
  );
}

export default function BentoGridSection() {
  return (
    <section id="mimari" className="max-w-6xl mx-auto px-4 py-24">
      {/* Header */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 text-xs font-extrabold tracking-widest text-[#00ffb3] uppercase mb-3">
          <span>MÜHENDİSLİK &amp; MİMARİ</span>
        </div>
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-black text-white tracking-tight">
          Veriye Dayalı Rasyonel Karar Avantajı
        </h2>
      </div>

      {/* 4-Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <BentoItem
          icon={<Shield className="w-6 h-6" />}
          title="Random Forest Regresyon Modeli"
          desc="Spekülatif ve değişken fiyatlar yerine, binlerce gerçek ilan verisiyle eğitilmiş Target Encoding ve Random Forest boru hattı sayesinde objektif bir pazar değer koridoru elde edin."
          tag="ML PIPELINE"
          delay={0.1}
        />
        <BentoItem
          icon={<Zap className="w-6 h-6" />}
          title="Bütçe-Ağırlıklı Akıllı Eşleştirme"
          desc="Bütçenizi atıl bırakmayan, bütçe sınırına en yakın ve en avantajlı araçları kilometre, model yılı ve donanım puanlamasıyla öne çıkaran akıllı keşif algoritması."
          tag="ÖNERİ MOTORU"
          delay={0.2}
        />
        <BentoItem
          icon={<MapPin className="w-6 h-6" />}
          title="81 İl Bölgesel Pazar Dinamikleri"
          desc="İl bazlı pazar talebi, karoser formu, yakıt ve vites kombinasyonlarının yarattığı bölgesel fiyat değişimlerini hassas şekilde hesaba katan derinlikli mimari."
          tag="COĞRAFİ ANALİZ"
          delay={0.3}
        />
        <BentoItem
          icon={<MessageSquareText className="w-6 h-6" />}
          title="Yerel Yapay Zeka Pazar İçgörüsü"
          desc="Her araç için fiyat seviyesinin nedenlerini (düşük kilometre avantajı, pazar talebi, segment konumu) açıklayan 3-4 cümlelik yerel ve güvenilir doğal dil sentezi."
          tag="LOKAL AI"
          delay={0.4}
        />
      </div>
    </section>
  );
}
