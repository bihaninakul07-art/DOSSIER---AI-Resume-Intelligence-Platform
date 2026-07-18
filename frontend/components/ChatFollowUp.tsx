"use client";

import { useState } from "react";
import { Send } from "lucide-react";
import { askFollowup } from "@/lib/api";

interface Exchange {
  question: string;
  answer: string;
}

export default function ChatFollowUp({ sessionId }: { sessionId: string }) {
  const [question, setQuestion] = useState("");
  const [exchanges, setExchanges] = useState<Exchange[]>([]);
  const [loading, setLoading] = useState(false);

  async function submit() {
    if (!question.trim() || loading) return;
    const q = question.trim();
    setQuestion("");
    setLoading(true);
    try {
      const { answer } = await askFollowup(sessionId, q);
      setExchanges((prev) => [...prev, { question: q, answer }]);
    } catch {
      setExchanges((prev) => [...prev, { question: q, answer: "Could not reach the analysis service." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="stamp-border rounded-sm bg-surface p-6">
      <p className="font-mono text-xs tracking-widest text-muted uppercase mb-4">
        Ask the analyst
      </p>

      <div className="space-y-4 mb-4 max-h-64 overflow-y-auto">
        {exchanges.map((ex, i) => (
          <div key={i} className="space-y-1">
            <p className="text-sm text-amber font-mono">Q: {ex.question}</p>
            <p className="text-sm text-text leading-relaxed">{ex.answer}</p>
          </div>
        ))}
        {exchanges.length === 0 && (
          <p className="text-sm text-muted">
            Ask why a recommendation was made, or what to prioritize first.
          </p>
        )}
      </div>

      <div className="flex gap-2">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder="Why this project idea?"
          className="flex-1 bg-surface2 border border-border rounded-sm px-3 py-2 text-sm text-text placeholder:text-muted outline-none focus:border-amber"
        />
        <button
          onClick={submit}
          disabled={loading}
          className="px-3 py-2 bg-teal/20 border border-teal rounded-sm text-teal hover:bg-teal/30 transition-colors disabled:opacity-50"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
