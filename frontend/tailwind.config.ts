import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0B1220",
        surface: "#131B2E",
        surface2: "#1B2740",
        border: "#28345080",
        text: "#E4E9F2",
        muted: "#8891A7",
        amber: "#E8A33D",
        teal: "#3FA796",
        rose: "#D9706C",
        violet: "#8B7FE8",
        pink: "#E876B0",
        cyan: "#4FD9E8",
      },
      fontFamily: {
        display: ["var(--font-fraunces)", "serif"],
        body: ["var(--font-inter)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
    },
  },
  plugins: [],
};
export default config;
