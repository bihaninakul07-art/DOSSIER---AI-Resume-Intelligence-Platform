"""Single unified entrypoint for every LLM call in the app.

Agents call `llm_router.generate(task=..., prompt=...)` and never touch a
provider client directly. NVIDIA NIM is tried first for every task; if
it's unavailable (no key, or the call fails) the router automatically
falls back to Groq. Nothing in the agents needs to know which provider
actually served the request.
"""
import logging
from dataclasses import dataclass
from typing import Optional

from app.llm.base import LLMClient
from app.llm.nvidia_client import NvidiaNimClient
from app.llm.groq_client import GroqClient

logger = logging.getLogger(__name__)

PROVIDER_ORDER = ["nvidia_nim", "groq"]


@dataclass
class LLMResult:
    text: str
    provider_used: str
    cross_check: Optional[dict] = None


class LLMRouter:
    def __init__(self):
        self._clients: dict[str, LLMClient] = {
            "nvidia_nim": NvidiaNimClient(),
            "groq": GroqClient(),
        }

    def _candidates(self) -> list[LLMClient]:
        return [self._clients[p] for p in PROVIDER_ORDER if self._clients.get(p)]

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
        candidates = [c for c in self._candidates() if getattr(c, "available", False)]
        if not candidates:
            raise RuntimeError(
                "No LLM provider configured. Set NVIDIA_NIM_API_KEY and/or GROQ_API_KEY."
            )

        last_error = None
        primary_result = None
        for client in candidates:
            try:
                text = await client.generate(
                    prompt, system=system, json_mode=json_mode,
                    temperature=temperature, max_tokens=max_tokens,
                )
                primary_result = LLMResult(text=text, provider_used=client.name)
                break
            except Exception as e:
                last_error = e
                logger.warning("Provider %s failed for task=%s: %s; trying fallback", client.name, task, e)

        if primary_result is None:
            raise RuntimeError(f"All LLM providers failed for task={task}: {last_error}")

        if cross_validate:
            others = [c for c in candidates if c.name != primary_result.provider_used]
            if others:
                try:
                    alt_text = await others[0].generate(
                        prompt, system=system, json_mode=json_mode,
                        temperature=temperature, max_tokens=max_tokens,
                    )
                    primary_result.cross_check = {"provider": others[0].name, "text": alt_text}
                except Exception as e:
                    logger.warning("Cross-validation call failed: %s", e)

        return primary_result


llm_router = LLMRouter()
