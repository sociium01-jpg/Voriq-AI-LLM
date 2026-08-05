/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0B0F19',
        surface: '#131B2E',
        surfaceBorder: '#1E293B',
        accent: '#D97706',
        accentHover: '#B45309',
        primaryText: '#F8FAFC',
        secondaryText: '#94A3B8',
      },
    },
  },
  plugins: [],
};
