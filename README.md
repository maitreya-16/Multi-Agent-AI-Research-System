# 🤖 Multi-Agent AI Research System

> A fully autonomous multi-agent research assistant that coordinates specialized AI agents for web search, scraping, report writing, and self-critique - powered by LangChain, Tavily API, and deployed via Streamlit.

---

## 📌 Overview

This system orchestrates a pipeline of specialized AI agents that collaborate through a **shared state pipeline** to autonomously research any topic end-to-end. Each agent handles a distinct responsibility — from real-time web retrieval to structured report generation and self-critique — enabling high-quality, validated research output with minimal human intervention.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 Multi-Agent Architecture | Specialized agents for search, scraping, writing, and critique coordinated via LangChain |
| 🌐 Real-Time Web Research | Tavily API integration for live search and BeautifulSoup for content extraction |
| 🔗 LCEL Chains | LangChain Expression Language for composable, structured report generation |
| 🪞 Self-Critique Loop | Critic agent reviews and validates outputs before finalization |
| 📊 Streamlit UI | Clean end-to-end web interface for task input and report viewing |
| 🔌 Extensible Design | Modular agent and tool architecture — easily add new agents or data sources |
| 🔐 Env Variable Support | Secure API key management via `python-dotenv` |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain** — Agent orchestration and LCEL pipeline
- **Tavily API** — Real-time web search and retrieval
- **BeautifulSoup4** — Web scraping and content parsing
- **OpenAI / Ollama** — Underlying LLM backbone
- **Streamlit** — Interactive frontend UI
- **Rich** — CLI-based visualization and logging
- **python-dotenv** — Environment variable management

---

## 🗂️ Project Structure

```
Multi-Agent-AI-Research-System/
│
├── agents.py           # Agent definitions and builders (search, scraper, writer, critic)
├── pipeline.py         # Shared state pipeline coordinating all agents
├── tools.py            # External tool integrations (Tavily, BeautifulSoup, utilities)
├── app.py              # Streamlit UI — entry point for end-to-end interaction
├── requirements.txt    # Python dependencies
├── .env                # API keys and environment variables (not committed)
└── README.md           # Documentation
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Multi-Agent-AI-Research-System.git
cd Multi-Agent-AI-Research-System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

> 💡 Get your Tavily API key at [tavily.com](https://tavily.com) and OpenAI key at [platform.openai.com](https://platform.openai.com).

---

## 🚀 Running the App

### Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` to interact with the research assistant.

---

## 🧩 Agent Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────┐
│           Shared State Pipeline         │
│                                         │
│  ┌──────────┐     ┌──────────────────┐  │
│  │  Search  │────▶│  Scraper Agent   │  │
│  │  Agent   │     │ (BeautifulSoup)  │  │
│  └──────────┘     └────────┬─────────┘  │
│       ▲                    │            │
│  Tavily API                ▼            │
│                   ┌──────────────────┐  │
│                   │   Writer Agent   │  │
│                   │  (LCEL Chains)   │  │
│                   └────────┬─────────┘  │
│                            │            │
│                            ▼            │
│                   ┌──────────────────┐  │
│                   │   Critic Agent   │  │
│                   │ (Self-Critique)  │  │
│                   └────────┬─────────┘  │
└────────────────────────────┼────────────┘
                             ▼
                     Final Research Report
```
