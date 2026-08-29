import StickySubNav from "@/components/navbar/StickySubNav";
import HeroSection from "@/components/hero/HeroSection";
import HighlightsSection from "@/components/metrics/HighlightsSection";
import CockpitShowcase from "@/components/cockpit/CockpitShowcase";
import BentoGridSection from "@/components/bento/BentoGridSection";
import ExperienceShowcase from "@/components/showcase/ExperienceShowcase";
import ProcessTimeline from "@/components/timeline/ProcessTimeline";
import FooterSection from "@/components/footer/FooterSection";
import DynamicBackground from "@/components/background/DynamicBackground";

export default function Home() {
  return (
    <main className="relative min-h-screen bg-[#040812] text-[#f8fafc] overflow-hidden">
      {/* Dynamic Animated Ambient Background */}
      <DynamicBackground />

      {/* Content Layer */}
      <div className="relative z-10">
        {/* Sticky Glassmorphic Navigation Bar */}
        <StickySubNav />

        {/* Hero with Scroll-Pinned Valuation Studio & Laser HUD */}
        <div id="vitrin">
          <HeroSection />
        </div>

        {/* Typographic Live Metrics Bar */}
        <HighlightsSection />

        {/* AI Market Intelligence Center & Telemetry Hub */}
        <CockpitShowcase />

        {/* Bento Grid Architecture */}
        <BentoGridSection />

        {/* Full Experience Showcase (Links to /degerleme and /kesif) */}
        <ExperienceShowcase />

        {/* 3-Step Process Flow */}
        <ProcessTimeline />

        {/* Footer */}
        <FooterSection />
      </div>
    </main>
  );
}
