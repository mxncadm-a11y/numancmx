"""
football_api.py — Wrapper para a API-Football (api-football.com)
Documentação: https://www.api-football.com/documentation-v3
"""

import os
import requests
from typing import Optional
from config import Config


class FootballAPI:
    """
    Cliente para a API-Football (via RapidAPI ou acesso direto).
    Suporta ambos os modos: RapidAPI e API direta.
    """

    BASE_URL_RAPID = "https://api-football-v1.p.rapidapi.com/v3"
    BASE_URL_DIRECT = "https://v3.football.api-sports.io"

    def __init__(self):
        self.config = Config()
        self.api_key = self.config.FOOTBALL_API_KEY
        self.use_rapid = self.config.USE_RAPIDAPI

        if not self.api_key:
            raise ValueError(
                "❌ FOOTBALL_API_KEY não encontrada!\n"
                "Configure no arquivo .env ou como variável de ambiente.\n"
                "Obtenha sua chave em: https://www.api-football.com/"
            )

        if self.use_rapid:
            self.base_url = self.BASE_URL_RAPID
            self.headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
            }
        else:
            self.base_url = self.BASE_URL_DIRECT
            self.headers = {
                "x-apisports-key": self.api_key
            }

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Executa requisição GET e retorna os dados."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if "errors" in data and data["errors"]:
                errors = data["errors"]
                raise ValueError(f"Erro da API: {errors}")

            return data.get("response", [])

        except requests.exceptions.ConnectionError:
            raise ConnectionError("❌ Sem conexão com a internet. Verifique sua rede.")
        except requests.exceptions.Timeout:
            raise TimeoutError("❌ Tempo de resposta da API esgotado. Tente novamente.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise PermissionError("❌ API Key inválida ou expirada.")
            elif e.response.status_code == 429:
                raise Exception("❌ Limite de requisições excedido. Aguarde um momento.")
            raise

    # ──────────────────────────────────────────────
    # TIMES
    # ──────────────────────────────────────────────

    def search_team(self, name: str) -> list:
        """Busca times pelo nome."""
        return self._get("teams", {"search": name})

    def get_team_info(self, team_id: int) -> dict:
        """Retorna informações de um time pelo ID."""
        results = self._get("teams", {"id": team_id})
        return results[0] if results else {}

    def get_team_statistics(self, team_id: int, league_id: int, season: int) -> dict:
        """Retorna estatísticas completas de um time em uma liga/temporada."""
        results = self._get("teams/statistics", {
            "team": team_id,
            "league": league_id,
            "season": season
        })
        return results if isinstance(results, dict) else {}

    def get_team_fixtures(self, team_id: int, season: int, last: int = 10) -> list:
        """Retorna os últimos N jogos de um time."""
        return self._get("fixtures", {
            "team": team_id,
            "season": season,
            "last": last
        })

    # ──────────────────────────────────────────────
    # PARTIDAS
    # ──────────────────────────────────────────────

    def get_fixture(self, fixture_id: int) -> dict:
        """Retorna dados de uma partida específica."""
        results = self._get("fixtures", {"id": fixture_id})
        return results[0] if results else {}

    def get_fixture_statistics(self, fixture_id: int) -> list:
        """Retorna estatísticas detalhadas de uma partida."""
        return self._get("fixtures/statistics", {"fixture": fixture_id})

    def get_fixture_events(self, fixture_id: int) -> list:
        """Retorna eventos (gols, cartões, substituições) de uma partida."""
        return self._get("fixtures/events", {"fixture": fixture_id})

    def get_fixture_lineups(self, fixture_id: int) -> list:
        """Retorna as escalações de uma partida."""
        return self._get("fixtures/lineups", {"fixture": fixture_id})

    def get_live_fixtures(self, league_id: Optional[int] = None) -> list:
        """Retorna partidas ao vivo."""
        params = {"live": "all"}
        if league_id:
            params["league"] = league_id
        return self._get("fixtures", params)

    # ──────────────────────────────────────────────
    # LIGAS
    # ──────────────────────────────────────────────

    def get_standings(self, league_id: int, season: int) -> list:
        """Retorna a classificação de uma liga."""
        results = self._get("standings", {
            "league": league_id,
            "season": season
        })
        if results and "league" in results[0]:
            return results[0]["league"]["standings"]
        return []

    def get_top_scorers(self, league_id: int, season: int) -> list:
        """Retorna os maiores artilheiros de uma liga."""
        return self._get("players/topscorers", {
            "league": league_id,
            "season": season
        })

    def get_top_assists(self, league_id: int, season: int) -> list:
        """Retorna os jogadores com mais assistências."""
        return self._get("players/topassists", {
            "league": league_id,
            "season": season
        })

    def search_league(self, name: str) -> list:
        """Busca ligas pelo nome."""
        return self._get("leagues", {"search": name})

    # ──────────────────────────────────────────────
    # JOGADORES
    # ──────────────────────────────────────────────

    def get_player_statistics(self, player_id: int, season: int) -> dict:
        """Retorna estatísticas de um jogador em uma temporada."""
        results = self._get("players", {
            "id": player_id,
            "season": season
        })
        return results[0] if results else {}

    def search_player(self, name: str, team_id: Optional[int] = None) -> list:
        """Busca jogadores pelo nome."""
        params = {"search": name}
        if team_id:
            params["team"] = team_id
        return self._get("players", params)

    # ──────────────────────────────────────────────
    # CONFRONTOS
    # ──────────────────────────────────────────────

    def get_head_to_head(self, team1_id: int, team2_id: int, last: int = 10) -> list:
        """Retorna histórico de confrontos entre dois times."""
        return self._get("fixtures/headtohead", {
            "h2h": f"{team1_id}-{team2_id}",
            "last": last
        })

    # ──────────────────────────────────────────────
    # LIGAS POPULARES (IDs de referência)
    # ──────────────────────────────────────────────

    POPULAR_LEAGUES = {
        "Brasileirão Série A": 71,
        "Brasileirão Série B": 72,
        "Copa do Brasil": 73,
        "Copa Libertadores": 13,
        "Copa Sul-Americana": 11,
        "Premier League": 39,
        "La Liga": 140,
        "Bundesliga": 78,
        "Serie A (ITA)": 135,
        "Ligue 1": 61,
        "Champions League": 2,
        "Europa League": 3,
        "MLS": 253,
    }
