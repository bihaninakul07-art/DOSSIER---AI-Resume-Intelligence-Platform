"""Curated knowledge base: role -> in-demand skills, project ideas, and
resume best-practice notes. This is chunked and embedded into ChromaDB
at startup. Kept static/curated (not live-scraped) so retrieval stays
reliable and reproducible for grading/demo purposes.
"""

KNOWLEDGE_CHUNKS = [
    # --- Backend Engineering ---
    {
        "id": "be-skills-1",
        "domain": "backend",
        "text": (
            "Backend Engineer roles in 2026 commonly require: Python or Go, "
            "REST/GraphQL API design, PostgreSQL or similar RDBMS, Docker, "
            "Kubernetes basics, message queues (Kafka/RabbitMQ), and system "
            "design fundamentals (caching, load balancing, horizontal scaling)."
        ),
    },
    {
        "id": "be-projects-1",
        "domain": "backend",
        "text": (
            "Strong backend portfolio projects: a rate-limited public API with "
            "proper auth (JWT/OAuth2), a distributed task queue built with "
            "Celery/Redis, a microservice split of a monolith with Docker "
            "Compose, or a URL shortener designed to demonstrate caching and "
            "database indexing decisions."
        ),
    },
    # --- Frontend Engineering ---
    {
        "id": "fe-skills-1",
        "domain": "frontend",
        "text": (
            "Frontend Engineer roles commonly require: React or Vue, "
            "TypeScript, state management (Redux/Zustand/Context), component "
            "libraries (shadcn/ui, Tailwind), performance optimization "
            "(code-splitting, lazy loading), and accessibility (WCAG basics)."
        ),
    },
    {
        "id": "fe-projects-1",
        "domain": "frontend",
        "text": (
            "Strong frontend portfolio projects: a real-time collaborative "
            "app using WebSockets, a design-system/component library "
            "published to npm, or a dashboard with complex data "
            "visualization (D3/Recharts) and responsive layouts."
        ),
    },
    # --- Data / ML ---
    {
        "id": "ml-skills-1",
        "domain": "ml",
        "text": (
            "ML/AI Engineer roles commonly require: PyTorch or TensorFlow, "
            "experience fine-tuning or prompting LLMs, vector databases "
            "(ChromaDB, Pinecone, FAISS), RAG pipeline design, MLOps basics "
            "(experiment tracking, model serving), and strong SQL."
        ),
    },
    {
        "id": "ml-projects-1",
        "domain": "ml",
        "text": (
            "Strong ML portfolio projects: a RAG application with hybrid "
            "retrieval and citation, a fine-tuned small model for a domain "
            "task, an agentic multi-tool system with LangGraph, or an "
            "end-to-end MLOps pipeline with model monitoring."
        ),
    },
    # --- DevOps / Cloud ---
    {
        "id": "devops-skills-1",
        "domain": "devops",
        "text": (
            "DevOps/Platform roles commonly require: Terraform or Pulumi, "
            "AWS/GCP/Azure core services, CI/CD pipeline design (GitHub "
            "Actions), observability (Prometheus/Grafana), and container "
            "orchestration (Kubernetes, Helm)."
        ),
    },
    {
        "id": "devops-projects-1",
        "domain": "devops",
        "text": (
            "Strong DevOps portfolio projects: an IaC-managed multi-service "
            "deployment with Terraform, a full CI/CD pipeline with "
            "automated testing and canary deploys, or a self-hosted "
            "observability stack monitoring a personal project."
        ),
    },
    # --- Resume craft (generic best practices) ---
    {
        "id": "resume-craft-1",
        "domain": "general",
        "text": (
            "Strong resume bullet points quantify impact: 'reduced API "
            "latency by 40% by adding Redis caching' beats 'worked on "
            "backend performance.' Every bullet should show a specific "
            "action, the technology used, and a measurable outcome."
        ),
    },
    {
        "id": "resume-craft-2",
        "domain": "general",
        "text": (
            "Recruiters and ATS systems scan for role-relevant keywords in "
            "the first few lines. A resume should front-load the strongest, "
            "most relevant project or achievement rather than burying it "
            "under older or less relevant experience."
        ),
    },
]
