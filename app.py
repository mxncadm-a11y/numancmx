"""
app.py — ⚽ Football Stats Analyzer | Streamlit + API-Football + Claude AI
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from football_api import FootballAPI
from claude_analyzer import ClaudeAnalyzer
from config import Config

# ─────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="⚽ Football Analyzer",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CSS PERSONALIZADO — Tema escuro premium
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Inter:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0a0e1a;
    color: #e8eaf0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1120 !important;
    border-right: 1px solid #1e2640;
}

[data-testid="stSidebar"] .stRadio > label {
    color: #8892b0 !important;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Header principal ── */
.main-header {
    background: linear-gradient(135deg, #0d1120 0%, #111827 50%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00d4aa, #0066ff, #00d4aa);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.main-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #ffffff;
    margin: 0;
    line-height: 1;
}
.main-subtitle {
    color: #5a7fa0;
    font-size: 13px;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 6px;
}

/* ── Cards ── */
.stat-card {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: #00d4aa; }
.stat-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 38px;
    font-weight: 800;
    color: #00d4aa;
    line-height: 1;
}
.stat-label {
    font-size: 11px;
    color: #5a7fa0;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 6px;
}

/* ── Seções ── */
.section-header {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 1px;
    border-left: 4px solid #00d4aa;
    padding-left: 14px;
    margin: 28px 0 16px;
}

/* ── AI Panel ── */
.ai-panel {
    background: linear-gradient(135deg, #0d1a2e 0%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #0066ff;
    border-radius: 12px;
    padding: 24px 28px;
    margin-top: 20px;
}
.ai-label {
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #0066ff;
    margin-bottom: 12px;
    font-weight: 600;
}
.ai-text {
    color: #b8c8dc;
    font-size: 14px;
    line-height: 1.8;
    white-space: pre-wrap;
}

/* ── Form ── */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stNumberInput > div > div > input {
    background: #111827 !important;
    border: 1px solid #1e2d45 !important;
    color: #e8eaf0 !important;
    border-radius: 8px !important;
}

/* ── Botão ── */
.stButton > button {
    background: linear-gradient(135deg, #00d4aa, #0099cc);
    color: #000000;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 1px;
    border: none;
    border-radius: 8px;
    padding: 10px 28px;
    width: 100%;
    transition: opacity 0.2s, transform 0.1s;
}
.stButton > button:hover {
    opacity: 0.9;
    transform: translateY(-1px);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111827;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #5a7fa0;
    border-radius: 8px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 1px;
}
.stTabs [aria-selected="true"] {
    background: #1e2d45 !important;
    color: #00d4aa !important;
}

/* ── Tabelas ── */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}

/* ── Form indicator ── */
.form-badge {
    display: inline-block;
    width: 22px; height: 22px;
    border-radius: 50%;
    text-align: center;
    line-height: 22px;
    font-size: 11px;
    font-weight: 700;
    margin: 1px;
}
.form-w { background: #00d4aa; color: #000; }
.form-d { background: #f59e0b; color: #000; }
.form-l { background: #ef4444; color: #fff; }

/* ── Divider ── */
hr { border-color: #1e2d45 !important; }

/* ── League badge ── */
.league-badge {
    background: #1e2d45;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 12px;
    color: #8892b0;
    display: inline-block;
}

/* ── Metric override ── */
[data-testid="metric-container"] {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="metric-container"] label {
    color: #5a7fa0 !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #00d4aa !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 32px !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #00d4aa !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #1e2d45; border-radius: 3px; }

/* ── Radio buttons on sidebar ── */
[data-testid="stSidebar"] [data-baseweb="radio"] {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# INICIALIZAÇÃO
# ─────────────────────────────────────────────────────────────

@st.cache_resource
def init_clients():
    config = Config()
    errors = config.validate()
    if errors:
        return None, None, errors
    try:
        api = FootballAPI()
        analyzer = ClaudeAnalyzer()
        return api, analyzer, []
    except Exception as e:
        return None, None, [str(e)]

api, analyzer, config_errors = init_clients()

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 28px;">
        <div style="font-size: 40px;">⚽</div>
        <div style="font-family:'Barlow Condensed',sans-serif; font-size:22px; font-weight:800; color:#fff; letter-spacing:1px;">FOOTBALL ANALYZER</div>
        <div style="font-size:10px; color:#5a7fa0; letter-spacing:3px; margin-top:4px;">POWERED BY CLAUDE AI</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div style="font-size:10px;color:#5a7fa0;letter-spacing:3px;margin-bottom:10px;">NAVEGAÇÃO</div>', unsafe_allow_html=True)

    page = st.radio(
        "",
        ["🏠  Início",
         "📊  Times",
         "⚽  Partidas",
         "🏆  Ligas",
         "👤  Jogadores",
         "⚔️  H2H"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<div style="font-size:10px;color:#5a7fa0;letter-spacing:3px;margin-bottom:10px;">LIGAS POPULARES</div>', unsafe_allow_html=True)

    LEAGUES = {
        "🇧🇷 Brasileirão A": 71,
        "🇧🇷 Brasileirão B": 72,
        "🇧🇷 Copa do Brasil": 73,
        "🌎 Libertadores": 13,
        "🌎 Sul-Americana": 11,
        "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": 39,
        "🇪🇸 La Liga": 140,
        "🇩🇪 Bundesliga": 78,
        "🇮🇹 Serie A": 135,
        "🇫🇷 Ligue 1": 61,
        "🌍 Champions League": 2,
    }
    for name, lid in LEAGUES.items():
        st.markdown(f'<div style="font-size:12px;color:#8892b0;padding:3px 0;">{name} <span style="float:right;color:#1e3a5f;">#{lid}</span></div>', unsafe_allow_html=True)

    if config_errors:
        st.markdown("---")
        st.error("⚠️ Configuração incompleta")
        for err in config_errors:
            st.caption(f"• {err}")

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="main-header">
        <div class="main-title">{title}</div>
        {"" if not subtitle else f'<div class="main-subtitle">{subtitle}</div>'}
    </div>
    """, unsafe_allow_html=True)


