"""
claude_analyzer.py — Módulo de análise com Claude AI (Anthropic)
"""

import json
import anthropic
from config import Config


class ClaudeAnalyzer:
    """
    Usa o Claude da Anthropic para gerar análises textuais
    a partir dos dados brutos da API-Football.
    """

    MODEL = "claude-opus-4-5"
    MAX_TOKENS = 1500

    SYSTEM_PROMPT = """Você é um analista de futebol especializado com profundo conhecimento 
estatístico e tático. Seu papel é analisar dados brutos de partidas e temporadas de futebol 
e produzir análises claras, perspicazes e em português brasileiro.

Suas análises devem:
- Ser objetivas, baseadas exclusivamente nos dados fornecidos
- Destacar pontos fortes e fracos dos times/jogadores
- Identificar padrões e tendências relevantes
- Usar linguagem clara e acessível, mas profissional
- Ser estruturadas com tópicos quando necessário
- Evitar especulações sem base nos dados
- Ter entre 200 e 400 palavras, sendo direto e informativo

Sempre responda em português brasileiro."""

    def __init__(self):
        config = Config()
        api_key = config.ANTHROPIC_API_KEY
        if not api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY não encontrada!\n"
                "Configure no arquivo .env ou como variável de ambiente.\n"
                "Obtenha sua chave em: https://console.anthropic.com/"
            )
        self.client = anthropic.Anthropic(api_key=api_key)

    def _analyze(self, prompt: str) -> str:
        """Envia o prompt ao Claude e retorna a análise."""
        try:
            message = self.client.messages.create(
                model=self.MODEL,
                max_tokens=self.MAX_TOKENS,
                system=self.SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except anthropic.APIConnectionError:
            return "❌ Erro de conexão com a API da Anthropic."
        except anthropic.AuthenticationError:
            return "❌ Chave da API Anthropic inválida ou expirada."
        except anthropic.RateLimitError:
            return "❌ Limite de requisições da Anthropic excedido. Aguarde um momento."
        except Exception as e:
            return f"❌ Erro inesperado: {str(e)}"

    # ──────────────────────────────────────────────
    # ANÁLISE DE TIME
    # ──────────────────────────────────────────────

    def analyze_team(self, stats: dict, fixtures: list) -> str:
        """Gera análise estatística completa de um time."""

        team_name = stats.get("team", {}).get("name", "Time desconhecido")
        league_name = stats.get("league", {}).get("name", "Liga desconhecida")
        season = stats.get("league", {}).get("season", "N/A")

        form = stats.get("form", "N/A")
        fixtures_stat = stats.get("fixtures", {})
        goals = stats.get("goals", {})
        biggest = stats.get("biggest", {})
        cards = stats.get("cards", {})
        lineups = stats.get("lineups", [])

        # Processar resultados dos últimos jogos
        recent_results = []
        for f in fixtures[-5:]:
            fixture_info = f.get("fixture", {})
            teams = f.get("teams", {})
            score = f.get("score", {}).get("fulltime", {})
            home_team = teams.get("home", {}).get("name", "?")
            away_team = teams.get("away", {}).get("name", "?")
            home_goals = score.get("home", "?")
            away_goals = score.get("away", "?")
            recent_results.append(f"{home_team} {home_goals} x {away_goals} {away_team}")

        prompt = f"""Analise as seguintes estatísticas do time {team_name} na {league_name} {season}:

**FORMA ATUAL:** {form}

**RESULTADOS (Jogados/Vitórias/Empates/Derrotas):**
- Em casa: {fixtures_stat.get('wins', {}).get('home', 0)}V / {fixtures_stat.get('draws', {}).get('home', 0)}E / {fixtures_stat.get('loses', {}).get('home', 0)}D
- Fora: {fixtures_stat.get('wins', {}).get('away', 0)}V / {fixtures_stat.get('draws', {}).get('away', 0)}E / {fixtures_stat.get('loses', {}).get('away', 0)}D

**GOLS MARCADOS:**
- Total: {goals.get('for', {}).get('total', {}).get('total', 0)}
- Em casa: {goals.get('for', {}).get('total', {}).get('home', 0)}
- Fora: {goals.get('for', {}).get('total', {}).get('away', 0)}
- Média: {goals.get('for', {}).get('average', {}).get('total', 0)} por jogo

**GOLS SOFRIDOS:**
- Total: {goals.get('against', {}).get('total', {}).get('total', 0)}
- Em casa: {goals.get('against', {}).get('total', {}).get('home', 0)}
- Fora: {goals.get('against', {}).get('total', {}).get('away', 0)}

**MAIORES RESULTADOS:**
- Maior vitória em casa: {biggest.get('wins', {}).get('home', 'N/A')}
- Maior vitória fora: {biggest.get('wins', {}).get('away', 'N/A')}
- Maior derrota em casa: {biggest.get('loses', {}).get('home', 'N/A')}
- Maior derrota fora: {biggest.get('loses', {}).get('away', 'N/A')}

**ÚLTIMAS 5 PARTIDAS:**
{chr(10).join(recent_results) if recent_results else 'Dados indisponíveis'}

**ESQUEMA TÁTICO MAIS USADO:**
{lineups[0].get('formation', 'N/A') if lineups else 'N/A'}

Forneça uma análise completa e perspicaz deste time, identificando padrões de desempenho, pontos fortes, fraquezas e tendências."""

        return self._analyze(prompt)

    # ──────────────────────────────────────────────
    # ANÁLISE DE PARTIDA
    # ──────────────────────────────────────────────

    def analyze_match(self, fixture: dict, stats: list, events: list) -> str:
        """Gera análise de uma partida específica."""

        teams = fixture.get("teams", {})
        score = fixture.get("score", {})
        home = teams.get("home", {}).get("name", "Time A")
        away = teams.get("away", {}).get("name", "Time B")
        ht_score = score.get("halftime", {})
        ft_score = score.get("fulltime", {})

        # Formatar eventos
        goals = [e for e in events if e.get("type") == "Goal"]
        cards = [e for e in events if e.get("type") == "Card"]

        goal_texts = []
        for g in goals:
            team = g.get("team", {}).get("name", "?")
            player = g.get("player", {}).get("name", "?")
            minute = g.get("time", {}).get("elapsed", "?")
            goal_texts.append(f"  {minute}' - {player} ({team})")

        card_texts = []
        for c in cards:
            team = c.get("team", {}).get("name", "?")
            player = c.get("player", {}).get("name", "?")
            minute = c.get("time", {}).get("elapsed", "?")
            detail = c.get("detail", "Cartão")
            card_texts.append(f"  {minute}' - {detail}: {player} ({team})")

        # Formatar estatísticas
        stats_text = ""
        if stats and len(stats) >= 2:
            home_stats = {s["type"]: s["value"] for s in stats[0].get("statistics", [])}
            away_stats = {s["type"]: s["value"] for s in stats[1].get("statistics", [])}

            for key in ["Ball Possession", "Total Shots", "Shots on Goal", "Corner Kicks",
                        "Fouls", "Passes", "Pass Accuracy", "Offsides"]:
                h_val = home_stats.get(key, "N/A")
                a_val = away_stats.get(key, "N/A")
                stats_text += f"  {key}: {h_val} vs {a_val}\n"

        prompt = f"""Analise a seguinte partida de futebol:

**PLACAR:**
{home} {ft_score.get('home', '?')} x {ft_score.get('away', '?')} {away}
Intervalo: {ht_score.get('home', '?')} x {ht_score.get('away', '?')}

**GOLS:**
{chr(10).join(goal_texts) if goal_texts else '  Nenhum gol registrado'}

**CARTÕES:**
{chr(10).join(card_texts) if card_texts else '  Nenhum cartão'}

**ESTATÍSTICAS (Casa vs Fora):**
{stats_text if stats_text else '  Dados indisponíveis'}

Forneça uma análise detalhada desta partida: quem dominou o jogo, momentos-chave, desempenho individual, e o que os dados revelam sobre o desempenho das equipes."""

        return self._analyze(prompt)

    # ──────────────────────────────────────────────
    # ANÁLISE DE LIGA
    # ──────────────────────────────────────────────

    def analyze_league(self, standings: list, top_scorers: list) -> str:
        """Gera análise da classificação de uma liga."""

        group = standings[0] if standings else []
        top_teams = group[:5] if len(group) >= 5 else group

        standings_text = ""
        for t in top_teams:
            name = t.get("team", {}).get("name", "?")
            pts = t.get("points", 0)
            gd = t.get("goalsDiff", 0)
            played = t.get("all", {}).get("played", 0)
            form = t.get("form", "N/A")
            standings_text += f"  {t.get('rank', '?')}. {name} — {pts}pts | +{gd} DG | {played}J | Forma: {form}\n"

        scorers_text = ""
        for i, s in enumerate(top_scorers[:5], 1):
            player = s.get("player", {}).get("name", "?")
            team = s.get("statistics", [{}])[0].get("team", {}).get("name", "?")
            goals = s.get("statistics", [{}])[0].get("goals", {}).get("total", 0)
            scorers_text += f"  {i}. {player} ({team}) — {goals} gols\n"

        prompt = f"""Analise a classificação e desempenho desta liga de futebol:

**TOP 5 DA CLASSIFICAÇÃO:**
{standings_text}

**ARTILHEIROS:**
{scorers_text if scorers_text else '  Dados indisponíveis'}

Identifique: quem lidera com mais folga, quem está surpreendendo, disputas acirradas, times em queda/ascensão, e o que os números revelam sobre a temporada."""

        return self._analyze(prompt)

    # ──────────────────────────────────────────────
    # ANÁLISE DE JOGADOR
    # ──────────────────────────────────────────────

    def analyze_player(self, player_data: dict) -> str:
        """Gera análise das estatísticas de um jogador."""

        player = player_data.get("player", {})
        stats_list = player_data.get("statistics", [{}])
        stats = stats_list[0] if stats_list else {}

        name = player.get("name", "Jogador desconhecido")
        age = player.get("age", "N/A")
        nationality = player.get("nationality", "N/A")
        position = stats.get("games", {}).get("position", "N/A")
        team = stats.get("team", {}).get("name", "N/A")
        league = stats.get("league", {}).get("name", "N/A")

        games = stats.get("games", {})
        goals = stats.get("goals", {})
        passes = stats.get("passes", {})
        dribbles = stats.get("dribbles", {})
        tackles = stats.get("tackles", {})
        cards = stats.get("cards", {})
        shots = stats.get("shots", {})

        prompt = f"""Analise as estatísticas do jogador de futebol {name}:

**PERFIL:**
- Idade: {age} | Nacionalidade: {nationality}
- Posição: {position} | Time: {team} | Liga: {league}

**PARTICIPAÇÃO:**
- Jogos: {games.get('appearences', 0)} | Minutos: {games.get('minutes', 0)}
- Avaliação média: {games.get('rating', 'N/A')}

**CONTRIBUIÇÕES OFENSIVAS:**
- Gols: {goals.get('total', 0)} | Assistências: {goals.get('assists', 0)}
- Chutes: {shots.get('total', 0)} | No alvo: {shots.get('on', 0)}

**CRIAÇÃO DE JOGO:**
- Passes: {passes.get('total', 0)} | Precisão: {passes.get('accuracy', 0)}%
- Dribles tentados: {dribbles.get('attempts', 0)} | Bem-sucedidos: {dribbles.get('success', 0)}

**DEFENSIVO:**
- Desarmes: {tackles.get('total', 0)} | Interceptações: {tackles.get('interceptions', 0)}

**DISCIPLINA:**
- Amarelos: {cards.get('yellow', 0)} | Vermelhos: {cards.get('red', 0)}

Avalie o desempenho geral deste jogador na temporada: pontos fortes, áreas de melhoria, impacto no jogo e comparação com o esperado para sua posição."""

        return self._analyze(prompt)

    # ──────────────────────────────────────────────
    # ANÁLISE H2H
    # ──────────────────────────────────────────────

    def analyze_h2h(self, fixtures: list) -> str:
        """Gera análise do histórico de confrontos entre dois times."""

        if not fixtures:
            return "Sem dados de confrontos disponíveis para análise."

        results = []
        for f in fixtures:
            teams = f.get("teams", {})
            score = f.get("score", {}).get("fulltime", {})
            date = f.get("fixture", {}).get("date", "")[:10]
            home = teams.get("home", {}).get("name", "?")
            away = teams.get("away", {}).get("name", "?")
            hg = score.get("home", "?")
            ag = score.get("away", "?")
            results.append(f"  {date}: {home} {hg} x {ag} {away}")

        team1 = fixtures[0].get("teams", {}).get("home", {}).get("name", "Time 1")
        team2 = fixtures[0].get("teams", {}).get("away", {}).get("name", "Time 2")

        prompt = f"""Analise o histórico de confrontos entre {team1} e {team2}:

**ÚLTIMOS CONFRONTOS:**
{chr(10).join(results)}

Com base nestes dados, analise: qual time leva vantagem histórica, padrões de placar, tendências recentes, e o que esperar de um próximo confronto entre essas equipes."""

        return self._analyze(prompt)
