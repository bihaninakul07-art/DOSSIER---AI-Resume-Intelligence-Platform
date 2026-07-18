"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AnalysisResult } from "@/lib/api";

const TABS = ["Recommendations", "Skill Gaps", "Profile"] as const;
type Tab = (typeof TABS)[number];

export default function ResultsDashboard({ result }: { result: AnalysisResult }) {
  const [tab, setTab] = useState<Tab>("Recommendations");

  const strengthCount = result.gap_analysis.strengths.length;
  const gapCount = result.gap_analysis.missing_skills.length;
  const skillCount = result.extracted_profile.skills.length;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-3">
        <StatCard value={skillCount} label="Skills Found" color="#4FD9E8" />
        <StatCard value={strengthCount} label="Strengths" color="#3FA796" />
        <StatCard value={gapCount} label="Gaps to Close" color="#E876B0" />
      </div>

      <div className="stamp-border rounded-sm bg-surface/70 backdrop-blur p-6">
        <div className="flex gap-1 mb-6 border-b border-border relative">
          {TABS.map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`relative font-mono text-xs tracking-widest uppercase px-3 py-2 transition-colors ${
                tab === t ? "text-text" : "text-muted hover:text-text"
              }`}
            >
              {t}
              {tab === t && (
                <motion.div
                  layoutId="tab-underline"
                  className="absolute left-0 right-0 -bottom-[1px] h-[2px]"
                  style={{ background: "linear-gradient(90deg, #E8A33D, #E876B0)" }}
                />
              )}
            </button>
          ))}
        </div>

        <AnimatePresence mode="wait">
          <motion.div
            key={tab}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.25 }}
          >
            {tab === "Recommendations" && (
              <div className="space-y-6">
                <Section title="Project Ideas" items={result.recommendation.project_ideas} color="#3FA796" />
                <Section title="Skills to Learn" items={result.recommendation.skills_to_learn} color="#E8A33D" />
                <Section title="Overall Recommendations" items={result.recommendation.overall_recommendations} color="#E876B0" />
                {result.recommendation.grounded_sources.length > 0 && (
                  <p className="font-mono text-xs text-muted pt-2 border-t border-border">
                    Grounded in {result.recommendation.grounded_sources.length} retrieved source(s):{" "}
                    {result.recommendation.grounded_sources.join(", ")}
                  </p>
                )}
              </div>
            )}

            {tab === "Skill Gaps" && (
              <div className="space-y-6">
                <p className="text-text leading-relaxed">{result.gap_analysis.reasoning}</p>
                <Section title="Missing Skills" items={result.gap_analysis.missing_skills} color="#E876B0" />
                <Section title="Weak Sections" items={result.gap_analysis.weak_sections} color="#E8A33D" />
                <Section title="Strengths" items={result.gap_analysis.strengths} color="#3FA796" />
              </div>
            )}

            {tab === "Profile" && (
              <div className="space-y-3 font-mono text-sm">
                <Row label="Primary Domain" value={result.extracted_profile.primary_domain} />
                <Row label="Seniority" value={result.extracted_profile.seniority} />
                <Row
                  label="Years Experience"
                  value={result.extracted_profile.years_experience?.toString() ?? "unclear"}
                />
                <Row label="Skills" value={result.extracted_profile.skills.join(", ") || "none extracted"} />
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}

function StatCard({ value, label, color }: { value: number; label: string; color: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glow-card stamp-border rounded-sm bg-surface/70 backdrop-blur p-4 text-center"
    >
      <p className="font-display text-3xl" style={{ color }}>{value}</p>
      <p className="font-mono text-[10px] uppercase tracking-widest text-muted mt-1">{label}</p>
    </motion.div>
  );
}

function Section({ title, items, color }: { title: string; items: string[]; color: string }) {
  if (!items.length) return null;
  return (
    <div>
      <p className="font-mono text-xs tracking-widest uppercase mb-2" style={{ color }}>{title}</p>
      <ul className="space-y-1.5">
        {items.map((item, i) => (
          <motion.li
            key={i}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className="text-text text-sm leading-relaxed pl-4 border-l-2"
            style={{ borderColor: `${color}55` }}
          >
            {item}
          </motion.li>
        ))}
      </ul>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between border-b border-border pb-2">
      <span className="text-muted uppercase tracking-wide text-xs">{label}</span>
      <span className="text-text">{value}</span>
    </div>
  );
}
