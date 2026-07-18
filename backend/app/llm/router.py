"""Single unified entrypoint for every LLM call in the app.

Agents call `llm_router.generate(task=..., prompt=...)` and never touch a
provider client directly. The router decides which provider handles the
task, falls back to whichever provider is actually configured, and can
optionally cross-validate a task across two providers - all behind this
one call site. Adding a new provider later means adding one client file
and one line in TASK_MODEL_MAP; nothing else in the app changes.
"""
import logging
from dataclasses import dataclass
from typing import Optional

from app.llm.base import LLMClient
from app.llm.groq_client import GroqClient
from app.llm.nvidia_client import NvidiaNimClient

logger = logging.getLogger(__name__)

# Which provider handles which kind of task, by default.
TASK_MODEL_MAP = {
    "parsing": "groq",
    "extraction": "groq",
    "market_search": "groq",
    "critique": "nvidia_nim",
    "recommendation": "nvidia_nim",
    "image_prompt": "nvidia_nim",
}


@dataclass
class LLMResult:
    text: str
    provider_used: str
    cross_check: Optional[dict] = None  # populated only when cross_validate=True


class LLMRouter:
    def __init__(self):
        self._clients: dict[str, LLMClient] = {
            "groq": GroqClient(),
            "nvidia_nim": NvidiaNimClient(),
        }

    def _pick(self, task: str) -> LLMClient:
        preferred = TASK_MODEL_MAP.get(task, "groq")
        client = self._clients.get(preferred)
        if client and getattr(client, "available", False):
            return client
        # fall back to whichever provider is actually configured
        for c in self._clients.values():
            if getattr(c, "available", False):
                logger.warning("Falling back to %s for task=%s", c.name, task)
                return c
        raise RuntimeError(
            "No LLM provider configured. Set GROQ_API_KEY and/or NVIDIA_NIM_API_KEY."
        )

    def _ordered_clients(self, task: str) -> list[LLMClient]:
        """Return clients in order: preferred first, then fallback."""
        preferred = TASK_MODEL_MAP.get(task, "groq")
        ordered = []
        if preferred in self._clients and self._clients[preferred].available:
            ordered.append(self._clients[preferred])
        for c in self._clients.values():
            if c.name != preferred and c.available:
                ordered.append(c)
        return ordered

    async def generate(
        self,
        task: str,
        prompt: str,
        system: Optional[str] = None,
        json_mode: bool = False,
        temperature: float = 0.4,
        max_tokens: int = 2000,
        cross_validate: bool = False,
    ) -> LLMResult:
        clients = self._ordered_clients(task)
        if not clients:
            raise RuntimeError("No LLM provider available. Set GROQ_API_KEY and/or NVIDIA_NIM_API_KEY.")

        last_error = None
        for i, client in enumerate(clients):
            try:
                text = await client.generate(
                    prompt, system=system, json_mode=json_mode,
                    temperature=temperature, max_tokens=max_tokens,
                )
                provider_used = client.name
                break
            except Exception as e:
                last_error = e
                logger.warning("Provider %s failed for task=%s: %s; trying fallback", client.name, task, e)
                continue
        else:
            raise RuntimeError(f"All providers failed for task={task}. Last error: {last_error}")

        cross_check = None
        if cross_validate:
            for secondary in clients[1:]:
                try:
                    alt_text = await secondary.generate(
                        prompt, system=system, json_mode=json_mode,
                        temperature=temperature, max_tokens=max_tokens,
                    )
                    cross_check = {"provider": secondary.name, "text": alt_text}
                    break
                except Exception as e:  # pragma: no cover
                    logger.warning("Cross-validation call failed: %s", e)

        return LLMResult(text=text, provider_used=provider_used, cross_check=cross_check)


llm_router = LLMRouter()