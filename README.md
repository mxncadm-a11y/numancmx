# ⚽ Football Stats Analyzer

Ferramenta de análise estatística de futebol com IA, usando **API-Football** para dados e **Claude (Anthropic)** para análises textuais inteligentes — tudo no terminal, em português.

---

## 🚀 Funcionalidades

| Funcionalidade | Comando |
|---|---|
| 📊 Estatísticas de time | `team` |
| ⚽ Análise de partida | `match` |
| 🏆 Classificação de liga | `league` |
| 👤 Estatísticas de jogador | `player` |
| ⚔️ Histórico H2H | `h2h` |
| 🔍 Buscar times | `search` |

Cada análise exibe dados brutos formatados **+** uma análise em linguagem natural gerada pelo Claude AI.

---

## 📦 Instalação

### 1. Clone ou baixe o projeto

```bash
cd football_analyzer
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as APIs

Copie o arquivo de exemplo e edite com suas chaves:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
ANTHROPIC_API_KEY=sk-ant-sua-chave-aqui
FOOTBALL_API_KEY=sua-chave-api-football-aqui
USE_RAPIDAPI=false
```

#### Onde obter as chaves:
- **Anthropic (Claude):** https://console.anthropic.com/
- **API-Football:** https://www.api-football.com/ *(plano gratuito: 100 req/dia)*

---

## 🎮 Uso

### Buscar um time pelo nome
```bash
python main.py search --name "Flamengo"
```

### Analisar estatísticas de um time
```bash
# Por nome (busca automática)
python main.py team --name "Flamengo" --season 2024 --league 71

# Por ID (mais rápido)
python main.py team --id 127 --season 2024 --league 71
```

### Analisar uma partida
```bash
python main.py match --id 215662
```

### Ver classificação de uma liga
```bash
python main.py league --id 71 --season 2024
```

### Analisar um jogador
```bash
python main.py player --id 1485 --season 2024
```

### Confronto direto (H2H)
```bash
python main.py h2h --team1 127 --team2 131
```

---

## 🌍 IDs de Ligas Populares

| Liga | ID |
|---|---|
| 🇧🇷 Brasileirão Série A | `71` |
| 🇧🇷 Brasileirão Série B | `72` |
| 🇧🇷 Copa do Brasil | `73` |
| 🌎 Copa Libertadores | `13` |
| 🌎 Copa Sul-Americana | `11` |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League | `39` |
| 🇪🇸 La Liga | `140` |
| 🇩🇪 Bundesliga | `78` |
| 🇮🇹 Serie A | `135` |
| 🇫🇷 Ligue 1 | `61` |
| 🌍 Champions League | `2` |
| 🌍 Europa League | `3` |

---

## 🏗️ Estrutura do Projeto

```
football_analyzer/
├── main.py            # Ponto de entrada e CLI
├── football_api.py    # Wrapper da API-Football
├── claude_analyzer.py # Análises com Claude AI
├── display.py         # Exibição rica no terminal
├── config.py          # Gerenciamento de configuração
├── requirements.txt   # Dependências Python
├── .env.example       # Modelo de configuração
└── README.md          # Esta documentação
```

---

## 📌 Exemplos de Saída

### Estatísticas de time
```
━━━━━━━━━━━━━━━━━━━━━━ Flamengo ━━━━━━━━━━━━━━━━━━━━━━
Liga: Brasileirão Série A | Temporada: 2024

Forma recente: W W D W L

┌─────────────────────────────────────┐
│        📊 Resultados                │
├──────────┬───────┬───┬───┬──────────┤
│ Local    │ Jogos │ V │ E │ D        │
├──────────┼───────┼───┼───┼──────────┤
│ 🏠 Casa  │  19   │12 │ 4 │  3       │
│ ✈️ Fora  │  19   │ 9 │ 5 │  5       │
│ 📈 Total │  38   │21 │ 9 │  8       │
└──────────┴───────┴───┴───┴──────────┘

╭─────────────── 📋 Análise do Time ───────────────╮
│  O Flamengo apresenta um desempenho sólido...    │
╰──────────────────────────────────────────────────╯
```

---

## ⚠️ Limites da API Gratuita

| Plano | Requisições/dia | Custo |
|---|---|---|
| Free | 100 | Gratuito |
| Starter | 7.500 | ~$10/mês |
| Pro | 50.000 | ~$40/mês |

Cada análise completa usa aproximadamente **2-4 requisições**.

---

## 🛠️ Tecnologias

- **Python 3.8+**
- **anthropic** — SDK oficial do Claude
- **requests** — Requisições HTTP
- **rich** — Interface de terminal estilizada

---

## 📄 Licença

MIT — Use livremente para fins pessoais e educacionais.
