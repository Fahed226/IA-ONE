"""Accès à Claude avec sorties structurées (validées par Pydantic)."""

from __future__ import annotations

import os
from typing import Protocol, TypeVar

import anthropic
from pydantic import BaseModel

from .prompts import SYSTEM_PROMPT

T = TypeVar("T", bound=BaseModel)

DEFAULT_MODEL = os.environ.get("FORMATION_MODEL", "claude-opus-5")
DEFAULT_EFFORT = os.environ.get("FORMATION_EFFORT", "high")


class GenerationError(RuntimeError):
    pass


class StructuredLLM(Protocol):
    def generate(self, prompt: str, schema: type[T]) -> T: ...


class ClaudeLLM:
    """Client Claude : streaming (sorties longues) + format JSON garanti par schéma."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        effort: str = DEFAULT_EFFORT,
        max_tokens: int = 64000,
        client: anthropic.Anthropic | None = None,
    ) -> None:
        self.model = model
        self.effort = effort
        self.max_tokens = max_tokens
        self.client = client or anthropic.Anthropic(max_retries=4)

    def generate(self, prompt: str, schema: type[T]) -> T:
        try:
            with self.client.beta.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                # Le prompt système est identique pour tous les appels : on le met en cache.
                system=[{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": prompt}],
                thinking={"type": "adaptive"},
                output_config={"effort": self.effort},
                output_format=schema,
                # En cas de refus d'un classifieur de sécurité, l'API rejoue sur un modèle de repli.
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            ) as stream:
                message = stream.get_final_message()
        except anthropic.AuthenticationError as exc:
            raise GenerationError("Clé API Anthropic invalide ou absente (ANTHROPIC_API_KEY).") from exc
        except anthropic.RateLimitError as exc:
            raise GenerationError("Limite de débit de l'API atteinte, réessayez plus tard.") from exc
        except anthropic.APIStatusError as exc:
            raise GenerationError(f"Erreur API ({exc.status_code}) : {exc.message}") from exc
        except anthropic.APIConnectionError as exc:
            raise GenerationError("Impossible de joindre l'API Anthropic.") from exc

        if message.stop_reason == "refusal":
            raise GenerationError("Le modèle a refusé de générer ce contenu.")
        if message.stop_reason == "max_tokens":
            raise GenerationError("Réponse tronquée (max_tokens atteint) : réduisez la taille demandée.")
        parsed = message.parsed_output
        if parsed is None:
            raise GenerationError("Réponse du modèle impossible à interpréter.")
        return parsed
