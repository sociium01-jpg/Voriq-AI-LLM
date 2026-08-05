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
        background: '#090D16',
        surface: '#111827',
        surfaceBorder: '#1F293D',
        accent: '#D97706', // Indian Saffron Warmth
        accentHover: '#B45309',
        primaryText: '#F3F4F6',
        secondaryText: '#9CA3AF',
      },
    },
  },
  plugins: [],
};
