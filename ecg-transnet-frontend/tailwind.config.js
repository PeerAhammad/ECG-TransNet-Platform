export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary:  { DEFAULT: "#0ea5e9", dark: "#0284c7" },
        danger:   "#ef4444",
        success:  "#22c55e",
        warning:  "#f59e0b",
      }
    }
  },
  plugins: []
}
