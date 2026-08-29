import { Shield, Lock, Database, RefreshCw, Award } from "lucide-react";

export default function FooterSection() {
  return (
    <footer className="border-t border-white/10 bg-[#02050b] pt-16 pb-12">
      <div className="max-w-6xl mx-auto px-4">
        {/* Trust Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-4 pb-14 border-b border-white/5">
          <div className="flex items-center gap-2.5 text-xs text-slate-300 font-semibold">
            <Database className="w-4 h-4 text-[#00ffb3]" />
            <span>Gerçek Piyasa Verisi</span>
          </div>
          <div className="flex items-center gap-2.5 text-xs text-slate-300 font-semibold">
            <Lock className="w-4 h-4 text-[#00ffb3]" />
            <span>Sıfır Veri Sızıntısı</span>
          </div>
          <div className="flex items-center gap-2.5 text-xs text-slate-300 font-semibold">
            <Shield className="w-4 h-4 text-[#00ffb3]" />
            <span>Lokal &amp; Güvenli Çıkarım</span>
          </div>
          <div className="flex items-center gap-2.5 text-xs text-slate-300 font-semibold">
            <Award className="w-4 h-4 text-[#00ffb3]" />
            <span>%94 Doğruluk Oranı</span>
          </div>
          <div className="flex items-center gap-2.5 text-xs text-slate-300 font-semibold">
            <RefreshCw className="w-4 h-4 text-[#00ffb3]" />
            <span>Sürekli Güncel Model</span>
          </div>
        </div>

        {/* Footer Info */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-6 pt-10 text-xs text-slate-500 font-medium">
          <div className="flex items-center gap-3">
            <span className="font-extrabold text-white">AutoInsight</span>
            <span>&bull;</span>
            <span>v2.5 Next.js Scrollytelling Sürümü</span>
            <span>&bull;</span>
            <span>53.514 İlan Analitiği</span>
          </div>
          <div>&copy; 2026 AutoInsight — Tüm Hakları Saklıdır.</div>
        </div>
      </div>
    </footer>
  );
}