def section(title: str):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def ai_panel(text: str):
    st.markdown(f"""
    <div class="ai-panel">
        <div class="ai-label">🤖 Claude AI — Análise</div>
        <div class="ai-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def form_badges(form_str: str) -> str:
    badges = ""
    for c in form_str[-8:]:
        cls = {"W": "form-w", "D": "form-d", "L": "form-l"}.get(c, "")
        badges += f'<span class="form-badge {cls}">{c}</span>'
    return badges


def plotly_dark(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8892b0", family="Inter"),
        title_font=dict(color="#ffffff", family="Barlow Condensed", size=18),
        xaxis=dict(gridcolor="#1e2d45", zerolinecolor="#1e2d45"),
        yaxis=dict(gridcolor="#1e2d45", zerolinecolor="#1e2d45"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig

# ─────────────────────────────────────────────────────────────
# PÁGINA: INÍCIO
# ─────────────────────────────────────────────────────────────

if page == "🏠  Início":
    header("FOOTBALL STATS ANALYZER", "API-FOOTBALL + CLAUDE AI • ANÁLISE INTELIGENTE")

    st.markdown("""
    <div style="color:#8892b0; font-size:15px; line-height:1.8; max-width:720px;">
        Bem-vindo ao <strong style="color:#00d4aa;">Football Analyzer</strong> — uma ferramenta de análise 
        estatística de futebol que combina dados em tempo real da 
        <strong style="color:#fff;">API-Football</strong> com inteligência artificial do 
        <strong style="color:#0066ff;">Claude (Anthropic)</strong> para gerar insights profundos em português.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    cards = [
        ("📊", "Times", "Estatísticas completas da temporada, forma e resultados"),
        ("⚽", "Partidas", "Análise detalhada de qualquer jogo: gols, eventos e stats"),
        ("🏆", "Ligas", "Classificação, artilheiros e visão da temporada"),
        ("👤", "Jogadores", "Performance individual com análise por posição"),
    ]
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:28px;margin-bottom:10px;">{icon}</div>
                <div style="font-family:'Barlow Condensed',sans-serif;font-size:18px;font-weight:700;color:#fff;">{title}</div>
                <div style="font-size:12px;color:#5a7fa0;margin-top:6px;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section("🚀 Como usar")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background:#111827;border:1px solid #1e2d45;border-radius:12px;padding:20px;">
            <div style="font-family:'Barlow Condensed',sans-serif;color:#fff;font-size:16px;font-weight:700;margin-bottom:14px;">⚙️ Configuração</div>
            <div style="font-size:13px;color:#8892b0;line-height:2;">
                1. Configure suas chaves no arquivo <code style="color:#00d4aa;">.env</code><br>
                2. <code style="color:#00d4aa;">ANTHROPIC_API_KEY</code> → console.anthropic.com<br>
                3. <code style="color:#00d4aa;">FOOTBALL_API_KEY</code> → api-football.com<br>
                4. Execute: <code style="color:#00d4aa;">streamlit run app.py</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#111827;border:1px solid #1e2d45;border-radius:12px;padding:20px;">
            <div style="font-family:'Barlow Condensed',sans-serif;color:#fff;font-size:16px;font-weight:700;margin-bottom:14px;">📡 API-Football — Planos</div>
            <div style="font-size:13px;color:#8892b0;line-height:2;">
                🆓 <strong style="color:#fff;">Free:</strong> 100 requisições/dia<br>
                💼 <strong style="color:#fff;">Starter:</strong> 7.500 req/dia — ~$10/mês<br>
                🚀 <strong style="color:#fff;">Pro:</strong> 50.000 req/dia — ~$40/mês<br>
                ℹ️ Cada análise usa ~3-5 requisições
            </div>
        </div>
        """, unsafe_allow_html=True)

    if config_errors:
        st.markdown("<br>", unsafe_allow_html=True)
        st.error("**Configuração necessária!** Crie o arquivo `.env` com suas chaves de API antes de usar as análises.")

# ─────────────────────────────────────────────────────────────
# PÁGINA: TIMES
# ─────────────────────────────────────────────────────────────

elif page == "📊  Times":
    header("ANÁLISE DE TIMES", "ESTATÍSTICAS • FORMA • DESEMPENHO")

    if config_errors:
        st.error("Configure as chaves de API antes de continuar.")
        st.stop()

    with st.form("team_form"):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            team_name = st.text_input("Nome do time", placeholder="ex: Flamengo, Palmeiras, Real Madrid...")
        with col2:
            season = st.number_input("Temporada", value=2024, min_value=2000, max_value=2025)
        with col3:
            league_id = st.number_input("ID da Liga", value=71, min_value=1)
        submitted = st.form_submit_button("🔍 ANALISAR TIME")

    if submitted and team_name:
        with st.spinner(f"Buscando {team_name}..."):
            teams = api.search_team(team_name)

        if not teams:
            st.error(f"Nenhum time encontrado para '{team_name}'")
        else:
            # Se múltiplos resultados, mostrar seletor
            if len(teams) > 1:
                options = {f"{t['team']['name']} ({t['team'].get('country','?')})": i for i, t in enumerate(teams)}
                choice = st.selectbox("Múltiplos times encontrados — selecione:", list(options.keys()))
                team_data = teams[options[choice]]
            else:
                team_data = teams[0]

            team_id = team_data["team"]["id"]
            team_info = team_data["team"]

            with st.spinner("Carregando estatísticas..."):
                stats = api.get_team_statistics(team_id, league_id, season)
                fixtures = api.get_team_fixtures(team_id, season, last=10)

            if not stats:
                st.warning("Sem dados para este time nesta liga/temporada.")
                st.stop()

            # Header do time
            col1, col2 = st.columns([1, 4])
            with col1:
                if team_info.get("logo"):
                    st.image(team_info["logo"], width=90)
            with col2:
                st.markdown(f"""
                <div style="margin-top:8px;">
                    <div style="font-family:'Barlow Condensed',sans-serif;font-size:34px;font-weight:800;color:#fff;">{team_info.get('name','')}</div>
                    <span class="league-badge">{stats.get('league',{}).get('name','?')} • {season}</span>
                    <span style="margin-left:8px;">{form_badges(stats.get('form',''))}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Métricas principais
            fixture_stats = stats.get("fixtures", {})
            goals = stats.get("goals", {})
            total_played = fixture_stats.get("played", {}).get("total", 0)
            total_wins = fixture_stats.get("wins", {}).get("total", 0)
            total_draws = fixture_stats.get("draws", {}).get("total", 0)
            total_losses = fixture_stats.get("loses", {}).get("total", 0)
            goals_for = goals.get("for", {}).get("total", {}).get("total", 0)
            goals_against = goals.get("against", {}).get("total", {}).get("total", 0)
            win_rate = round((total_wins / total_played * 100) if total_played > 0 else 0, 1)

            c1, c2, c3, c4, c5, c6 = st.columns(6)
            c1.metric("Jogos", total_played)
            c2.metric("Vitórias", total_wins)
            c3.metric("Empates", total_draws)
            c4.metric("Derrotas", total_losses)
            c5.metric("Gols Marcados", goals_for)
            c6.metric("% Vitórias", f"{win_rate}%")

            st.markdown("<br>", unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["📊 Estatísticas", "📅 Últimas Partidas", "🤖 Análise IA"])

            with tab1:
                col1, col2 = st.columns(2)

                with col1:
                    section("Resultados por Local")
                    df_results = pd.DataFrame({
                        "Local": ["🏠 Casa", "✈️ Fora"],
                        "Vitórias": [
                            fixture_stats.get("wins", {}).get("home", 0),
                            fixture_stats.get("wins", {}).get("away", 0),
                        ],
                        "Empates": [
                            fixture_stats.get("draws", {}).get("home", 0),
                            fixture_stats.get("draws", {}).get("away", 0),
                        ],
                        "Derrotas": [
                            fixture_stats.get("loses", {}).get("home", 0),
                            fixture_stats.get("loses", {}).get("away", 0),
                        ],
                    })
                    fig = go.Figure()
                    colors = {"Vitórias": "#00d4aa", "Empates": "#f59e0b", "Derrotas": "#ef4444"}
                    for col_name, color in colors.items():
                        fig.add_trace(go.Bar(
                            name=col_name, x=df_results["Local"],
                            y=df_results[col_name], marker_color=color,
                        ))
                    fig.update_layout(barmode="group", title="Resultados")
                    st.plotly_chart(plotly_dark(fig), use_container_width=True)

                with col2:
                    section("Gols por Período")
                    goals_for_minutes = goals.get("for", {}).get("minute", {})
                    if goals_for_minutes:
                        periods = list(goals_for_minutes.keys())
                        gf_vals = [goals_for_minutes.get(p, {}).get("total", 0) or 0 for p in periods]
                        goals_against_minutes = goals.get("against", {}).get("minute", {})
                        ga_vals = [goals_against_minutes.get(p, {}).get("total", 0) or 0 for p in periods]

                        fig2 = go.Figure()
                        fig2.add_trace(go.Bar(name="Marcados", x=periods, y=gf_vals, marker_color="#00d4aa"))
                        fig2.add_trace(go.Bar(name="Sofridos", x=periods, y=ga_vals, marker_color="#ef4444"))
                        fig2.update_layout(barmode="group", title="Gols por Minuto")
                        st.plotly_chart(plotly_dark(fig2), use_container_width=True)
                    else:
                        st.info("Dados de gols por minuto indisponíveis.")

                # Maiores vitórias/derrotas
                biggest = stats.get("biggest", {})
                col1, col2 = st.columns(2)
                with col1:
                    section("🏆 Maiores Vitórias")
                    st.markdown(f"""
                    <div class="stat-card">
                        <div style="font-size:12px;color:#5a7fa0;">Em Casa</div>
                        <div style="font-family:'Barlow Condensed',sans-serif;font-size:28px;font-weight:700;color:#00d4aa;">{biggest.get('wins',{}).get('home','—')}</div>
                        <div style="font-size:12px;color:#5a7fa0;margin-top:8px;">Fora de Casa</div>
                        <div style="font-family:'Barlow Condensed',sans-serif;font-size:28px;font-weight:700;color:#00d4aa;">{biggest.get('wins',{}).get('away','—')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    section("💔 Maiores Derrotas")
                    st.markdown(f"""
                    <div class="stat-card">
                        <div style="font-size:12px;color:#5a7fa0;">Em Casa</div>
                        <div style="font-family:'Barlow Condensed',sans-serif;font-size:28px;font-weight:700;color:#ef4444;">{biggest.get('loses',{}).get('home','—')}</div>
                        <div style="font-size:12px;color:#5a7fa0;margin-top:8px;">Fora de Casa</div>
                        <div style="font-family:'Barlow Condensed',sans-serif;font-size:28px;font-weight:700;color:#ef4444;">{biggest.get('loses',{}).get('away','—')}</div>
                    </div>
                    """, unsafe_allow_html=True)

            with tab2:
                section("Últimas 10 Partidas")
                if fixtures:
                    rows = []
                    for f in reversed(fixtures):
                        teams_f = f.get("teams", {})
                        score_f = f.get("score", {}).get("fulltime", {})
                        date_f = f.get("fixture", {}).get("date", "")[:10]
                        home_f = teams_f.get("home", {}).get("name", "?")
                        away_f = teams_f.get("away", {}).get("name", "?")
                        hg = score_f.get("home", "?")
                        ag = score_f.get("away", "?")
                        league_f = f.get("league", {}).get("name", "?")

                        home_win = teams_f.get("home", {}).get("winner")
                        away_win = teams_f.get("away", {}).get("winner")
                        result = "V" if (home_f == team_info.get("name") and home_win) or (away_f == team_info.get("name") and away_win) else ("E" if home_win is None else "D")

                        rows.append({
                            "Data": date_f,
                            "Liga": league_f,
                            "Mandante": home_f,
                            "Placar": f"{hg} x {ag}",
                            "Visitante": away_f,
                            "Res.": result,
                        })
                    df_fix = pd.DataFrame(rows)
                    st.dataframe(
                        df_fix,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Res.": st.column_config.TextColumn("Res."),
                        }
                    )

            with tab3:
                with st.spinner("🤖 Claude analisando dados..."):
                    analysis = analyzer.analyze_team(stats, fixtures)
                ai_panel(analysis)

# ─────────────────────────────────────────────────────────────
# PÁGINA: PARTIDAS
# ─────────────────────────────────────────────────────────────

elif page == "⚽  Partidas":
    header("ANÁLISE DE PARTIDAS", "EVENTOS • ESTATÍSTICAS • INSIGHTS")

    if config_errors:
        st.error("Configure as chaves de API antes de continuar.")
        st.stop()

    with st.form("match_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            fixture_id = st.number_input("ID da Partida (API-Football)", value=0, min_value=0,
                                          help="Use 'Buscar Times' para encontrar IDs de partidas recentes")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("⚽ ANALISAR PARTIDA")

    if submitted and fixture_id > 0:
        with st.spinner("Carregando dados da partida..."):
            fixture = api.get_fixture(fixture_id)
            stats = api.get_fixture_statistics(fixture_id)
            events = api.get_fixture_events(fixture_id)

        if not fixture:
            st.error(f"Partida #{fixture_id} não encontrada.")
            st.stop()

        teams = fixture.get("teams", {})
        score = fixture.get("score", {})
        league_data = fixture.get("league", {})
        fixture_info = fixture.get("fixture", {})

        home_team = teams.get("home", {})
        away_team = teams.get("away", {})
        ft = score.get("fulltime", {})
        ht = score.get("halftime", {})

        # Score hero
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0d1120,#111827);border:1px solid #1e3a5f;border-radius:16px;padding:32px;text-align:center;margin-bottom:24px;">
            <div style="font-size:11px;color:#5a7fa0;letter-spacing:3px;margin-bottom:16px;">{league_data.get('name','?')} • {fixture_info.get('date','')[:10]} • {fixture_info.get('venue',{}).get('name','?')}</div>
            <div style="display:flex;align-items:center;justify-content:center;gap:32px;">
                <div style="text-align:center;">
                    {'<img src="' + home_team.get("logo","") + '" width="64" style="margin-bottom:8px;">' if home_team.get("logo") else ""}
                    <div style="font-family:'Barlow Condensed',sans-serif;font-size:24px;font-weight:700;color:#fff;">{home_team.get('name','?')}</div>
                </div>
                <div style="font-family:'Barlow Condensed',sans-serif;font-size:56px;font-weight:800;color:#00d4aa;letter-spacing:-2px;">{ft.get('home','?')} — {ft.get('away','?')}</div>
                <div style="text-align:center;">
                    {'<img src="' + away_team.get("logo","") + '" width="64" style="margin-bottom:8px;">' if away_team.get("logo") else ""}
                    <div style="font-family:'Barlow Condensed',sans-serif;font-size:24px;font-weight:700;color:#fff;">{away_team.get('name','?')}</div>
                </div>
            </div>
            <div style="font-size:12px;color:#5a7fa0;margin-top:12px;">Intervalo: {ht.get('home','?')} – {ht.get('away','?')}</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["📊 Estatísticas", "⚡ Eventos", "🤖 Análise IA"])

        with tab1:
            if stats and len(stats) >= 2:
                home_stats = {s["type"]: s["value"] for s in stats[0].get("statistics", [])}
                away_stats = {s["type"]: s["value"] for s in stats[1].get("statistics", [])}

                keys = ["Ball Possession", "Total Shots", "Shots on Goal", "Corner Kicks",
                        "Fouls", "Passes", "Pass Accuracy", "Offsides", "Yellow Cards"]

                stat_rows = []
                for k in keys:
                    hv = str(home_stats.get(k, "–"))
                    av = str(away_stats.get(k, "–"))
                    stat_rows.append({"Estatística": k, home_team.get("name","Casa"): hv, away_team.get("name","Fora"): av})

                st.dataframe(pd.DataFrame(stat_rows), use_container_width=True, hide_index=True)

                # Gráfico radar simplificado
                radar_keys = ["Total Shots", "Shots on Goal", "Corner Kicks", "Fouls", "Passes"]
                try:
                    h_vals = [float(str(home_stats.get(k, 0) or 0).replace("%","")) for k in radar_keys]
                    a_vals = [float(str(away_stats.get(k, 0) or 0).replace("%","")) for k in radar_keys]

                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(r=h_vals, theta=radar_keys, fill="toself",
                                                   name=home_team.get("name","Casa"), line_color="#00d4aa"))
                    fig.add_trace(go.Scatterpolar(r=a_vals, theta=radar_keys, fill="toself",
                                                   name=away_team.get("name","Fora"), line_color="#0066ff"))
                    fig.update_layout(polar=dict(
                        bgcolor="rgba(0,0,0,0)",
                        radialaxis=dict(gridcolor="#1e2d45", color="#5a7fa0"),
                        angularaxis=dict(gridcolor="#1e2d45", color="#8892b0"),
                    ), title="Comparação Estatística")
                    st.plotly_chart(plotly_dark(fig), use_container_width=True)
                except:
                    pass
            else:
                st.info("Estatísticas não disponíveis para esta partida.")

        with tab2:
            goals_ev = [e for e in events if e.get("type") == "Goal"]
            cards_ev = [e for e in events if e.get("type") == "Card"]
            subs_ev = [e for e in events if e.get("type") == "subst"]

            if goals_ev:
                section("⚽ Gols")
                for g in goals_ev:
                    minute = g.get("time", {}).get("elapsed", "?")
                    player = g.get("player", {}).get("name", "?")
                    team = g.get("team", {}).get("name", "?")
                    assist = g.get("assist", {}).get("name")
                    st.markdown(f"""
                    <div style="background:#111827;border:1px solid #1e2d45;border-left:4px solid #00d4aa;border-radius:8px;padding:12px 16px;margin:6px 0;display:flex;gap:16px;align-items:center;">
                        <span style="font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:700;color:#00d4aa;">{minute}'</span>
                        <div>
                            <div style="color:#fff;font-weight:500;">{player}</div>
                            <div style="font-size:12px;color:#5a7fa0;">{team}{f' • Assistência: {assist}' if assist else ''}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            if cards_ev:
                section("🟨 Cartões")
                for c in cards_ev:
                    minute = c.get("time", {}).get("elapsed", "?")
                    player = c.get("player", {}).get("name", "?")
                    team = c.get("team", {}).get("name", "?")
                    detail = c.get("detail", "Cartão")
                    color = "#f59e0b" if "Yellow" in detail else "#ef4444"
                    st.markdown(f"""
                    <div style="background:#111827;border:1px solid #1e2d45;border-left:4px solid {color};border-radius:8px;padding:12px 16px;margin:6px 0;">
                        <span style="font-family:'Barlow Condensed',sans-serif;font-size:18px;font-weight:700;color:{color};">{minute}'</span>
                        <span style="color:#fff;margin-left:12px;">{player}</span>
                        <span style="color:#5a7fa0;font-size:12px;margin-left:8px;">• {team} • {detail}</span>
                    </div>
                    """, unsafe_allow_html=True)

            if not goals_ev and not cards_ev:
                st.info("Eventos não disponíveis para esta partida.")

        with tab3:
            with st.spinner("🤖 Claude analisando partida..."):
                analysis = analyzer.analyze_match(fixture, stats, events)
            ai_panel(analysis)

# ─────────────────────────────────────────────────────────────
# PÁGINA: LIGAS
# ─────────────────────────────────────────────────────────────

elif page == "🏆  Ligas":
    header("ANÁLISE DE LIGAS", "CLASSIFICAÇÃO • ARTILHEIROS • TEMPORADA")

    if config_errors:
        st.error("Configure as chaves de API antes de continuar.")
        st.stop()

    with st.form("league_form"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            league_options = {name: lid for name, lid in LEAGUES.items()}
            league_choice = st.selectbox("Liga", list(league_options.keys()))
        with col2:
            custom_id = st.number_input("ID personalizado (opcional)", value=0, min_value=0)
        with col3:
            season = st.number_input("Temporada", value=2024, min_value=2000, max_value=2025)
        submitted = st.form_submit_button("🏆 VER CLASSIFICAÇÃO")

    if submitted:
        league_id = custom_id if custom_id > 0 else league_options[league_choice]

        with st.spinner("Carregando classificação..."):
            standings = api.get_standings(league_id, season)
            top_scorers = api.get_top_scorers(league_id, season)

        if not standings:
            st.error("Classificação não disponível para esta liga/temporada.")
            st.stop()

        group = standings[0]

        tab1, tab2, tab3 = st.tabs(["🏆 Classificação", "🥇 Artilheiros", "🤖 Análise IA"])

        with tab1:
            section(f"Classificação • Temporada {season}")
            rows = []
            for t in group:
                rows.append({
                    "#": t.get("rank"),
                    "Time": t.get("team", {}).get("name", "?"),
                    "P": t.get("points", 0),
                    "J": t.get("all", {}).get("played", 0),
                    "V": t.get("all", {}).get("win", 0),
                    "E": t.get("all", {}).get("draw", 0),
                    "D": t.get("all", {}).get("lose", 0),
                    "GM": t.get("all", {}).get("goals", {}).get("for", 0),
                    "GC": t.get("all", {}).get("goals", {}).get("against", 0),
                    "SG": t.get("goalsDiff", 0),
                    "Forma": t.get("form", ""),
                })
            df_standings = pd.DataFrame(rows)
            st.dataframe(df_standings, use_container_width=True, hide_index=True)

            # Gráfico pontos
            section("Pontos por Time (Top 10)")
            top10 = df_standings.head(10)
            fig = go.Figure(go.Bar(
                x=top10["Time"], y=top10["P"],
                marker_color=["#00d4aa" if i < 4 else "#0066ff" if i < 6 else "#f59e0b" if i > 14 else "#8892b0"
                               for i in range(len(top10))],
                text=top10["P"], textposition="auto",
            ))
            fig.update_layout(title="Pontuação", xaxis_tickangle=-30)
            st.plotly_chart(plotly_dark(fig), use_container_width=True)

        with tab2:
            if top_scorers:
                section("Top 10 Artilheiros")
                scorer_rows = []
                for i, s in enumerate(top_scorers[:10], 1):
                    player = s.get("player", {})
                    st_s = s.get("statistics", [{}])[0]
                    scorer_rows.append({
                        "#": i,
                        "Jogador": player.get("name", "?"),
                        "Time": st_s.get("team", {}).get("name", "?"),
                        "Nac.": player.get("nationality", "?"),
                        "Gols": st_s.get("goals", {}).get("total", 0),
                        "Assist.": st_s.get("goals", {}).get("assists", 0),
                        "Jogos": st_s.get("games", {}).get("appearences", 0),
                    })
                df_scorers = pd.DataFrame(scorer_rows)
                st.dataframe(df_scorers, use_container_width=True, hide_index=True)

                # Bar chart artilheiros
                fig2 = go.Figure(go.Bar(
                    y=df_scorers["Jogador"][:10],
                    x=df_scorers["Gols"][:10],
                    orientation="h",
                    marker_color="#f59e0b",
                    text=df_scorers["Gols"][:10],
                    textposition="auto",
                ))
                fig2.update_layout(title="Gols Marcados", yaxis=dict(autorange="reversed"))
                st.plotly_chart(plotly_dark(fig2), use_container_width=True)

        with tab3:
            with st.spinner("🤖 Claude analisando liga..."):
                analysis = analyzer.analyze_league(standings, top_scorers)
            ai_panel(analysis)

# ─────────────────────────────────────────────────────────────
# PÁGINA: JOGADORES
# ─────────────────────────────────────────────────────────────

elif page == "👤  Jogadores":
    header("ANÁLISE DE JOGADORES", "PERFORMANCE • ESTATÍSTICAS • IMPACTO")

    if config_errors:
        st.error("Configure as chaves de API antes de continuar.")
        st.stop()

    with st.form("player_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            player_id = st.number_input("ID do Jogador (API-Football)", value=0, min_value=0)
        with col2:
            season = st.number_input("Temporada", value=2024, min_value=2000, max_value=2025)
        st.markdown('<div style="font-size:12px;color:#5a7fa0;">Dica: Busque o ID em api-football.com ou use a busca de times para encontrar jogadores.</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("👤 ANALISAR JOGADOR")

    if submitted and player_id > 0:
        with st.spinner("Carregando dados do jogador..."):
            player_data = api.get_player_statistics(player_id, season)

        if not player_data:
            st.error("Jogador não encontrado.")
            st.stop()

        player = player_data.get("player", {})
        stats_list = player_data.get("statistics", [{}])
        stats = stats_list[0] if stats_list else {}

        # Header jogador
        col1, col2 = st.columns([1, 4])
        with col1:
            if player.get("photo"):
                st.image(player["photo"], width=100)
        with col2:
            st.markdown(f"""
            <div style="margin-top:6px;">
                <div style="font-family:'Barlow Condensed',sans-serif;font-size:36px;font-weight:800;color:#fff;">{player.get('name','?')}</div>
                <div style="font-size:13px;color:#5a7fa0;">
                    {stats.get('games',{}).get('position','?')} • {stats.get('team',{}).get('name','?')} • {stats.get('league',{}).get('name','?')}
                </div>
                <div style="font-size:12px;color:#1e3a5f;margin-top:4px;">
                    {player.get('nationality','?')} • {player.get('age','?')} anos • {player.get('height','?')} • {player.get('weight','?')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        games = stats.get("games", {})
        goals = stats.get("goals", {})
        shots = stats.get("shots", {})
        passes = stats.get("passes", {})
        dribbles = stats.get("dribbles", {})
        tackles = stats.get("tackles", {})
        cards = stats.get("cards", {})

        # Métricas
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("Partidas", games.get("appearences", 0))
        c2.metric("Minutos", games.get("minutes", 0))
        c3.metric("Gols", goals.get("total", 0))
        c4.metric("Assistências", goals.get("assists", 0))
        c5.metric("Rating", games.get("rating", "–"))
        c6.metric("Amarelos", cards.get("yellow", 0))

        tab1, tab2 = st.tabs(["📊 Stats Detalhadas", "🤖 Análise IA"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                section("Ofensivo")
                off_data = {
                    "Gols": goals.get("total", 0),
                    "Assistências": goals.get("assists", 0),
                    "Chutes": shots.get("total", 0),
                    "No Alvo": shots.get("on", 0),
                }
                fig = go.Figure(go.Bar(
                    x=list(off_data.keys()), y=list(off_data.values()),
                    marker_color=["#00d4aa", "#0066ff", "#f59e0b", "#10b981"],
                    text=list(off_data.values()), textposition="auto"
                ))
                fig.update_layout(title="Stats Ofensivas")
                st.plotly_chart(plotly_dark(fig), use_container_width=True)

            with col2:
                section("Criação & Defensivo")
                def_data = {
                    "Passes": passes.get("total", 0),
                    "Dribles Tent.": dribbles.get("attempts", 0),
                    "Dribles OK": dribbles.get("success", 0),
                    "Desarmes": tackles.get("total", 0),
                    "Intercep.": tackles.get("interceptions", 0),
                }
                fig2 = go.Figure(go.Bar(
                    x=list(def_data.keys()), y=list(def_data.values()),
                    marker_color=["#8892b0", "#f59e0b", "#00d4aa", "#0066ff", "#10b981"],
                    text=list(def_data.values()), textposition="auto"
                ))
                fig2.update_layout(title="Stats de Criação e Defesa")
                st.plotly_chart(plotly_dark(fig2), use_container_width=True)

        with tab2:
            with st.spinner("🤖 Claude analisando jogador..."):
                analysis = analyzer.analyze_player(player_data)
            ai_panel(analysis)

# ─────────────────────────────────────────────────────────────
# PÁGINA: H2H
# ─────────────────────────────────────────────────────────────

elif page == "⚔️  H2H":
    header("CONFRONTO DIRETO — H2H", "HISTÓRICO • PADRÕES • TENDÊNCIAS")

    if config_errors:
        st.error("Configure as chaves de API antes de continuar.")
        st.stop()

    with st.form("h2h_form"):
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            team1_id = st.number_input("ID do Time 1", value=0, min_value=0)
        with col2:
            team2_id = st.number_input("ID do Time 2", value=0, min_value=0)
        with col3:
            last_n = st.number_input("Últimos", value=10, min_value=2, max_value=30)
        submitted = st.form_submit_button("⚔️ VER CONFRONTOS")

    if submitted and team1_id > 0 and team2_id > 0:
        with st.spinner("Carregando confrontos..."):
            h2h = api.get_head_to_head(team1_id, team2_id, last_n)

        if not h2h:
            st.error("Nenhum confronto encontrado entre estes times.")
            st.stop()

        # Calcular vantagem
        team1_name = h2h[0].get("teams", {}).get("home", {}).get("name", "Time 1")
        team2_name = h2h[0].get("teams", {}).get("away", {}).get("name", "Time 2")

        wins1, wins2, draws = 0, 0, 0
        goals1_total, goals2_total = 0, 0

        for f in h2h:
            teams_f = f.get("teams", {})
            score_f = f.get("score", {}).get("fulltime", {})
            home_name = teams_f.get("home", {}).get("name")
            hw = teams_f.get("home", {}).get("winner")
            aw = teams_f.get("away", {}).get("winner")

            hg = score_f.get("home", 0) or 0
            ag = score_f.get("away", 0) or 0

            if home_name == team1_name:
                goals1_total += hg
                goals2_total += ag
                if hw: wins1 += 1
                elif aw: wins2 += 1
                else: draws += 1
            else:
                goals2_total += hg
                goals1_total += ag
                if hw: wins2 += 1
                elif aw: wins1 += 1
                else: draws += 1

        # Score hero
        st.markdown(f"""
        <div style="background:#111827;border:1px solid #1e3a5f;border-radius:16px;padding:28px;text-align:center;margin-bottom:24px;">
            <div style="display:flex;justify-content:space-around;align-items:center;">
                <div>
                    <div style="font-family:'Barlow Condensed',sans-serif;font-size:26px;font-weight:800;color:#fff;">{team1_name}</div>
                    <div style="font-family:'Barlow Condensed',sans-serif;font-size:56px;font-weight:800;color:#00d4aa;">{wins1}</div>
                    <div style="font-size:11px;color:#5a7fa0;letter-spacing:2px;">VITÓRIAS</div>
                </div>
                <div>
                    <div style="font-family:'Barlow Condensed',sans-serif;font-size:36px;font-weight:700;color:#f59e0b;">{draws}</div>
                    <div style="font-size:11px;color:#5a7fa0;letter-spacing:2px;">EMPATES</div>
                </div>
                <div>
                    <div style="font-family:'Barlow Condensed',sans-serif;font-size:26px;font-weight:800;color:#fff;">{team2_name}</div>
                    <div style="font-family:'Barlow Condensed',sans-serif;font-size:56px;font-weight:800;color:#0066ff;">{wins2}</div>
                    <div style="font-size:11px;color:#5a7fa0;letter-spacing:2px;">VITÓRIAS</div>
                </div>
            </div>
            <div style="margin-top:16px;font-size:13px;color:#5a7fa0;">
                Total de gols: {team1_name} {goals1_total} × {goals2_total} {team2_name}
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📅 Histórico", "🤖 Análise IA"])

        with tab1:
            section("Histórico de Confrontos")
            rows = []
            for f in h2h:
                teams_f = f.get("teams", {})
                score_f = f.get("score", {}).get("fulltime", {})
                date = f.get("fixture", {}).get("date", "")[:10]
                home = teams_f.get("home", {}).get("name", "?")
                away = teams_f.get("away", {}).get("name", "?")
                hg = score_f.get("home", "?")
                ag = score_f.get("away", "?")
                league_n = f.get("league", {}).get("name", "?")
                rows.append({"Data": date, "Liga": league_n, "Mandante": home, "Placar": f"{hg} × {ag}", "Visitante": away})

            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            # Donut de vitórias
            fig = go.Figure(go.Pie(
                labels=[team1_name, "Empates", team2_name],
                values=[wins1, draws, wins2],
                marker_colors=["#00d4aa", "#f59e0b", "#0066ff"],
                hole=0.5,
            ))
            fig.update_layout(title="Distribuição de Resultados")
            st.plotly_chart(plotly_dark(fig), use_container_width=True)

        with tab2:
            with st.spinner("🤖 Claude analisando histórico..."):
                analysis = analyzer.analyze_h2h(h2h)
            ai_panel(analysis)
