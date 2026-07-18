"""NVIDIA NIM client for LLM inference (OpenAI-compatible API)."""
import os
from typing import Optional

import httpx

from app.llm.base import LLMClient


class NvidiaNimClient(LLMClient):
    """NVIDIA NIM LLM client - OpenAI-compatible API for models like Nemotron, Llama, Mixtral."""

    name = "nvidia_nim"

    def __init__(self):
        api_key = os.getenv("NVIDIA_NIM_API_KEY")
        # Use default NVIDIA NIM endpoint (integrate.api.nvidia.com/v1)
        base_url = "https://integrate.api.nvidia.com/v1"
        self.model = os.getenv("NVIDIA_NIM_MODEL", "nvidia/nemotron-3-ultra")
        self._client = None
        if api_key:
            self._client = httpx.AsyncClient(
                base_url=base_url,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=120.0,
            )

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
            raise RuntimeError("NVIDIA_NIM_API_KEY not configured")

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        resp = await self._client.post("/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"] or ""

    async def close(self):
        if self._client:
            await self._client.aclose()


class NvidiaNimImageClient:
    """NVIDIA NIM client for image generation (FLUX, Stable Diffusion via NIM)."""

    def __init__(self):
        api_key = os.getenv("NVIDIA_NIM_API_KEY")
        # Use default NVIDIA NIM endpoint (ai.api.nvidia.com/v1/genai)
        base_url = "https://ai.api.nvidia.com/v1/genai"
        self.model = os.getenv("NVIDIA_NIM_IMAGE_MODEL", "black-forest-labs/flux.1-schnell")
        self._client = None
        if api_key:
            self._client = httpx.AsyncClient(
                base_url=base_url,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=180.0,
            )

    @property
    def available(self) -> bool:
        return self._client is not None

    async def generate(self, prompt: str) -> str | None:
        """Generate image and return base64 data URI."""
        if not self._client:
            return None

        payload = {
            "model": self.model,
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "steps": 4,
            "guidance_scale": 0.0,
            "n": 1,
            "response_format": "b64_json",
        }

        try:
            resp = await self._client.post("/images/generations", json=payload)
            resp.raise_for_status()
            data = resp.json()
            b64 = data["data"][0]["b64_json"]
            return f"data:image/png;base64,{b64}"
        except Exception as e:
            import logging
            logging.warning(f"NVIDIA NIM image generation failed: {e}")
            return None

    async def close(self):
        if self._client:
            await self._client.aclose()