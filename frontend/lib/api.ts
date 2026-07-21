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
  let currentEvent: string | null = null;
  let currentDataLines: string[] = [];

  function dispatch() {
    if (!currentEvent || currentDataLines.length === 0) {
      currentEvent = null;
      currentDataLines = [];
      return;
    }
    const data = currentDataLines.join("\n");
    try {
      if (currentEvent === "status") {
        onStatus(JSON.parse(data));
      } else if (currentEvent === "complete") {
        onComplete(JSON.parse(data));
      } else if (currentEvent === "error") {
        onError(JSON.parse(data).message);
      }
    } catch (err) {
      console.error("SSE parse error:", err, data);
      onError("Failed to parse server response.");
    }
    currentEvent = null;
    currentDataLines = [];
  }

  function processLine(line: string) {
    if (line === "") {
      // Blank line = end of one event. Dispatch and reset.
      dispatch();
      return;
    }
    if (line.startsWith("event:")) {
      currentEvent = line.slice(6).trim();
    } else if (line.startsWith("data:")) {
      currentDataLines.push(line.slice(5).replace(/^ /, ""));
    }
    // Ignore comment lines (starting with ":") and anything else per SSE spec.
  }

  while (true) {
    const { done, value } = await reader.read();
    if (done) {
      buffer += decoder.decode(); // flush any pending multi-byte chars
      const lines = buffer.split(/\r?\n/);
      for (const line of lines) processLine(line);
      // Final dispatch in case the stream ended without a trailing blank line.
      dispatch();
      break;
    }
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split(/\r?\n/);
    buffer = lines.pop() || ""; // keep last (possibly incomplete) line in buffer
    for (const line of lines) processLine(line);
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
