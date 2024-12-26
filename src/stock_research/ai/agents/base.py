from typing import Any, Dict, Optional
from datetime import datetime

from phidata import Agent, Knowledge
from pydantic import BaseModel

from ...config.settings import settings

class AnalysisResult(BaseModel):
    """Base model for analysis results."""
    
    ticker: str
    analysis_type: str
    timestamp: str
    data: Dict[str, Any]
    summary: str
    recommendations: list[str]

class BaseAnalysisAgent(Agent):
    """Base class for analysis agents."""
    
    def __init__(
        self,
        name: str,
        knowledge_file: str,
        tools: Optional[list] = None,
    ):
        knowledge_path = settings.KNOWLEDGE_DIR / knowledge_file
        
        super().__init__(
            name=name,
            llm=settings.DEFAULT_MODEL,
            knowledge=Knowledge(
                documents=[str(knowledge_path)]
            ),
            tools=tools or [],
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
    
    def format_prompt(self, ticker: str) -> str:
        """Format the analysis prompt."""
        raise NotImplementedError
    
    def analyze(self, ticker: str) -> AnalysisResult:
        """Perform analysis for the given ticker."""
        prompt = self.format_prompt(ticker)
        response = self.run(prompt)
        
        return self.process_response(ticker, response)
    
    def process_response(self, ticker: str, response: str) -> AnalysisResult:
        """Process the agent's response into a structured format."""
        raise NotImplementedError