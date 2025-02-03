from abc import ABC, abstractmethod

from openai import AsyncOpenAI
from fastapi import HTTPException

from .constants import mock_response


class AIDriver:
    @abstractmethod
    async def generate_text(self, prompt: str, role: str = "assistant") -> str:
        pass


class MockAIDriver(AIDriver):
    async def generate_text(self, prompt: str, role: str = "assistant") -> str:
        return mock_response


# class OpenAIDriver(AIDriver):
#     def __init__(self, api_key, model="o1-mini"):
#         self._client = AsyncOpenAI(api_key=api_key)
#         self._model = model
#
#     async def generate_text(self, prompt: str, role: str = "assistant") -> str:
#         completion = await self._client.chat.completions.create(
#             model=self._model,
#             messages=[{
#                 "role": role,
#                 "content": prompt,
#             }],
#         )
#         return completion.choices[0].message.content


class AIClient:
    def __init__(self, driver: AIDriver):
        self._driver = driver

    async def generate_text(self, prompt, role: str = "assistant") -> str:
        return await self._driver.generate_text(prompt, role)