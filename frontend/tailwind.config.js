/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nestle: "#3a3a4a",
        grey: "#e4e4e7"
      },
      animation: {
      'fade-in': 'fadeIn 0.3s ease-out',
      'slide-up': 'slideUp 0.4s ease-out',
    },
    keyframes: {
      fadeIn: {
        '0%': { opacity: 0 },
        '100%': { opacity: 1 },
      },
      slideUp: {
        '0%': { opacity: 0, transform: 'translateY(20px)' },
        '100%': { opacity: 1, transform: 'translateY(0)' },
      },
    },
    },
  },
  plugins: [],
}