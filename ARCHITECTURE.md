# Architecture

## Pipeline
```
PDF upload
   │
   ▼
Parser Agent ──────► structured sections (experience, education, projects, skills)
   │
   ▼
Extractor Agent ───► normalized profile (skills[], years_exp, domain, seniority) — LLM, JSON mode
   │
   ├──────────────┬─────────────────────┐
   ▼              ▼                     │  (parallel branch)
RAG Agent    Market Trend Agent         │
(ChromaDB    (live web search,          │
hybrid       degrades gracefully        │
BM25+        if unavailable)            │
semantic)         │                     │
   └──────┬───────┘                     │
          ▼                             │
     Critique Agent ◄────────────────────┘
     (LLM: compares profile against retrieved
      benchmarks + market notes → gap analysis)
          │
          ▼
     Recommendation Agent
     (LLM, cross-validated across 2 providers →
      project ideas, skills to learn, overall advice)
          │
          ▼
     Poster Agent
     (NVIDIA NIM FLUX image gen from recommendation summary)
          │
          ▼
     Final structured report + poster, streamed live
     to the frontend via SSE as each node completes
```

Orchestrated as a LangGraph `StateGraph`. The RAG Agent and Market Trend
Agent both run off the Extractor's output and both must complete before
Critique runs — a parallelization + merge pattern, not a linear chain.

## Multi-LLM routing (single unified API)
Every agent calls exactly one function: `llm_router.generate(task=..., prompt=...)`.
The router (`app/llm/router.py`) maps task type to a provider:
- `parsing` / `extraction` / `market_search` → **Groq** (fast, cheap)
- `critique` / `recommendation` / `image_prompt` → **NVIDIA NIM** (deeper reasoning)

If the preferred provider isn't configured, the router falls back to
whichever is. The Recommendation Agent additionally calls the router with
`cross_validate=True`, which runs the same prompt on the other configured
provider and reports whether they agree — surfacing multi-LLM signal
without a stateful debate loop. Adding a third provider (OpenAI, Claude)
means writing one new client class and one router mapping line; nothing
elsewhere in the app changes.

## RAG
- **Embeddings:** fastembed, `BAAI/bge-small-en-v1.5`
- **Vector store:** ChromaDB (persistent, local disk)
- **Retrieval:** hybrid — BM25 keyword ranking + semantic embedding
  ranking, merged via Reciprocal Rank Fusion (`app/rag/hybrid_search.py`)
- **Knowledge base:** curated (not live-scraped) chunks of role-specific
  skill demand, project ideas, and resume best practices, per domain
  (backend/frontend/ml/devops/general) — kept static for reproducible
  grading/demo results
- Retrieved source IDs are surfaced in the final report so recommendations
  are traceable to specific evidence, not just LLM assertion

## Agentic workflow patterns used
Maps to the patterns described in Anthropic's "Building Effective Agents":
- **Prompt chaining** — parser → extractor → critique → recommendation
- **Parallelization** — RAG Agent + Market Trend Agent run concurrently
- **Tool use** — PDF parsing, ChromaDB retrieval, web search, image generation are all agent-callable tools
- **Routing** — the LLM router picks a provider per task type

## Memory
- **Session memory:** SQLite (`app/memory/session_store.py`) persists each
  analysis by `session_id`, plus a follow-up Q&A transcript per session so
  a user can ask "why this recommendation?" without re-uploading
- **Persistent history:** `/api/history` lists past analyses across sessions

## Streaming
`/api/analyze` returns a Server-Sent Events stream. Each LangGraph node
completion emits a `status` event (`{node, label}`); the frontend's
`AgentStatusFeed` renders these live as they arrive, then a final
`complete` event carries the full structured result.

## Bootcamp concept coverage
| Week | Concept | Implementation |
|---|---|---|
| 1–2 | LLM API + Prompting | Per-agent system prompts, JSON-mode structured output, `llm_router` |
| 3 | Image generation (diffusion) | FLUX-based poster generation via NVIDIA NIM |
| 4 | Agents & tools | Parser/RAG/search/image tools, agent-per-responsibility design |
| 5 | Multi-agent orchestration | LangGraph `StateGraph`, parallel branch + merge |
| 6 | RAG | Hybrid ChromaDB retrieval with citation |
| — | Memory | SQLite session + persistent history |
| — | Streaming | SSE live agent status |

## Known design tradeoffs
- Market Trend Agent uses unauthenticated DuckDuckGo search rather than a
  paid search API, to keep the project runnable without extra keys — traded
  reliability for zero-cost accessibility, with graceful degradation if it fails.
- Knowledge base is curated rather than dynamically scraped, trading
  breadth for reproducibility during grading/demo.
- Cross-validation on the Recommendation Agent is a single-pass compare,
  not an iterative debate — kept intentionally simple rather than adding
  the complexity/cost of a multi-round negotiation.