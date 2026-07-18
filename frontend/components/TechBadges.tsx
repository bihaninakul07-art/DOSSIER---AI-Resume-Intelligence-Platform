"use client";

import { motion } from "framer-motion";

const STACK = [
  { label: "Groq · Llama 3.3", color: "#4FD9E8" },
  { label: "Gemini 2.0", color: "#8B7FE8" },
  { label: "LangGraph", color: "#3FA796" },
  { label: "ChromaDB + BM25", color: "#E8A33D" },
  { label: "FLUX.1 diffusion", color: "#E876B0" },
  { label: "fastembed", color: "#4FD9E8" },
];

export default function TechBadges() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.3 }}
      className="flex flex-wrap gap-2 mb-10"
    >
      {STACK.map((t) => (
        <span
          key={t.label}
          className="font-mono text-[10px] uppercase tracking-widest px-2.5 py-1 rounded-full border"
          style={{ color: t.color, borderColor: `${t.color}55`, background: `${t.color}0F` }}
        >
          {t.label}
        </span>
      ))}
    </motion.div>
  );
}
