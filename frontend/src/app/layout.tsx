import type { Metadata } from "next";
import { Plus_Jakarta_Sans, Space_Grotesk } from "next/font/google";
import "./globals.css";
import SmoothScrollProvider from "@/components/providers/SmoothScrollProvider";

const plusJakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-sans",
});

const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "AutoInsight — Akıllı Otomotiv Karar Platformu",
  description:
    "53.000'den fazla gerçek pazar verisi ve yapay zeka ile aracınızın gerçek piyasa değerini ve en avantajlı fırsatları saniyeler içinde keşfedin.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="tr" className={`${plusJakarta.variable} ${spaceGrotesk.variable} dark`}>
      <body className="bg-[#040812] text-[#f8fafc] min-h-screen antialiased selection:bg-[#00ffb3] selection:text-[#040812]">
        <SmoothScrollProvider>{children}</SmoothScrollProvider>
      </body>
    </html>
  );
}
