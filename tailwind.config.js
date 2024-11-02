/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.{html,js}",  // adjust path to match your HTML template files
    "./app/static/js/**/*.js"           // adjust path to your custom JS files
  ],
  theme: {
    extend: {
      colors: {
        backgroundMain: "#f0f4f8",
        backgroundContainer: "#ffffff",
        textPrimary: "#1b1f3b",
        textSecondary: "#4a5568",
        accentPrimary: "#00d9ff",
        accentPrimaryHover: "#00b3cc"
      },
      fontFamily: {
        sans: ['Kumbh Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

