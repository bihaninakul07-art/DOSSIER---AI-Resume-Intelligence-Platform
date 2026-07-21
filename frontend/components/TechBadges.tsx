"use client";

import { motion } from "framer-motion";

const STACK = [
  { label: "NVIDIA NIM · Nemotron", color: "#D89B4A" },
  { label: "Groq · Llama 3.3", color: "#4A8C7C" },
  { label: "LangGraph", color: "#4A8C7C" },
  { label: "ChromaDB + BM25", color: "#D89B4A" },
  { label: "Pollinations · FLUX", color: "#B5564C" },
  { label: "fastembed", color: "#D89B4A" },
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
