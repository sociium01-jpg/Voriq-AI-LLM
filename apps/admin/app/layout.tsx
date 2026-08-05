import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Voriq AI Admin & Model Registry Control Panel',
  description: 'Manage datasets, LoRA fine-tuning pipelines, model evaluation, canary deployments, and GPU workers.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-background text-primaryText">
        {children}
      </body>
    </html>
  );
}
