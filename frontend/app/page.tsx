"use client";

import { useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import confetti from "canvas-confetti";
import AmbientBackground from "@/components/AmbientBackground";
import TechBadges from "@/components/TechBadges";
import PipelinePreview from "@/components/PipelinePreview";
import FeatureGrid from "@/components/FeatureGrid";
import UploadZone from "@/components/UploadZone";
import AgentStatusFeed from "@/components/AgentStatusFeed";
import ResultsDashboard from "@/components/ResultsDashboard";
import PosterCard from "@/components/PosterCard";
import ChatFollowUp from "@/components/ChatFollowUp";
import { analyzeResume, AnalysisResult, StatusEvent } from "@/lib/api";

type Stage = "idle" | "running" | "done" | "error";

export default function Home() {
  const [stage, setStage] = useState<Stage>("idle");
  const [events, setEvents] = useState<StatusEvent[]>([]);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleFile(file: File) {
    setStage("running");
    setEvents([]);
    setResult(null);
    setError(null);

    await analyzeResume(
      file,
      (e) => setEvents((prev) => [...prev, e]),
      (r) => {
        setResult(r);
        setStage("done");
        confetti({
          particleCount: 90,
          spread: 70,
          origin: { y: 0.3 },
          colors: ["#E8A33D", "#3FA796", "#E876B0", "#4FD9E8"],
        });
      },
      (msg) => { setError(msg); setStage("error"); }
    );
  }

  return (
    <main className="relative max-w-4xl mx-auto px-6 py-16 z-10">
      <AmbientBackground />

      <motion.header
        initial={{ opacity: 0, y: -12 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-12 relative"
      >
        <div className="flex items-start justify-between mb-6">
          <span className="font-mono text-[10px] tracking-widest text-teal uppercase px-2.5 py-1 rounded-full border border-teal/40 bg-teal/10">
            ● 7 agents online
          </span>
          <Link href="/history" className="font-mono text-xs uppercase tracking-widest text-muted hover:text-teal transition-colors whitespace-nowrap">
            Case archive →
          </Link>
        </div>
        <p className="font-mono text-xs tracking-widest text-amber uppercase mb-2">
          Case File — Resume Intelligence
        </p>
        <h1 className="font-display text-6xl italic shimmer-text leading-none">DOSSIER</h1>
        <p className="text-muted mt-4 max-w-lg text-[15px] leading-relaxed">
          Drop in a resume. A multi-agent pipeline parses it, retrieves grounded
          role benchmarks, cross-checks two LLMs, and returns an evidence-based
          career report — with a generated roadmap poster.
        </p>
      </motion.header>

      {stage === "idle" && <TechBadges />}
      {stage === "idle" && <PipelinePreview />}

      {stage === "idle" && <FeatureGrid />}

      {stage !== "done" && (
        <UploadZone onFile={handleFile} disabled={stage === "running"} />
      )}

      <AnimatePresence>
        {stage === "running" && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-8"
          >
            <AgentStatusFeed events={events} />
          </motion.div>
        )}
      </AnimatePresence>

      {stage === "error" && (
        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-8 text-rose font-mono text-sm">
          Error: {error}
        </motion.p>
      )}

      {stage === "done" && result && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-8 space-y-6"
        >
          <button
            onClick={() => setStage("idle")}
            className="font-mono text-xs uppercase tracking-widest text-muted hover:text-teal transition-colors"
          >
            ← Analyze another resume
          </button>
          <ResultsDashboard result={result} />
          <PosterCard posterUrl={result.poster_url} />
          <ChatFollowUp sessionId={result.session_id} />
        </motion.div>
      )}
    </main>
  );
}
