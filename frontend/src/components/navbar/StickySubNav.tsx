"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { ArrowUpRight, Car, Search } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function StickySubNav() {
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 100);
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      className={`fixed top-4 left-1/2 -translate-x-1/2 z-50 w-[94%] max-w-6xl transition-all duration-300 rounded-2xl ${
        scrolled || pathname !== "/"
          ? "bg-[#08101e]/85 backdrop-blur-2xl border border-white/10 shadow-2xl py-3 px-6"
          : "bg-transparent py-4 px-2"
      }`}
    >
      <div className="flex items-center justify-between">
        {/* Logo */}
        <Link
          href="/"
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#091c14] to-[#08182d] border border-[#00c48c]/40 flex items-end justify-center gap-[3px] p-2 shadow-[0_0_20px_rgba(0,196,140,0.2)] group-hover:scale-105 transition-transform">
            <div className="w-1 h-2.5 bg-[#00ffb3] rounded-sm opacity-50" />
            <div className="w-1 h-4 bg-[#00ffb3] rounded-sm opacity-75" />
            <div className="w-1 h-5.5 bg-[#00ffb3] rounded-sm" />
          </div>
          <div>
            <span className="font-extrabold text-xl tracking-tight text-white">
              Auto<span className="text-[#00ffb3] drop-shadow-[0_0_12px_rgba(0,255,179,0.4)]">Insight</span>
            </span>
          </div>
        </Link>

        {/* Dynamic Nav Links */}
        <nav className="hidden md:flex items-center gap-7 text-sm font-medium text-slate-300">
          <Link
            href="/#vitrin"
            className="hover:text-[#00ffb3] transition-colors"
          >
            Vitrin
          </Link>
          <Link
            href="/#telemetri"
            className="hover:text-[#00ffb3] transition-colors"
          >
            Telemetri
          </Link>
          <Link
            href="/#deneyim"
            className="hover:text-[#00ffb3] transition-colors"
          >
            Modüller
          </Link>
          <Link
            href="/#mimari"
            className="hover:text-[#00ffb3] transition-colors"
          >
            Yapay Zeka Mimarisi
          </Link>
        </nav>

        {/* Quick CTA Actions */}
        <div className="flex items-center gap-3">
          <Link
            href="/degerleme"
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#00ffb3] text-[#040812] font-bold text-xs uppercase tracking-wider hover:bg-[#22ffa8] transition-all hover:scale-105 shadow-[0_0_20px_rgba(0,255,179,0.3)]"
          >
            <Car className="w-3.5 h-3.5" />
            <span>Piyasa Değerleme</span>
          </Link>

          <Link
            href="/kesif"
            className="hidden sm:flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white/10 text-white hover:text-[#00ffb3] font-bold text-xs uppercase tracking-wider hover:bg-white/15 border border-white/15 transition-all"
          >
            <Search className="w-3.5 h-3.5" />
            <span>Araç Keşfi</span>
          </Link>
        </div>
      </div>
    </motion.header>
  );
}
