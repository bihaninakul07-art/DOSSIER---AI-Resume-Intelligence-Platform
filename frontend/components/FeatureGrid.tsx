"use client";

import { motion } from "framer-motion";
import { Network, Database, Sparkles, MessagesSquare } from "lucide-react";

const FEATURES = [
  { icon: Network, title: "Multi-Agent Pipeline", desc: "6 specialist agents parse, retrieve, critique, and recommend — live.", color: "text-teal" },
  { icon: Database, title: "Grounded in RAG", desc: "Recommendations cite real retrieved role benchmarks, not guesses.", color: "text-violet" },
  { icon: Sparkles, title: "Visual Roadmap", desc: "A generated poster maps your skill gaps and next projects.", color: "text-pink" },
  { icon: MessagesSquare, title: "Ask Follow-ups", desc: "Question any verdict — the analyst remembers your report.", color: "text-cyan" },
];

export default function FeatureGrid() {
  return (
    <div className="grid grid-cols-2 gap-3 mb-10">
      {FEATURES.map((f, i) => (
        <motion.div
          key={f.title}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.08, duration: 0.4 }}
          className="glow-card stamp-border rounded-sm bg-surface/60 backdrop-blur p-4"
        >
          <f.icon className={`w-5 h-5 mb-2 ${f.color}`} />
          <p className="font-display text-sm text-text">{f.title}</p>
          <p className="text-xs text-muted mt-1 leading-relaxed">{f.desc}</p>
        </motion.div>
      ))}
    </div>
  );
}
