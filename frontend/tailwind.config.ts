import type { Config } from "tailwindcss";
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0B0B0C",
        surface: "#131315",
        surface2: "#1C1C1F",
        border: "#33333880",
        text: "#EDEDEF",
        muted: "#8A8A90",
        amber: "#D89B4A",
        teal: "#4A8C7C",
        rose: "#B5564C",
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
