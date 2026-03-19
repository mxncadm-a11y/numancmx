# ⚽ Football Stats Analyzer — Streamlit

Dashboard interativo de análise de futebol com **API-Football** + **Claude AI**, rodando 100% no navegador via Streamlit.

---

## 🚀 Instalação rápida

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar chaves de API
cp .env.example .env
# Edite o .env com suas chaves

# 3. Rodar o app
streamlit run app.py
```

O app abre automaticamente em **http://localhost:8501** 🎉

---

## 🔑 Configuração do `.env`

```env
ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui
FOOTBALL_API_KEY=sua-chave-api-football-aqui
USE_RAPIDAPI=false
```

| Chave | Onde obter |
|---|---|
| `ANTHROPIC_API_KEY` | https://console.anthropic.com/ |
| `FOOTBALL_API_KEY` | https://www.api-football.com/ |

---

## 📱 Páginas do Dashboard

| Página | O que faz |
|---|---|
| 🏠 Início | Apresentação e guia de uso |
| 📊 Times | Estatísticas completas + gráficos + análise IA |
| ⚽ Partidas | Eventos, placar, radar comparativo + análise IA |
| 🏆 Ligas | Classificação, artilheiros, gráficos + análise IA |
| 👤 Jogadores | Performance individual + gráficos + análise IA |
| ⚔️ H2H | Histórico de confrontos + distribuição + análise IA |

---

## 🌍 IDs de Ligas

| Liga | ID |
|---|---|
| 🇧🇷 Brasileirão Série A | `71` |
| 🇧🇷 Brasileirão Série B | `72` |
| 🌎 Copa Libertadores | `13` |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League | `39` |
| 🇪🇸 La Liga | `140` |
| 🇩🇪 Bundesliga | `78` |
| 🌍 Champions League | `2` |

---

## 🗂️ Estrutura

```
football_streamlit/
├── app.py              # Dashboard Streamlit completo
├── football_api.py     # Wrapper da API-Football
├── claude_analyzer.py  # Análises com Claude AI
├── config.py           # Configuração e .env
├── requirements.txt    # Dependências
└── .env.example        # Modelo de configuração
```

---

## ☁️ Deploy no Streamlit Cloud (gratuito)

1. Suba o projeto para um repositório GitHub
2. Acesse https://share.streamlit.io
3. Conecte seu repositório
4. Em **Secrets**, adicione:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
FOOTBALL_API_KEY = "sua-chave"
USE_RAPIDAPI = "false"
```
5. Deploy! 🚀
