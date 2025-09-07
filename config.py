"""
Configuration file for Search AI Agent
Copy this file and modify the values as needed
"""

import os
from typing import Optional

# API Configuration - These will be loaded after .env file is processed
GEMINI_API_KEY: Optional[str] = None
TAVILY_API_KEY: Optional[str] = None

# Model Configuration
MODEL_NAME = "gemini-2.5-flash"
MODEL_TEMPERATURE = 0.7
MODEL_MAX_TOKENS = 2000

# Search Configuration
DEFAULT_SEARCH_RESULTS = 5
DEFAULT_QUERY = "Research recent developments in AI and machine learning, focusing on practical applications and industry trends. Be comprehensive but concise."

# API Endpoints
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Error Messages
ERROR_MESSAGES = {
    "missing_gemini_key": "GEMINI_API_KEY environment variable is required",
    "missing_tavily_key": "TAVILY_API_KEY environment variable is required",
    "tavily_client_error": "Failed to create Tavily client: {}",
    "provider_error": "Failed to create provider: {}",
    "model_error": "Failed to create model: {}",
    "agent_error": "Error running agent: {}",
}

# Instructions for the AI Agent
AGENT_INSTRUCTIONS = """
You are a Search AI Agent, an intelligent assistant that can search the web and extract information from websites.

Your capabilities:
1. Search the web for current information using the search tool
2. Extract detailed content from specific URLs using the extract_content tool

Guidelines:
- Always use the search tool first to find relevant information
- When you find useful URLs, use extract_content to get detailed information
- Provide comprehensive, well-structured responses
- Cite your sources when possible
- Be concise but thorough
- If a search doesn't yield good results, try rephrasing the query

Example workflow:
1. Search for the user's query
2. Identify relevant URLs from search results
3. Extract content from the most relevant URLs
4. Synthesize the information into a coherent response
"""

# Multi-Agent Role Instructions
RESEARCHER_INSTRUCTIONS = """
You are the Researcher. Your job is to plan and execute web searches using the available tools.
- Break the query into sub-questions.
- Use search first, then pick 3-5 high-signal URLs.
- Use extract_content on selected URLs and summarize factual findings.
- Return a concise research brief with citations (URLs) and bullet key points.
"""

ANALYST_INSTRUCTIONS = """
You are the Analyst. Your job is to synthesize the Researcher's brief.
- Compare and contrast sources, identify consensus and disagreements.
- Pull out practical implications and risks.
- Produce a structured analysis with sections: Summary, Key Findings, Caveats, Recommendations.
"""

WRITER_INSTRUCTIONS = """
You are the Writer. Your job is to polish the Analyst's synthesis for the end user profile.
- Adapt tone and technical depth to the provided personalization context.
- Keep it clear, concise, and actionable; include numbered steps where relevant.
- Preserve citations where helpful.
"""

def load_api_keys():
    """Load API keys from environment variables."""
    global GEMINI_API_KEY, TAVILY_API_KEY
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

def validate_config() -> bool:
    """Validate that all required configuration is present."""
    # Load API keys first
    load_api_keys()
    
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY is not set")
        return False
    
    if not TAVILY_API_KEY:
        print("❌ TAVILY_API_KEY is not set")
        return False
    
    return True

def print_setup_instructions():
    """Print setup instructions for missing configuration."""
    print("\n💡 Setup Instructions:")
    print("1. Create a .env file in the project root")
    print("2. Add your API keys:")
    print("   GEMINI_API_KEY=your_gemini_api_key_here")
    print("   TAVILY_API_KEY=your_tavily_api_key_here")
    print("\n3. Get your API keys from:")
    print("   - Gemini: https://makersuite.google.com/app/apikey")
    print("   - Tavily: https://tavily.com/") 