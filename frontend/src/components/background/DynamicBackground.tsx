"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";

export default function DynamicBackground() {
  const [mousePos, setMousePos] = useState({ x: -1000, y: -1000 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener("mousemove", handleMouseMove, { passive: true });
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      {/* Interactive Cursor Spotlight Glow */}
      <div
        className="absolute w-[600px] h-[600px] rounded-full bg-radial from-[#00ffb3]/10 via-[#38bdf8]/5 to-transparent blur-[100px] -translate-x-1/2 -translate-y-1/2 transition-transform duration-100 ease-out"
        style={{
          left: `${mousePos.x}px`,
          top: `${mousePos.y}px`,
        }}
      />

      {/* Floating Animated Gradient Orbs */}
      <motion.div
        animate={{
          x: [0, 80, -60, 0],
          y: [0, -70, 50, 0],
          scale: [1, 1.2, 0.9, 1],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute top-10 left-[10%] w-[500px] h-[500px] bg-gradient-to-tr from-[#00ffb3]/12 via-[#00c48c]/8 to-transparent rounded-full blur-[130px]"
      />

      <motion.div
        animate={{
          x: [0, -90, 70, 0],
          y: [0, 80, -60, 0],
          scale: [1, 0.9, 1.15, 1],
        }}
        transition={{
          duration: 24,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute top-[45%] right-[5%] w-[650px] h-[650px] bg-gradient-to-bl from-[#38bdf8]/12 via-[#00c48c]/6 to-transparent rounded-full blur-[140px]"
      />

      <motion.div
        animate={{
          x: [0, 60, -80, 0],
          y: [0, -50, 70, 0],
          scale: [1, 1.1, 0.95, 1],
        }}
        transition={{
          duration: 28,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        className="absolute bottom-10 left-[25%] w-[550px] h-[550px] bg-gradient-to-r from-[#00ffb3]/10 via-[#a855f7]/8 to-transparent rounded-full blur-[140px]"
      />

      {/* Cyber Grid Matrix with Subtle Perspective */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-70" />

      {/* Subtle Scan Lines Texture */}
      <div className="absolute inset-0 bg-[radial-gradient(rgba(0,255,179,0.03)_1px,transparent_1px)] bg-[size:24px_24px] opacity-60" />
    </div>
  );
}
