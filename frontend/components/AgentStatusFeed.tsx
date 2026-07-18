"use client";

import { motion, AnimatePresence } from "framer-motion";
import { StatusEvent } from "@/lib/api";
import {
  FileSearch, Brain, Database, TrendingUp, Scale, Lightbulb, Image as ImageIcon,
} from "lucide-react";

const NODES = [
  { key: "parser", icon: FileSearch, color: "#3FA796" },
  { key: "extractor", icon: Brain, color: "#4FD9E8" },
  { key: "rag_agent", icon: Database, color: "#8B7FE8" },
  { key: "market_trend_agent", icon: TrendingUp, color: "#8B7FE8" },
  { key: "critique", icon: Scale, color: "#E876B0" },
  { key: "recommendation_agent", icon: Lightbulb, color: "#E8A33D" },
  { key: "poster", icon: ImageIcon, color: "#E8A33D" },
];

export default function AgentStatusFeed({ events }: { events: StatusEvent[] }) {
  const completedKeys = new Set(events.map((e) => e.node));
  const currentKey = events[events.length - 1]?.node;
  const currentLabel = events[events.length - 1]?.label;

  return (
    <div className="stamp-border rounded-sm bg-surface/70 backdrop-blur p-6">
      <p className="font-mono text-xs tracking-widest text-muted uppercase mb-6">
        Live pipeline
      </p>

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
                  background: done || active ? `${node.color}22` : "#1B274080",
                  border: `1.5px solid ${done || active ? node.color : "#28345080"}`,
                  boxShadow: active ? `0 0 16px ${node.color}55` : "none",
                }}
              >
                <node.icon
                  className="w-4 h-4"
                  style={{ color: done || active ? node.color : "#8891A7" }}
                />
              </motion.div>
              {i < NODES.length - 1 && (
                <svg width="100%" height="2" className="flex-1 hidden sm:block">
                  <line
                    x1="0" y1="1" x2="100%" y2="1"
                    stroke={done ? "#3FA796" : "#28345080"}
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
          className="font-mono text-sm text-text text-center"
        >
          {currentLabel || "Initializing pipeline..."}
        </motion.p>
      </AnimatePresence>
    </div>
  );
}
