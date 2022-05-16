//const defaultTheme = require("tailwindcss/defaultTheme")

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    container: {
      center: true
    },
    extend: {
      fontFamily: {
        sans: ["Inter var", "sans-serif"]
      },
      colors: {
        "blue": "#1DA1F2",
        "darkblue": "#2795D9",
        "lightblue": "#EFF9FF",
        "dark": "#657786",
        "light": "#AAAB8C2",
        "lighter": "#E1E8ED",
        "lightest": "#F5F8FA",
      }
    },
  },
  plugins: [
    require('@formkit/tailwindcss').default
  ],
}