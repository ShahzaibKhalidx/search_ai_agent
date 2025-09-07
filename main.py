import os
import asyncio
import sys
from typing import Optional
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, ModelSettings
from dotenv import load_dotenv, find_dotenv
from tavily import AsyncTavilyClient

# Load environment variables first
load_dotenv(find_dotenv())

from config import (
    GEMINI_API_KEY, TAVILY_API_KEY, MODEL_NAME, MODEL_TEMPERATURE, 
    MODEL_MAX_TOKENS, DEFAULT_SEARCH_RESULTS, DEFAULT_QUERY, 
    GEMINI_BASE_URL, AGENT_INSTRUCTIONS, validate_config, print_setup_instructions,
    RESEARCHER_INSTRUCTIONS, ANALYST_INSTRUCTIONS, WRITER_INSTRUCTIONS, load_api_keys
)
from user_profile import get_user_context, get_user_profile, update_user_profile, profile_manager

# Load API keys after importing config
load_api_keys()


class PersonalizedSearchAgent:
    """Enhanced search agent with personalization capabilities."""
    
    def __init__(self, model, tools):
        self.model = model
        self.tools = tools
        self.current_user_id = None
        self.user_profile = None
        self.interaction_history = []
        
    def set_user(self, user_id: str = None):
        """Set the current user for personalization."""
        self.current_user_id = user_id
        self.user_profile = get_user_profile(user_id) if user_id else None
        
        # Get personalization context
        personalization_context = get_user_context(user_id)
        
        # Create personalized instructions
        personalized_instructions = self._create_personalized_instructions(personalization_context)
        
        # Create agent with personalized instructions
        self.agent = Agent(
            name="Personalized Search Agent",
            model=self.model,
            tools=self.tools,
            instructions=personalized_instructions,
            model_settings=ModelSettings(
                temperature=MODEL_TEMPERATURE,
                tool_choice="auto",
                max_tokens=MODEL_MAX_TOKENS
            )
        )
        
        # Display user context
        if personalization_context:
            print(f"👤 {personalization_context}")
    
    def _create_personalized_instructions(self, personalization_context: str) -> str:
        """Create personalized instructions for the agent."""
        base_instructions = AGENT_INSTRUCTIONS
        
        if personalization_context:
            personalized_instructions = f"""
{personalization_context}

{base_instructions}

Additional Personalization Guidelines:
- Use examples and analogies that relate to the user's interests and profession
- Adjust technical depth based on the user's expertise level
- Reference the user's location when relevant (e.g., local tech events, regional trends)
- Consider the user's preferred topics when suggesting related areas to explore
- Use language and examples that match the user's professional background
"""
        else:
            personalized_instructions = base_instructions
        
        return personalized_instructions
    
    def add_interaction(self, query: str, response: str):
        """Track interaction history for context."""
        interaction = {
            "timestamp": asyncio.get_event_loop().time(),
            "query": query,
            "response": response[:200] + "..." if len(response) > 200 else response  # Truncate long responses
        }
        self.interaction_history.append(interaction)
        
        # Keep only last 10 interactions for context
        if len(self.interaction_history) > 10:
            self.interaction_history.pop(0)
    
    async def run(self, query: str):
        """Run the personalized search agent."""
        try:
            print(f"🤖 Personalized Search Agent is processing: {query}")
            print("=" * 60)
            
            # Run the agent
            runner = await Runner.run(self.agent, query)
            
            # Track interaction
            self.add_interaction(query, runner.final_output)
            
            # Update user profile with interaction count
            if self.current_user_id:
                update_user_profile(self.current_user_id, interaction_count=len(self.interaction_history))
            
            print("\n" + "=" * 60)
            print("🎯 FINAL ANSWER:")
            print("=" * 60)
            print(runner.final_output)
            
            return runner.final_output
            
        except Exception as e:
            print(f"❌ Error running agent: {e}")
            return None


