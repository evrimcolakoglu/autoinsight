import StickySubNav from "@/components/navbar/StickySubNav";
import HeroSection from "@/components/hero/HeroSection";
import HighlightsSection from "@/components/metrics/HighlightsSection";
import CockpitShowcase from "@/components/cockpit/CockpitShowcase";
import BentoGridSection from "@/components/bento/BentoGridSection";
import DualSimulator from "@/components/simulator/DualSimulator";
import ProcessTimeline from "@/components/timeline/ProcessTimeline";
import FooterSection from "@/components/footer/FooterSection";

export default function Home() {
  return (
    <main className="relative min-h-screen bg-[#040812] text-[#f8fafc] overflow-hidden">
      {/* Sticky Glassmorphic Navigation Bar */}
      <StickySubNav />

      {/* Hero with Scroll-Pinned Supercar Stage & Laser HUD */}
      <div id="vitrin">
        <HeroSection />
      </div>

      {/* Typographic Live Metrics Bar */}
      <HighlightsSection />

      {/* Cockpit & Dynamic Telemetry Hub */}
      <CockpitShowcase />

      {/* Bento Grid Architecture */}
      <BentoGridSection />

      {/* Interactive Dual Valuation / Matching Simulator */}
      <DualSimulator />

      {/* 3-Step Process Flow */}
      <ProcessTimeline />

      {/* Footer */}
      <FooterSection />
    </main>
  );
}
