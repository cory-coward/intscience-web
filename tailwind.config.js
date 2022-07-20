/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./js-frontend/**/*.{html,js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/forms"),
  ],
}
