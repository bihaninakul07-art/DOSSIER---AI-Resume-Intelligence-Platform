"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchHistory } from "@/lib/api";

interface HistoryItem {
  session_id: string;
  created_at: number;
  result: { extracted_profile: { primary_domain: string; seniority: string } };
}

export default function HistoryPage() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory()
      .then((data) => setItems(data.items))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="max-w-3xl mx-auto px-6 py-16">
      <Link href="/" className="font-mono text-xs uppercase tracking-widest text-muted hover:text-teal transition-colors">
        ← Back
      </Link>
      <h1 className="font-display text-3xl italic text-text mt-4 mb-8">Case Archive</h1>

      {loading && <p className="text-muted">Loading past cases...</p>}
      {!loading && items.length === 0 && (
        <p className="text-muted">No analyses on record yet.</p>
      )}

      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.session_id} className="stamp-border rounded-sm bg-surface p-4 flex justify-between items-center">
            <div>
              <p className="font-mono text-xs text-muted uppercase">
                {new Date(item.created_at * 1000).toLocaleString()}
              </p>
              <p className="text-text">
                {item.result.extracted_profile.primary_domain} —{" "}
                {item.result.extracted_profile.seniority}
              </p>
            </div>
            <p className="font-mono text-xs text-muted">{item.session_id.slice(0, 8)}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
