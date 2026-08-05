import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Voriq AI Studio — India-First Multimodal AI OS',
  description: 'Multilingual AI chat, Indian-language intelligence, RAG document analysis, character-consistent image and video production, and fine-tuning engine.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-background text-primaryText selection:bg-accent selection:text-white">
        {children}
      </body>
    </html>
  );
}
