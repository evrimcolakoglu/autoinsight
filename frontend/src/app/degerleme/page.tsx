"use client";

import { useRouter } from "next/navigation";
import StickySubNav from "@/components/navbar/StickySubNav";
import SellerScreen from "@/components/seller/SellerScreen";
import FooterSection from "@/components/footer/FooterSection";
import DynamicBackground from "@/components/background/DynamicBackground";

export default function DegerlemePage() {
  const router = useRouter();

  return (
    <main className="relative min-h-screen bg-[#040812] text-[#f8fafc] overflow-hidden">
      <DynamicBackground />
      <div className="relative z-10">
        <StickySubNav />
        <SellerScreen onBack={() => router.push("/")} />
        <FooterSection />
      </div>
    </main>
  );
}
