"""Common interface every LLM provider client must implement.

Agents never talk to a provider directly - they only ever call
`llm_router.generate(...)`. This file defines the contract that
keeps every provider swappable behind that single call site.
"""
from abc import ABC, abstractmethod
from typing import Optional


class LLMClient(ABC):
    """Abstract base for a single LLM provider."""

    name: str = "base"

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        json_mode: bool = False,
        temperature: float = 0.4,
        max_tokens: int = 2000,
    ) -> str:
        """Return the raw text (or JSON string) completion for a prompt."""
        raise NotImplementedError