class MultiAgentTeam:
    """Orchestrates a Researcher → Analyst → Writer multi-agent workflow."""

    def __init__(self, model, tools, personalization_context: str | None = None):
        self.model = model
        self.tools = tools
        self.personalization_context = personalization_context or ""

        # Build role-specific instruction sets with optional personalization header for the Writer
        writer_instr = (
            f"{self.personalization_context}\n\n{WRITER_INSTRUCTIONS}" if self.personalization_context else WRITER_INSTRUCTIONS
        )

        self.researcher = Agent(
            name="Researcher",
            model=self.model,
            tools=self.tools,
            instructions=RESEARCHER_INSTRUCTIONS,
            model_settings=ModelSettings(
                temperature=MODEL_TEMPERATURE,
                tool_choice="auto",
                max_tokens=MODEL_MAX_TOKENS,
            ),
        )

        self.analyst = Agent(
            name="Analyst",
            model=self.model,
            tools=[],
            instructions=ANALYST_INSTRUCTIONS,
            model_settings=ModelSettings(
                temperature=MODEL_TEMPERATURE,
                tool_choice="none",
                max_tokens=MODEL_MAX_TOKENS,
            ),
        )

        self.writer = Agent(
            name="Writer",
            model=self.model,
            tools=[],
            instructions=writer_instr,
            model_settings=ModelSettings(
                temperature=MODEL_TEMPERATURE,
                tool_choice="none",
                max_tokens=MODEL_MAX_TOKENS,
            ),
        )

    async def run(self, query: str) -> str:
        print("👥 Running Multi-Agent Team (Researcher → Analyst → Writer)")
        print("=" * 60)

        # Step 1: Researcher conducts web research using tools
        researcher_prompt = (
            "You will research the following user query. Produce a research brief with citations (URLs) and bullet key points.\n\n"
            f"Query: {query}"
        )
        researcher_runner = await Runner.run(self.researcher, researcher_prompt)
        research_brief = researcher_runner.final_output

        # Step 2: Analyst synthesizes the research brief
        analyst_prompt = (
            "Synthesize the following research brief. Provide sections: Summary, Key Findings, Caveats, Recommendations.\n\n"
            f"Research Brief:\n{research_brief}"
        )
        analyst_runner = await Runner.run(self.analyst, analyst_prompt)
        analysis = analyst_runner.final_output

        # Step 3: Writer adapts to user profile and polishes
        writer_prompt = (
            "Polish the analysis for the end user. Adapt tone and depth to the provided context if any. Keep it concise and actionable.\n\n"
            f"Analysis:\n{analysis}"
        )
        writer_runner = await Runner.run(self.writer, writer_prompt)
        final_output = writer_runner.final_output

        print("\n" + "=" * 60)
        print("🎯 FINAL ANSWER (Team):")
        print("=" * 60)
        print(final_output)
        return final_output


def load_environment():
    """Load environment variables and validate required API keys."""
    load_dotenv(find_dotenv())
    set_tracing_disabled(disabled=True)
    
    # Get API keys directly from environment
    gemini_key = os.environ.get("GEMINI_API_KEY")
    tavily_key = os.environ.get("TAVILY_API_KEY")
    
    # Validate configuration
    if not gemini_key:
        print("❌ GEMINI_API_KEY is not set")
        print_setup_instructions()
        sys.exit(1)
    
    if not tavily_key:
        print("❌ TAVILY_API_KEY is not set")
        print_setup_instructions()
        sys.exit(1)
    
    return gemini_key, tavily_key


def create_tavily_client(api_key: str) -> AsyncTavilyClient:
    """Create and return Tavily client."""
    try:
        return AsyncTavilyClient(api_key=api_key)
    except Exception as e:
        raise RuntimeError(f"Failed to create Tavily client: {e}")


