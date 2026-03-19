"""
display.py — Módulo de exibição com Rich para terminal estilizado
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.rule import Rule
from rich import box


class Display:
    """Responsável por renderizar dados no terminal com Rich."""

    def __init__(self, console: Console):
        self.console = console

    # ──────────────────────────────────────────────
    # ANÁLISE DE TIME
    # ──────────────────────────────────────────────

    def show_team_stats(self, stats: dict, fixtures: list):
        """Exibe estatísticas de um time."""
        if not stats:
            self.console.print("[red]Sem dados disponíveis para este time.[/red]")
            return

        team = stats.get("team", {})
        league = stats.get("league", {})
        form_str = stats.get("form", "")
        fixture_stats = stats.get("fixtures", {})
        goals = stats.get("goals", {})
        lineups = stats.get("lineups", [])

        # Header
        self.console.print(Rule(f"[bold green]{team.get('name', 'Time')}[/bold green]", style="green"))
        self.console.print(f"[dim]Liga: {league.get('name')} | Temporada: {league.get('season')}[/dim]\n")

        # Forma
        form_display = self._format_form(form_str)
        self.console.print(f"Forma recente: {form_display}\n")

        # Tabela de resultados
        results_table = Table(title="📊 Resultados", box=box.ROUNDED, style="cyan")
        results_table.add_column("Local", style="bold")
        results_table.add_column("Jogos", justify="center")
        results_table.add_column("V", justify="center", style="green")
        results_table.add_column("E", justify="center", style="yellow")
        results_table.add_column("D", justify="center", style="red")

        for location in ["home", "away", "total"]:
            label = {"home": "🏠 Casa", "away": "✈️ Fora", "total": "📈 Total"}[location]
            results_table.add_row(
                label,
                str(fixture_stats.get("played", {}).get(location, 0)),
                str(fixture_stats.get("wins", {}).get(location, 0)),
                str(fixture_stats.get("draws", {}).get(location, 0)),
                str(fixture_stats.get("loses", {}).get(location, 0)),
            )

        # Tabela de gols
        goals_table = Table(title="⚽ Gols", box=box.ROUNDED, style="yellow")
        goals_table.add_column("Tipo", style="bold")
        goals_table.add_column("Casa", justify="center")
        goals_table.add_column("Fora", justify="center")
        goals_table.add_column("Total", justify="center")
        goals_table.add_column("Média", justify="center")

        goals_table.add_row(
            "Marcados",
            str(goals.get("for", {}).get("total", {}).get("home", 0)),
            str(goals.get("for", {}).get("total", {}).get("away", 0)),
            str(goals.get("for", {}).get("total", {}).get("total", 0)),
            str(goals.get("for", {}).get("average", {}).get("total", 0)),
        )
        goals_table.add_row(
            "Sofridos",
            str(goals.get("against", {}).get("total", {}).get("home", 0)),
            str(goals.get("against", {}).get("total", {}).get("away", 0)),
            str(goals.get("against", {}).get("total", {}).get("total", 0)),
            str(goals.get("against", {}).get("average", {}).get("total", 0)),
        )

        self.console.print(Columns([results_table, goals_table]))

        # Esquema tático
        if lineups:
            top_lineup = lineups[0]
            self.console.print(f"\n🎯 Esquema mais usado: [bold]{top_lineup.get('formation', 'N/A')}[/bold] "
                               f"({top_lineup.get('played', 0)} jogos)")

        # Últimos jogos
        if fixtures:
            self.console.print(Rule("[bold]Últimas Partidas[/bold]", style="dim"))
            recent_table = Table(box=box.SIMPLE, show_header=True)
            recent_table.add_column("Data", style="dim")
            recent_table.add_column("Partida")
            recent_table.add_column("Placar", justify="center")

            for f in fixtures[-5:]:
                fixture_info = f.get("fixture", {})
                teams = f.get("teams", {})
                score = f.get("score", {}).get("fulltime", {})
                date = fixture_info.get("date", "")[:10]
                home_name = teams.get("home", {}).get("name", "?")
                away_name = teams.get("away", {}).get("name", "?")
                hg = score.get("home", "?")
                ag = score.get("away", "?")
                matchup = f"{home_name} vs {away_name}"
                score_str = f"[bold]{hg} x {ag}[/bold]"
                recent_table.add_row(date, matchup, score_str)

            self.console.print(recent_table)

    # ──────────────────────────────────────────────
    # ANÁLISE DE PARTIDA
    # ──────────────────────────────────────────────

    def show_match_stats(self, fixture: dict, stats: list, events: list):
        """Exibe dados de uma partida."""
        if not fixture:
            self.console.print("[red]Partida não encontrada.[/red]")
            return

        teams = fixture.get("teams", {})
        score = fixture.get("score", {})
        league = fixture.get("league", {})
        fixture_info = fixture.get("fixture", {})

        home = teams.get("home", {}).get("name", "Time A")
        away = teams.get("away", {}).get("name", "Time B")
        ft = score.get("fulltime", {})
        ht = score.get("halftime", {})
        date = fixture_info.get("date", "")[:10]
        venue = fixture_info.get("venue", {}).get("name", "N/A")
        status = fixture_info.get("status", {}).get("long", "N/A")

        self.console.print(Rule(f"[bold green]{home} vs {away}[/bold green]", style="green"))
        self.console.print(f"[dim]{league.get('name')} | {date} | {venue}[/dim]")
        self.console.print(f"[dim]Status: {status}[/dim]\n")

        # Placar
        score_text = Text()
        score_text.append(f"{home}  ", style="bold cyan")
        score_text.append(f"{ft.get('home', '?')} x {ft.get('away', '?')}", style="bold white on dark_green")
        score_text.append(f"  {away}", style="bold cyan")
        self.console.print(Panel(score_text, subtitle=f"Intervalo: {ht.get('home','?')}-{ht.get('away','?')}"))

        # Eventos
        goals = [e for e in events if e.get("type") == "Goal"]
        cards = [e for e in events if e.get("type") == "Card"]

        if goals:
            self.console.print("\n[bold]⚽ Gols:[/bold]")
            for g in goals:
                minute = g.get("time", {}).get("elapsed", "?")
                player = g.get("player", {}).get("name", "?")
                team = g.get("team", {}).get("name", "?")
                assist = g.get("assist", {}).get("name")
                assist_str = f" (assist: {assist})" if assist else ""
                self.console.print(f"  {minute}' [green]●[/green] {player} ({team}){assist_str}")

        if cards:
            self.console.print("\n[bold]🟨 Cartões:[/bold]")
            for c in cards:
                minute = c.get("time", {}).get("elapsed", "?")
                player = c.get("player", {}).get("name", "?")
                team = c.get("team", {}).get("name", "?")
                detail = c.get("detail", "Cartão")
                color = "yellow" if "Yellow" in detail else "red"
                self.console.print(f"  {minute}' [{color}]■[/{color}] {player} ({team}) — {detail}")

        # Estatísticas comparativas
        if stats and len(stats) >= 2:
            stat_table = Table(title="📊 Estatísticas da Partida", box=box.ROUNDED)
            stat_table.add_column(home, justify="right", style="cyan")
            stat_table.add_column("Métrica", justify="center", style="bold")
            stat_table.add_column(away, justify="left", style="magenta")

            home_stats = {s["type"]: s["value"] for s in stats[0].get("statistics", [])}
            away_stats = {s["type"]: s["value"] for s in stats[1].get("statistics", [])}

            keys = [
                "Ball Possession", "Total Shots", "Shots on Goal",
                "Shots off Goal", "Corner Kicks", "Fouls",
                "Yellow Cards", "Red Cards", "Passes", "Pass Accuracy"
            ]
            for key in keys:
                h_val = str(home_stats.get(key, "–"))
                a_val = str(away_stats.get(key, "–"))
                stat_table.add_row(h_val, key, a_val)

            self.console.print(f"\n{stat_table}")

    # ──────────────────────────────────────────────
    # CLASSIFICAÇÃO DE LIGA
    # ──────────────────────────────────────────────

    def show_league_standings(self, standings: list, top_scorers: list):
        """Exibe a classificação de uma liga."""
        if not standings or not standings[0]:
            self.console.print("[red]Dados de classificação não disponíveis.[/red]")
            return

        group = standings[0]

        table = Table(title="🏆 Classificação", box=box.ROUNDED, show_lines=True)
        table.add_column("#", justify="center", style="bold")
        table.add_column("Time", style="bold")
        table.add_column("P", justify="center", style="bold yellow")
        table.add_column("J", justify="center")
        table.add_column("V", justify="center", style="green")
        table.add_column("E", justify="center")
        table.add_column("D", justify="center", style="red")
        table.add_column("GF", justify="center")
        table.add_column("GC", justify="center")
        table.add_column("SG", justify="center")
        table.add_column("Forma", justify="center")

        for t in group:
            rank = t.get("rank", "?")
            name = t.get("team", {}).get("name", "?")
            pts = str(t.get("points", 0))
            played = str(t.get("all", {}).get("played", 0))
            win = str(t.get("all", {}).get("win", 0))
            draw = str(t.get("all", {}).get("draw", 0))
            lose = str(t.get("all", {}).get("lose", 0))
            gf = str(t.get("all", {}).get("goals", {}).get("for", 0))
            gc = str(t.get("all", {}).get("goals", {}).get("against", 0))
            gd = str(t.get("goalsDiff", 0))
            form = self._format_form(t.get("form", ""), max_chars=5)

            table.add_row(str(rank), name, pts, played, win, draw, lose, gf, gc, gd, form)

        self.console.print(table)

        if top_scorers:
            scorer_table = Table(title="🥇 Artilheiros", box=box.SIMPLE)
            scorer_table.add_column("#", justify="center")
            scorer_table.add_column("Jogador")
            scorer_table.add_column("Time")
            scorer_table.add_column("Gols", justify="center", style="bold green")
            scorer_table.add_column("Assist.", justify="center")

            for i, s in enumerate(top_scorers[:10], 1):
                player = s.get("player", {}).get("name", "?")
                team = s.get("statistics", [{}])[0].get("team", {}).get("name", "?")
                goals = str(s.get("statistics", [{}])[0].get("goals", {}).get("total", 0))
                assists = str(s.get("statistics", [{}])[0].get("goals", {}).get("assists", 0))
                scorer_table.add_row(str(i), player, team, goals, assists)

            self.console.print(f"\n{scorer_table}")

    # ──────────────────────────────────────────────
    # JOGADOR
    # ──────────────────────────────────────────────

    def show_player_stats(self, player_data: dict):
        """Exibe estatísticas de um jogador."""
        if not player_data:
            self.console.print("[red]Jogador não encontrado.[/red]")
            return

        player = player_data.get("player", {})
        stats_list = player_data.get("statistics", [{}])
        stats = stats_list[0] if stats_list else {}

        name = player.get("name", "?")
        age = player.get("age", "?")
        nationality = player.get("nationality", "?")
        height = player.get("height", "?")
        weight = player.get("weight", "?")

        self.console.print(Rule(f"[bold cyan]{name}[/bold cyan]", style="cyan"))
        self.console.print(f"Idade: {age} | Nacionalidade: {nationality} | Altura: {height} | Peso: {weight}")
        self.console.print(f"Time: [bold]{stats.get('team', {}).get('name', '?')}[/bold] | "
                           f"Liga: {stats.get('league', {}).get('name', '?')}\n")

        games = stats.get("games", {})
        goals = stats.get("goals", {})
        shots = stats.get("shots", {})
        passes = stats.get("passes", {})
        dribbles = stats.get("dribbles", {})
        tackles = stats.get("tackles", {})
        cards = stats.get("cards", {})

        stat_table = Table(box=box.ROUNDED)
        stat_table.add_column("Categoria", style="bold")
        stat_table.add_column("Valor", justify="center")

        stat_table.add_section()
        stat_table.add_row("🎮 Partidas", str(games.get("appearences", 0)))
        stat_table.add_row("⏱ Minutos", str(games.get("minutes", 0)))
        stat_table.add_row("⭐ Rating", str(games.get("rating", "N/A")))

        stat_table.add_section()
        stat_table.add_row("⚽ Gols", str(goals.get("total", 0)))
        stat_table.add_row("🎯 Assistências", str(goals.get("assists", 0)))
        stat_table.add_row("🔫 Chutes", str(shots.get("total", 0)))
        stat_table.add_row("🎯 No Alvo", str(shots.get("on", 0)))

        stat_table.add_section()
        stat_table.add_row("📤 Passes", str(passes.get("total", 0)))
        stat_table.add_row("🎯 Precisão", f"{passes.get('accuracy', 0)}%")
        stat_table.add_row("🏃 Dribles (tent.)", str(dribbles.get("attempts", 0)))
        stat_table.add_row("✅ Dribles (ok)", str(dribbles.get("success", 0)))

        stat_table.add_section()
        stat_table.add_row("🛡️ Desarmes", str(tackles.get("total", 0)))
        stat_table.add_row("✋ Intercep.", str(tackles.get("interceptions", 0)))

        stat_table.add_section()
        stat_table.add_row("🟨 Amarelos", str(cards.get("yellow", 0)))
        stat_table.add_row("🟥 Vermelhos", str(cards.get("red", 0)))

        self.console.print(stat_table)

    # ──────────────────────────────────────────────
    # H2H
    # ──────────────────────────────────────────────

    def show_h2h(self, fixtures: list):
        """Exibe histórico de confrontos."""
        if not fixtures:
            self.console.print("[red]Sem histórico de confrontos.[/red]")
            return

        self.console.print(Rule("[bold]⚔️ Histórico de Confrontos[/bold]"))
        table = Table(box=box.SIMPLE, show_header=True)
        table.add_column("Data", style="dim")
        table.add_column("Liga")
        table.add_column("Casa", style="cyan")
        table.add_column("Placar", justify="center", style="bold")
        table.add_column("Fora", style="magenta")

        for f in fixtures:
            teams = f.get("teams", {})
            score = f.get("score", {}).get("fulltime", {})
            date = f.get("fixture", {}).get("date", "")[:10]
            league = f.get("league", {}).get("name", "?")
            home = teams.get("home", {}).get("name", "?")
            away = teams.get("away", {}).get("name", "?")
            hg = score.get("home", "?")
            ag = score.get("away", "?")
            table.add_row(date, league, home, f"{hg} x {ag}", away)

        self.console.print(table)

    # ──────────────────────────────────────────────
    # BUSCA DE TIMES
    # ──────────────────────────────────────────────

    def show_team_search_results(self, teams: list):
        """Exibe resultados de busca de times."""
        if not teams:
            self.console.print("[red]Nenhum time encontrado.[/red]")
            return

        table = Table(title="🔍 Times Encontrados", box=box.ROUNDED)
        table.add_column("ID", justify="center", style="bold yellow")
        table.add_column("Nome")
        table.add_column("País")
        table.add_column("Fundado", justify="center")

        for t in teams:
            team = t.get("team", {})
            table.add_row(
                str(team.get("id", "?")),
                team.get("name", "?"),
                team.get("country", "?"),
                str(team.get("founded", "?"))
            )

        self.console.print(table)
        self.console.print("[dim]Use o ID acima com: python main.py team --id <ID>[/dim]")

    # ──────────────────────────────────────────────
    # ANÁLISE IA
    # ──────────────────────────────────────────────

    def show_ai_analysis(self, analysis: str, title: str = "🤖 Análise IA"):
        """Exibe a análise gerada pelo Claude."""
        self.console.print()
        self.console.print(Panel(
            analysis,
            title=f"[bold magenta]{title}[/bold magenta]",
            border_style="magenta",
            padding=(1, 2)
        ))

    # ──────────────────────────────────────────────
    # HELPERS
    # ──────────────────────────────────────────────

    def _format_form(self, form_str: str, max_chars: int = 10) -> str:
        """Formata string de forma com cores."""
        form_str = form_str[-max_chars:] if len(form_str) > max_chars else form_str
        result = ""
        for char in form_str:
            if char == "W":
                result += "[green]W[/green]"
            elif char == "D":
                result += "[yellow]D[/yellow]"
            elif char == "L":
                result += "[red]L[/red]"
            else:
                result += char
        return result
