export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface StatusEvent {
  node: string;
  label: string;
}

export interface AnalysisResult {
  session_id: string;
  extracted_profile: {
    skills: string[];
    years_experience: number | null;
    primary_domain: string;
    seniority: string;
  };
  gap_analysis: {
    missing_skills: string[];
    weak_sections: string[];
    strengths: string[];
    reasoning: string;
  };
  recommendation: {
    project_ideas: string[];
    skills_to_learn: string[];
    overall_recommendations: string[];
    grounded_sources: string[];
  };
  poster_url: string | null;
  provider_notes: Record<string, unknown>;
}

/**
 * Streams the /api/analyze SSE response, invoking onStatus for each agent
 * status event and onComplete/onError with the terminal event.
 */
export async function analyzeResume(
  file: File,
  onStatus: (e: StatusEvent) => void,
  onComplete: (r: AnalysisResult) => void,
  onError: (message: string) => void
) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_URL}/api/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!res.body) {
    onError("No response stream from server.");
    return;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const chunks = buffer.split("\n\n");
    buffer = chunks.pop() || "";

    for (const chunk of chunks) {
      const eventMatch = chunk.match(/^event:\s*(.+)$/m);
      const dataMatch = chunk.match(/^data:\s*(.+)$/m);
      if (!eventMatch || !dataMatch) continue;

      const eventType = eventMatch[1].trim();
      const data = dataMatch[1].trim();

      if (eventType === "status") {
        onStatus(JSON.parse(data));
      } else if (eventType === "complete") {
        onComplete(JSON.parse(data));
      } else if (eventType === "error") {
        onError(JSON.parse(data).message);
      }
    }
  }
}

export async function fetchHistory() {
  const res = await fetch(`${API_URL}/api/history`);
  if (!res.ok) throw new Error("Failed to fetch history");
  return res.json();
}

export async function askFollowup(sessionId: string, question: string) {
  const res = await fetch(`${API_URL}/api/followup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, question }),
  });
  if (!res.ok) throw new Error("Follow-up request failed");
  return res.json();
}
