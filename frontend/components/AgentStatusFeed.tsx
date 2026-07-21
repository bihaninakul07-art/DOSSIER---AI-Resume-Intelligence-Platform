"use client";

import { motion, AnimatePresence } from "framer-motion";
import { StatusEvent } from "@/lib/api";
import {
  FileSearch, Brain, Database, TrendingUp, Scale, Lightbulb, Image as ImageIcon, Check,
} from "lucide-react";

const NODES = [
  { key: "parser", icon: FileSearch, color: "#D89B4A" },
  { key: "extractor", icon: Brain, color: "#4A8C7C" },
  { key: "rag_agent", icon: Database, color: "#D89B4A" },
  { key: "market_trend_agent", icon: TrendingUp, color: "#4A8C7C" },
  { key: "critique", icon: Scale, color: "#B5564C" },
  { key: "recommendation_agent", icon: Lightbulb, color: "#D89B4A" },
  { key: "poster", icon: ImageIcon, color: "#4A8C7C" },
];

export default function AgentStatusFeed({ events }: { events: StatusEvent[] }) {
  const completedKeys = new Set(events.map((e) => e.node));
  const currentKey = events[events.length - 1]?.node;
  const currentLabel = events[events.length - 1]?.label;
  const stepNumber = events.length;
  const totalSteps = NODES.length;

  const labelByKey = new Map(events.map((e) => [e.node, e.label]));

  return (
    <div className="stamp-border rounded-sm bg-surface/70 backdrop-blur p-6">
      <div className="flex items-center justify-between mb-6">
        <p className="font-mono text-xs tracking-widest text-muted uppercase">
          Live pipeline
        </p>
        <p className="font-mono text-xs tracking-widest text-amber uppercase">
          Step {Math.min(stepNumber, totalSteps)} / {totalSteps}
        </p>
      </div>

      <div className="grid grid-cols-7 gap-1 mb-6">
        {NODES.map((node, i) => {
          const done = completedKeys.has(node.key) && node.key !== currentKey;
          const active = node.key === currentKey;
          return (
            <div key={node.key} className="flex items-center">
              <motion.div
                animate={active ? { scale: [1, 1.15, 1] } : { scale: 1 }}
                transition={active ? { duration: 1.1, repeat: Infinity } : {}}
                className="w-9 h-9 rounded-full flex items-center justify-center shrink-0 mx-auto"
                style={{
                  background: done || active ? `${node.color}22` : "#1C1C1F",
                  border: `1.5px solid ${done || active ? node.color : "#33333880"}`,
                  boxShadow: active ? `0 0 16px ${node.color}55` : "none",
                }}
              >
                {done ? (
                  <Check className="w-4 h-4" style={{ color: node.color }} />
                ) : (
                  <node.icon
                    className="w-4 h-4"
                    style={{ color: active ? node.color : "#8A8A90" }}
                  />
                )}
              </motion.div>
              {i < NODES.length - 1 && (
                <svg width="100%" height="2" className="flex-1 hidden sm:block">
                  <line
                    x1="0" y1="1" x2="100%" y2="1"
                    stroke={done ? "#4A8C7C" : "#33333880"}
                    strokeWidth="2"
                    className={done ? "flow-line" : ""}
                  />
                </svg>
              )}
            </div>
          );
        })}
      </div>

      <AnimatePresence mode="wait">
        <motion.p
          key={currentLabel}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -6 }}
          className="font-mono text-base text-text text-center mb-4"
        >
          {currentLabel || "Initializing pipeline..."}
        </motion.p>
      </AnimatePresence>

      <ul className="space-y-1.5 border-t border-border pt-4">
        {NODES.map((node) => {
          const label = labelByKey.get(node.key);
          const done = completedKeys.has(node.key) && node.key !== currentKey;
          const active = node.key === currentKey;
          if (!label) return null;
          return (
            <li
              key={node.key}
              className="flex items-center gap-2 font-mono text-xs"
              style={{ color: done ? "#8A8A90" : active ? node.color : "#8A8A90" }}
            >
              {done ? (
                <Check className="w-3 h-3 shrink-0" style={{ color: node.color }} />
              ) : (
                <span
                  className="w-1.5 h-1.5 rounded-full shrink-0 pulse-dot"
                  style={{ background: node.color }}
                />
              )}
              <span className={done ? "line-through decoration-1" : ""}>{label}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
