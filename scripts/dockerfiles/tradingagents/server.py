#!/usr/bin/env python3
"""TradingAgents FastAPI wrapper — exposes TauricResearch/TradingAgents as a REST API for AI-powered algorithmic trading."""

import os
from fastapi import FastAPI

app = FastAPI(
    title='TradingAgents',
    version='1.0.0',
    description='TradingAgents — Multi-agent LLM financial trading framework. Specialized AI agents collaborate to analyze markets, debate strategies, and execute trades.'
)


@app.get('/health')
async def health():
    """Health check — verify TradingAgents is installed and importable."""
    try:
        import tradingagents  # noqa: F401
        return {
            'status': 'ok',
            'framework': 'TradingAgents',
            'upstream': 'TauricResearch/TradingAgents',
            'version': 'v0.2.4'
        }
    except ImportError:
        return {
            'status': 'degraded',
            'framework': 'TradingAgents',
            'error': 'tradingagents module not importable'
        }


@app.get('/info')
async def info():
    return {
        'name': 'TradingAgents',
        'description': 'Multi-agent LLM financial trading framework — analysts, researchers, traders, and risk managers collaborate on trading decisions',
        'upstream': 'https://github.com/TauricResearch/TradingAgents',
        'install': 'pip install . (from cloned repo)',
        'providers': ['OpenAI (GPT)', 'Google (Gemini)', 'Anthropic (Claude)', 'xAI (Grok)', 'DeepSeek', 'Qwen (DashScope)', 'GLM (Zhipu)', 'OpenRouter', 'Ollama'],
        'agent_roles': [
            'Fundamentals Analyst — evaluates financials and performance metrics',
            'Sentiment Analyst — analyzes social media and public sentiment',
            'News Analyst — monitors global news and macroeconomic indicators',
            'Technical Analyst — uses MACD, RSI, and other indicators',
            'Bullish/Bearish Researchers — structured debate on market outlook',
            'Trader Agent — composes reports and makes trading decisions',
            'Risk Management — evaluates volatility, liquidity, and exposure',
            'Portfolio Manager — approves/rejects proposals for simulated execution'
        ],
        'cli': 'tradingagents  (interactive CLI)  or  python -m cli.main',
        'python_usage': 'from tradingagents.graph.trading_graph import TradingAgentsGraph; ta = TradingAgentsGraph(); _, decision = ta.propagate("NVDA", "2026-01-15")',
        'data_source': 'Alpha Vantage API (ALPHA_VANTAGE_API_KEY required)'
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('TRADINGAGENTS_PORT', '8000'))
    uvicorn.run(app, host='0.0.0.0', port=port)
