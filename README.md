# Stock Research Agent

A comprehensive stock market research application built with phidata agents and Streamlit.

## Features

- **Fundamental Analysis**: Company financials, valuation metrics, and growth indicators
- **Technical Analysis**: Price trends, technical indicators, and trading signals
- **Sentiment Analysis**: News sentiment, social media trends, and market psychology
- **Interactive UI**: Built with Streamlit for a seamless user experience

## Installation

1. Clone the repository:
```bash
git clone https://github.com/joshmo01/stock-research-agent.git
cd stock-research-agent
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Unix systems
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
uv pip install -e ".[dev]"
```

4. Create a `.env` file with your API keys:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the Streamlit application:
```bash
streamlit run src/stock_research/ui/app.py
```

## Project Structure

```
stock_research/
├── src/
│   └── stock_research/
│       ├── ai/
│       │   ├── agents/     # AI agents for analysis
│       │   ├── tools/      # Custom tools and utilities
│       │   └── knowledge/  # Knowledge base for agents
│       ├── config/         # Configuration settings
│       └── ui/            # Streamlit UI components
└── tests/                 # Test suite
```

## Development

1. Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
isort .
```

4. Run type checking:
```bash
mypy src tests
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.