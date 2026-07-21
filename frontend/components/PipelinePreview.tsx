"use client";

import { motion } from "framer-motion";
import {
  FileSearch, Brain, Database, TrendingUp, Scale, Lightbulb, Image as ImageIcon,
} from "lucide-react";

const STEPS = [
  { icon: FileSearch, title: "Parse", desc: "Read the PDF into structured sections", color: "#D89B4A" },
  { icon: Brain, title: "Extract", desc: "Groq pulls skills, domain, seniority", color: "#4A8C7C" },
  { icon: Database, title: "Retrieve", desc: "Hybrid RAG pulls role benchmarks", color: "#D89B4A" },
  { icon: TrendingUp, title: "Market Check", desc: "Live search for current demand", color: "#4A8C7C" },
  { icon: Scale, title: "Critique", desc: "NVIDIA NIM weighs profile vs. evidence", color: "#B5564C" },
  { icon: Lightbulb, title: "Recommend", desc: "Cross-checked, grounded advice", color: "#D89B4A" },
  { icon: ImageIcon, title: "Illustrate", desc: "FLUX renders your roadmap poster", color: "#4A8C7C" },
];

export default function PipelinePreview() {
  return (
    <div className="mb-10">
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="font-mono text-xs tracking-widest text-muted uppercase mb-4"
      >
        How the pipeline thinks
      </motion.p>
      <div className="flex overflow-x-auto gap-0 pb-2 -mx-1 px-1">
        {STEPS.map((s, i) => (
          <div key={s.title} className="flex items-center shrink-0">
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.07 }}
              className="glow-card stamp-border rounded-sm bg-surface/60 backdrop-blur px-4 py-3 w-[132px]"
            >
              <div
                className="w-7 h-7 rounded-full flex items-center justify-center mb-2"
                style={{ background: `${s.color}22`, border: `1px solid ${s.color}55` }}
              >
                <s.icon className="w-3.5 h-3.5" style={{ color: s.color }} />
              </div>
              <p className="font-display text-sm text-text">{s.title}</p>
              <p className="text-[11px] text-muted mt-1 leading-snug">{s.desc}</p>
            </motion.div>
            {i < STEPS.length - 1 && (
              <svg width="20" height="2" className="shrink-0 mx-1">
                <line x1="0" y1="1" x2="20" y2="1" stroke="#33333880" strokeWidth="2" strokeDasharray="4 3" />
              </svg>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
