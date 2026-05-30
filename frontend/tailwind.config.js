/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: '#090a0f',
        darkCard: 'rgba(15, 18, 36, 0.4)',
        cyanGlow: '#00f2fe',
        purpleGlow: '#4facfe',
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        glow: '0 0 20px rgba(0, 242, 254, 0.15)',
        glowPurple: '0 0 20px rgba(79, 172, 254, 0.15)',
      }
    },
  },
  plugins: [],
}
