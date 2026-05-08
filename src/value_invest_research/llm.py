from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from openai import OpenAI
except ModuleNotFoundError:
    OpenAI = None  # type: ignore[assignment]


@dataclass(frozen=True)
class LlmConfig:
    api_key: str
    base_url: str
    model: str
    max_tokens: int = 4096
    temperature: float = 0.3

    @classmethod
    def from_env(cls) -> "LlmConfig":
        return cls(
            api_key=os.environ.get("LLM_API_KEY", ""),
            base_url=os.environ.get("LLM_BASE_URL", "https://api.z.ai/api/coding/paas/v4"),
            model=os.environ.get("LLM_MODEL", "glm-5.1"),
        )


class LlmClient:
    def __init__(self, config: LlmConfig) -> None:
        if OpenAI is None:
            raise RuntimeError("openai package is required for LLM workflows; install value-invest-research[llm]")
        self._config = config
        self._client = OpenAI(api_key=config.api_key, base_url=config.base_url)

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        resp = self._client.chat.completions.create(
            model=self._config.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=self._config.max_tokens,
            temperature=self._config.temperature,
        )
        return resp.choices[0].message.content or ""

    def chat_with_context(self, messages: list[dict[str, str]]) -> str:
        resp = self._client.chat.completions.create(
            model=self._config.model,
            messages=messages,
            max_tokens=self._config.max_tokens,
            temperature=self._config.temperature,
        )
        return resp.choices[0].message.content or ""
