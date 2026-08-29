"use client";

import { motion } from "framer-motion";
import { SlidersHorizontal, Cpu, FileText } from "lucide-react";

export default function ProcessTimeline() {
  const steps = [
    {
      num: "01",
      title: "Parametreleri Belirleyin",
      desc: "Marka, seri, model, yıl, kilometre, yakıt, vites ve kasa bilgilerini akıllı arayüz üzerinden aktarın.",
      icon: <SlidersHorizontal className="w-6 h-6" />,
    },
    {
      num: "02",
      title: "Yapay Zeka Telemetrisi",
      desc: "Gelişmiş analitik motorumuz aracın piyasa değerini, %11.09 MAPE güven aralığını ve emsal pazar konumunu anında hesaplar.",
      icon: <Cpu className="w-6 h-6" />,
    },
    {
      num: "03",
      title: "Gerekçeli Piyasa Raporu",
      desc: "Güven koridoru, emsal ilan yüzdelik konumu ve 3-4 cümlelik yapay zeka pazar analiziyle objektif değerleme raporunuzu alın.",
      icon: <FileText className="w-6 h-6" />,
    },
  ];

  return (
    <section className="max-w-6xl mx-auto px-4 py-24">
      {/* Header */}
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 text-xs font-extrabold tracking-widest text-[#00ffb3] uppercase mb-3">
          <span>İŞLEM AKIŞI</span>
        </div>
        <h2 className="text-3xl sm:text-4xl md:text-5xl font-black text-white tracking-tight">
          Üç Adımda Akıllı Değerleme
        </h2>
      </div>

      {/* 3-Steps Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {steps.map((step, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 25 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: idx * 0.15 }}
            className="relative p-8 rounded-3xl bg-gradient-to-b from-[#091526] to-[#050b14] border border-white/10 hover:border-[#00ffb3]/40 transition-all duration-300 hover:-translate-y-1 shadow-2xl flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-6">
                <span className="font-mono text-xs font-black tracking-widest text-[#00ffb3] px-3 py-1 rounded-lg bg-[#00ffb3]/10 border border-[#00ffb3]/25">
                  ADIM {step.num}
                </span>
                <div className="text-[#00ffb3]">{step.icon}</div>
              </div>

              <h3 className="text-xl font-extrabold text-white tracking-tight mb-3">
                {step.title}
              </h3>

              <p className="text-sm text-slate-400 leading-relaxed font-normal">
                {step.desc}
              </p>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