def create_provider(api_key: str):
    """Create and return OpenAI-compatible provider for Gemini."""
    try:
        print(f"🔑 Creating provider with API key: {api_key[:10] + '...' if api_key else 'None'}")
        print(f"🌐 Base URL: {GEMINI_BASE_URL}")
        return AsyncOpenAI(
            api_key=api_key,
            base_url=GEMINI_BASE_URL,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to create provider: {e}")


def create_model(provider):
    """Create and return the LLM model."""
    try:
        return OpenAIChatCompletionsModel(
            openai_client=provider,
            model=MODEL_NAME,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to create model: {e}")


@function_tool()
async def search(query: str) -> str:
    """Search the web for information using Tavily search API."""
    print(f"🔍 Searching for: {query}")
    try:
        response = await tavily_client.search(query, max_results=DEFAULT_SEARCH_RESULTS)
        return f"Search results for '{query}': {response}"
    except Exception as e:
        error_msg = f"Error during search: {e}"
        print(f"❌ {error_msg}")
        return error_msg


@function_tool()
async def extract_content(urls: list) -> dict:
    """Extract content from a list of URLs using Tavily content extraction API."""
    print(f"📄 Extracting content from {len(urls)} URLs...")
    results = {}
    
    for url in urls:
        try:
            print(f"  Extracting from: {url}")
            response = await tavily_client.extract_content(url)
            results[url] = response
        except Exception as e:
            error_msg = f"Error extracting content from {url}: {e}"
            print(f"❌ {error_msg}")
            results[url] = error_msg
    
    return results


def create_agent(model, tools):
    """Create and return the personalized search agent."""
    return PersonalizedSearchAgent(model, tools)


def create_multi_agent_team(model, tools, personalization_context: str | None = None) -> MultiAgentTeam:
    """Create a multi-agent team with role-specific agents."""
    return MultiAgentTeam(model, tools, personalization_context)


async def run_agent(query: str, user_id: str = None):
    """Run the personalized search agent with the given query."""
    try:
        print(f"🤖 Personalized Search Agent is processing: {query}")
        print("=" * 60)
        
        # Set user for personalization
        agent.set_user(user_id)
        
        # Run the agent
        result = await agent.run(query)
        
        return result
        
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        return None


def print_user_management_help():
    """Print help for user management commands."""
    print("\n👥 User Management Commands:")
    print("=" * 40)
    print("--user-id <id>     : Set specific user ID for personalization")
    print("--list-users       : List all user profiles")
    print("--show-profile <id>: Show specific user profile")
    print("--update-profile <id> <field> <value> : Update user profile")
    print("--help             : Show this help message")
    print("\nExamples:")
    print("  python main.py --user-id user123 'Research AI trends'")
    print("  python main.py --list-users")
    print("  python main.py --show-profile user123")


def handle_user_commands(args):
    """Handle user management commands."""
    if "--help" in args:
        print_user_management_help()
        return None, None
    
    if "--list-users" in args:
        profiles = profile_manager.list_profiles()
        print("\n👥 User Profiles:")
        print("=" * 50)
        for profile in profiles:
            print(f"ID: {profile.user_id}")
            print(f"Name: {profile.name}")
            print(f"City: {profile.city}")
            print(f"Profession: {profile.profession}")
            print(f"Interests: {', '.join(profile.interests)}")
            print(f"Interactions: {profile.interaction_count}")
            print("-" * 30)
        return None, None
    
    if "--show-profile" in args:
        try:
            idx = args.index("--show-profile")
            if idx + 1 < len(args):
                user_id = args[idx + 1]
                profile = get_user_profile(user_id)
                if profile:
                    print(f"\n👤 Profile for {user_id}:")
                    print("=" * 40)
                    print(f"Name: {profile.name}")
                    print(f"City: {profile.city}")
                    print(f"Profession: {profile.profession}")
                    print(f"Interests: {', '.join(profile.interests)}")
                    print(f"Expertise: {profile.expertise_level}")
                    print(f"Preferred Topics: {', '.join(profile.preferred_topics)}")
                    print(f"Interactions: {profile.interaction_count}")
                else:
                    print(f"❌ User profile not found: {user_id}")
            else:
                print("❌ Please provide a user ID")
        except ValueError:
            print("❌ Invalid command format")
        return None, None
    
    if "--update-profile" in args:
        try:
            idx = args.index("--update-profile")
            if idx + 3 < len(args):
                user_id = args[idx + 1]
                field = args[idx + 2]
                value = args[idx + 3]
                
                if update_user_profile(user_id, **{field: value}):
                    print(f"✅ Updated {field} for user {user_id}")
                else:
                    print(f"❌ Failed to update profile for user {user_id}")
            else:
                print("❌ Please provide user ID, field, and value")
        except Exception as e:
            print(f"❌ Error updating profile: {e}")
        return None, None
    
    # Extract user ID if specified
    user_id = None
    if "--user-id" in args:
        try:
            idx = args.index("--user-id")
            if idx + 1 < len(args):
                user_id = args[idx + 1]
                # Remove the --user-id and user_id from args for the query
                args.pop(idx)
                args.pop(idx)
        except ValueError:
            pass

    # Team mode flag
    team_mode = False
    if "--team" in args:
        team_mode = True
        args.remove("--team")
    
    # Join remaining args as the query
    query = " ".join(args) if args else DEFAULT_QUERY

    return query, user_id, team_mode


def main():
    """Main function to run the personalized search agent."""
    try:
        # Load environment and create components
        print("🚀 Initializing Personalized Search AI Agent...")
        gemini_api_key, tavily_api_key = load_environment()
        
        global tavily_client
        tavily_client = create_tavily_client(tavily_api_key)
        
        provider = create_provider(gemini_api_key)
        model = create_model(provider)
        
        # Create tools and agent
        tools = [search, extract_content]
        global agent
        agent = create_agent(model, tools)
        
        print("✅ Personalized Search AI Agent initialized successfully!")
        
        # Handle command line arguments
        if len(sys.argv) > 1:
            query, user_id, team_mode = handle_user_commands(sys.argv[1:])
            
            if query is None:  # Command was handled, exit
                return
        else:
            query = DEFAULT_QUERY
            user_id = None
            team_mode = False
            print(f"📝 Using default query: {query}")
        
        # Run team or single agent
        if team_mode:
            # Build personalization context for writer
            personalization_context = get_user_context(user_id) if user_id else None
            team = create_multi_agent_team(model, tools, personalization_context)
            asyncio.run(team.run(query))
        else:
            asyncio.run(run_agent(query, user_id))
        
    except KeyboardInterrupt:
        print("\n👋 Search Agent stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("\n💡 Make sure you have set the required environment variables:")
        print("   - GEMINI_API_KEY")
        print("   - TAVILY_API_KEY")
        sys.exit(1)


if __name__ == "__main__":
    main()