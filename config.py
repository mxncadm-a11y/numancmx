"""
config.py — Gerenciamento de configuração e variáveis de ambiente
"""

import os
from pathlib import Path


def load_dotenv(env_path: str = ".env"):
    """Carrega variáveis de ambiente de um arquivo .env manualmente."""
    env_file = Path(env_path)
    if not env_file.exists():
        return

    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


class Config:
    """Centraliza configurações do projeto."""

    def __init__(self):
        load_dotenv()

    @property
    def ANTHROPIC_API_KEY(self) -> str:
        return os.getenv("ANTHROPIC_API_KEY", "")

    @property
    def FOOTBALL_API_KEY(self) -> str:
        return os.getenv("FOOTBALL_API_KEY", "")

    @property
    def USE_RAPIDAPI(self) -> bool:
        """True = usa RapidAPI, False = usa API direta (api-sports.io)."""
        val = os.getenv("USE_RAPIDAPI", "false").lower()
        return val in ("true", "1", "yes")

    def validate(self) -> list:
        """Retorna lista de erros de configuração."""
        errors = []
        if not self.ANTHROPIC_API_KEY:
            errors.append("ANTHROPIC_API_KEY não configurada")
        if not self.FOOTBALL_API_KEY:
            errors.append("FOOTBALL_API_KEY não configurada")
        return errors
