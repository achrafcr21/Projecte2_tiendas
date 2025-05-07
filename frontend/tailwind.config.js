/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#4F46E5', // Indigo-600
          DEFAULT: '#4338CA', // Indigo-700
          dark: '#3730A3', // Indigo-800
        },
        secondary: {
          DEFAULT: '#F3F4F6', // gris claro
          dark: '#9CA3AF',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
