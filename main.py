#!/usr/bin/env python3
"""
⚽ Football Stats Analyzer — Powered by API-Football + Claude AI
"""

import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from football_api import FootballAPI
from claude_analyzer import ClaudeAnalyzer
from display import Display

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="⚽ Análise Estatística de Futebol com IA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py team --name "Flamengo" --season 2024
  python main.py match --id 215662
  python main.py league --id 71 --season 2024
  python main.py player --id 1485
  python main.py h2h --team1 33 --team2 40
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Subcomando: time
    team_parser = subparsers.add_parser("team", help="Analisar estatísticas de um time")
    team_parser.add_argument("--name", type=str, help="Nome do time")
    team_parser.add_argument("--id", type=int, help="ID do time na API")
    team_parser.add_argument("--season", type=int, default=2024, help="Temporada (padrão: 2024)")
    team_parser.add_argument("--league", type=int, default=71, help="ID da liga (padrão: 71 = Brasileirão)")

    # Subcomando: partida
    match_parser = subparsers.add_parser("match", help="Analisar uma partida específica")
    match_parser.add_argument("--id", type=int, required=True, help="ID da partida")

    # Subcomando: liga
    league_parser = subparsers.add_parser("league", help="Analisar classificação de uma liga")
    league_parser.add_argument("--id", type=int, default=71, help="ID da liga (padrão: 71 = Brasileirão)")
    league_parser.add_argument("--season", type=int, default=2024, help="Temporada (padrão: 2024)")

    # Subcomando: jogador
    player_parser = subparsers.add_parser("player", help="Analisar estatísticas de um jogador")
    player_parser.add_argument("--id", type=int, required=True, help="ID do jogador")
    player_parser.add_argument("--season", type=int, default=2024, help="Temporada (padrão: 2024)")

    # Subcomando: h2h
    h2h_parser = subparsers.add_parser("h2h", help="Histórico de confrontos entre dois times")
    h2h_parser.add_argument("--team1", type=int, required=True, help="ID do primeiro time")
    h2h_parser.add_argument("--team2", type=int, required=True, help="ID do segundo time")

    # Subcomando: search
    search_parser = subparsers.add_parser("search", help="Buscar times por nome")
    search_parser.add_argument("--name", type=str, required=True, help="Nome do time para buscar")

    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        return

    print_banner()

    try:
        api = FootballAPI()
        analyzer = ClaudeAnalyzer()
        display = Display(console)

        if args.command == "team":
            run_team_analysis(api, analyzer, display, args)

        elif args.command == "match":
            run_match_analysis(api, analyzer, display, args)

        elif args.command == "league":
            run_league_analysis(api, analyzer, display, args)

        elif args.command == "player":
            run_player_analysis(api, analyzer, display, args)

        elif args.command == "h2h":
            run_h2h_analysis(api, analyzer, display, args)

        elif args.command == "search":
            run_team_search(api, display, args)

    except KeyboardInterrupt:
        console.print("\n[yellow]Análise interrompida pelo usuário.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Erro: {e}[/red]")
        sys.exit(1)


def print_banner():
    banner = Text()
    banner.append("⚽ FOOTBALL STATS ANALYZER", style="bold green")
    banner.append("  |  ", style="dim")
    banner.append("API-Football", style="bold cyan")
    banner.append(" + ", style="dim")
    banner.append("Claude AI", style="bold magenta")
    console.print(Panel(banner, border_style="green"))
    console.print()


def run_team_analysis(api, analyzer, display, args):
    if args.name:
        console.print(f"[cyan]🔍 Buscando time: {args.name}...[/cyan]")
        teams = api.search_team(args.name)
        if not teams:
            console.print("[red]Time não encontrado.[/red]")
            return
        team_id = teams[0]["team"]["id"]
        team_name = teams[0]["team"]["name"]
    elif args.id:
        team_id = args.id
        team_name = f"Time ID {args.id}"
    else:
        console.print("[red]Informe --name ou --id do time.[/red]")
        return

    console.print(f"[cyan]📊 Carregando estatísticas de {team_name}...[/cyan]")
    stats = api.get_team_statistics(team_id, args.league, args.season)
    fixtures = api.get_team_fixtures(team_id, args.season, last=10)

    display.show_team_stats(stats, fixtures)

    console.print("\n[magenta]🤖 Claude AI analisando dados...[/magenta]")
    analysis = analyzer.analyze_team(stats, fixtures)
    display.show_ai_analysis(analysis, title="📋 Análise do Time")


def run_match_analysis(api, analyzer, display, args):
    console.print(f"[cyan]🔍 Carregando dados da partida {args.id}...[/cyan]")
    fixture = api.get_fixture(args.id)
    stats = api.get_fixture_statistics(args.id)
    events = api.get_fixture_events(args.id)

    display.show_match_stats(fixture, stats, events)

    console.print("\n[magenta]🤖 Claude AI analisando partida...[/magenta]")
    analysis = analyzer.analyze_match(fixture, stats, events)
    display.show_ai_analysis(analysis, title="📋 Análise da Partida")


def run_league_analysis(api, analyzer, display, args):
    console.print(f"[cyan]📊 Carregando classificação da liga {args.id}...[/cyan]")
    standings = api.get_standings(args.id, args.season)
    top_scorers = api.get_top_scorers(args.id, args.season)

    display.show_league_standings(standings, top_scorers)

    console.print("\n[magenta]🤖 Claude AI analisando liga...[/magenta]")
    analysis = analyzer.analyze_league(standings, top_scorers)
    display.show_ai_analysis(analysis, title="📋 Análise da Liga")


def run_player_analysis(api, analyzer, display, args):
    console.print(f"[cyan]🔍 Carregando estatísticas do jogador {args.id}...[/cyan]")
    player = api.get_player_statistics(args.id, args.season)

    display.show_player_stats(player)

    console.print("\n[magenta]🤖 Claude AI analisando jogador...[/magenta]")
    analysis = analyzer.analyze_player(player)
    display.show_ai_analysis(analysis, title="📋 Análise do Jogador")


def run_h2h_analysis(api, analyzer, display, args):
    console.print(f"[cyan]🔍 Carregando confrontos entre times...[/cyan]")
    h2h = api.get_head_to_head(args.team1, args.team2)

    display.show_h2h(h2h)

    console.print("\n[magenta]🤖 Claude AI analisando histórico...[/magenta]")
    analysis = analyzer.analyze_h2h(h2h)
    display.show_ai_analysis(analysis, title="📋 Análise H2H")


def run_team_search(api, display, args):
    console.print(f"[cyan]🔍 Buscando times com nome '{args.name}'...[/cyan]")
    teams = api.search_team(args.name)
    display.show_team_search_results(teams)


if __name__ == "__main__":
    main()
