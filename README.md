🔬 MultiResearchAgent
A multi-agent AI research pipeline built with LangChain and Mistral AI that autonomously searches, scrapes, writes, and critiques research reports on any topic — with a professional Streamlit UI.
🧠 How It Works
The pipeline runs 4 agents/chains in sequence:
StepAgentTask1🌐 Search AgentSearches the web using Tavily API2📖 Reader AgentScrapes the most relevant URL for deep content3✍️ Writer ChainDrafts a structured research report4🧐 Critic ChainReviews and scores the report out of 10
🛠️ Tech Stack

LangChain — Agent orchestration
Mistral AI (mistral-small-2603) — LLM backbone
Tavily — Real-time web search
BeautifulSoup — Web scraping
Streamlit — Interactive UI
Python-dotenv — Secure API key management

🚀 Getting Started
bashgit clone https://github.com/ruderapratap/MultiResearchAgent.git
cd MultiResearchAgent
pip install -r requirements.txt
Create a .env file:
TAVILY_API_KEY=your_tavily_key
MISTRAL_API_KEY=your_mistral_key
Run the app:
bashpython -m streamlit run app.py
📁 Project Structure
├── app.py          # Streamlit UI
├── pipeline.py     # Main pipeline orchestrator
├── agents.py       # Agent & chain definitions
├── tools.py        # Web search & scraper tools
├── requirements.txt
└── .env            # API keys (never commit this)
✨ Features

🔍 Real-time web research on any topic
📄 Auto-generated structured reports
⭐ AI-powered quality scoring
🕰️ Session-based research history
🎨 Professional UI with custom theming
