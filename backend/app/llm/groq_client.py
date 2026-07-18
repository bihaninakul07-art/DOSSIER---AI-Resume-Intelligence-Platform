import os
from typing import Optional

from groq import AsyncGroq

from app.llm.base import LLMClient


class GroqClient(LLMClient):
    """Fast inference provider - used for parsing / extraction tasks."""

    name = "groq"

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self._client = AsyncGroq(api_key=api_key) if api_key else None
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    @property
    def available(self) -> bool:
        return self._client is not None

    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        json_mode: bool = False,
        temperature: float = 0.4,
        max_tokens: int = 2000,
    ) -> str:
        if not self._client:
            raise RuntimeError("GROQ_API_KEY not configured")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        resp = await self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        return resp.choices[0].message.content or ""
