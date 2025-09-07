#!/usr/bin/env python3
"""
Examples of using the Personalized Search AI Agent
This file shows different ways to use the agent for various types of searches with personalization
"""

import asyncio
from main import create_agent, create_model, create_provider, create_tavily_client, load_environment

async def example_research_topic():
    """Example: Research a specific topic."""
    print("🔬 Example: Researching a specific topic")
    print("=" * 50)
    
    query = "What are the latest developments in quantum computing and their potential applications?"
    
    try:
        # Initialize the agent
        gemini_api_key, tavily_api_key = load_environment()
        tavily_client = create_tavily_client(tavily_api_key)
        provider = create_provider(gemini_api_key)
        model = create_model(provider)
        tools = []  # We'll import these from main
        agent = create_agent(model, tools)
        
        print(f"Query: {query}")
        print("Running agent...")
        
        # Note: This is a simplified example - in practice, you'd use the main.py
        print("💡 This example shows the structure. Run 'python main.py' for full functionality.")
        
    except Exception as e:
        print(f"❌ Example failed: {e}")

def print_example_queries():
    """Print example queries users can try."""
    print("📝 Example Queries You Can Try:")
    print("=" * 50)
    
    examples = [
        "Research recent breakthroughs in renewable energy technology",
        "What are the latest developments in AI and machine learning?",
        "Find information about current space exploration missions",
        "Research best practices for cybersecurity in 2024",
        "What are the emerging trends in blockchain technology?",
        "Research recent developments in quantum computing",
        "Find information about sustainable agriculture practices",
        "Research the latest developments in electric vehicle technology",
        "What are the current trends in remote work and productivity?",
        "Research recent breakthroughs in medical technology"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i:2}. {example}")
    
    print("\n💡 Usage:")
    print("   python main.py 'Your query here'")
    print("   python main.py 'Research recent developments in AI'")

def print_personalization_examples():
    """Print examples of personalization features."""
    print("\n🎯 Personalization Examples:")
    print("=" * 50)
    
    print("1. **Personalized Search with User ID:**")
    print("   python main.py --user-id user123 'Research AI trends'")
    print("   → Agent will remember user123's preferences and tailor responses")
    
    print("\n2. **Create New User Profile:**")
    print("   python main.py --user-id newuser 'What are quantum computing basics?'")
    print("   → Automatically creates profile with mock data and personalizes responses")
    
    print("\n3. **Update User Profile:**")
    print("   python main.py --update-profile user123 name 'Alex Johnson'")
    print("   python main.py --update-profile user123 city 'San Francisco'")
    print("   python main.py --update-profile user123 profession 'Data Scientist'")
    
    print("\n4. **View User Profiles:**")
    print("   python main.py --list-users")
    print("   python main.py --show-profile user123")
    
    print("\n5. **Personalized vs Generic Search:**")
    print("   # Generic search (no personalization)")
    print("   python main.py 'Research machine learning'")
    print("   # Personalized search (with user context)")
    print("   python main.py --user-id user123 'Research machine learning'")

def print_advanced_usage():
    """Print advanced usage examples."""
    print("\n🚀 Advanced Usage Examples:")
    print("=" * 50)
    
    print("1. **Research with specific focus:**")
    print("   python main.py --user-id user123 'Research recent developments in AI, focusing on practical applications and industry trends'")
    
    print("\n2. **Comparative research with personalization:**")
    print("   python main.py --user-id user123 'Compare the latest developments in electric vehicles vs hydrogen fuel cell technology'")
    
    print("\n3. **Technical deep-dive with expertise level:**")
    print("   python main.py --user-id user123 'Research best practices for microservices architecture in 2024, including security considerations'")
    
    print("\n4. **Current events research with location context:**")
    print("   python main.py --user-id user123 'What are the latest developments in space exploration and upcoming missions?'")
    
    print("\n5. **Industry trend analysis with professional context:**")
    print("   python main.py --user-id user123 'Research emerging trends in fintech and their impact on traditional banking'")

def print_personalization_benefits():
    """Print the benefits of personalization."""
    print("\n✨ Personalization Benefits:")
    print("=" * 50)
    
    print("🎯 **Tailored Responses:**")
    print("   - Examples relevant to your profession and interests")
    print("   - Technical depth matching your expertise level")
    print("   - References to your location when relevant")
    
    print("\n🧠 **Context Memory:**")
    print("   - Remembers your preferences across sessions")
    print("   - Builds understanding of your interests over time")
    print("   - Tracks interaction history for better context")
    
    print("\n🔍 **Relevant Suggestions:**")
    print("   - Suggests topics aligned with your preferences")
    print("   - Adapts explanations to your background")
    print("   - Provides industry-specific insights")
    
    print("\n📊 **Profile Management:**")
    print("   - Easy profile creation and updates")
    print("   - Persistent storage of preferences")
    print("   - Multiple user support")

def print_user_management_commands():
    """Print all available user management commands."""
    print("\n👥 User Management Commands:")
    print("=" * 50)
    
    commands = [
        ("--user-id <id>", "Set specific user ID for personalization"),
        ("--list-users", "List all user profiles"),
        ("--show-profile <id>", "Show specific user profile"),
        ("--update-profile <id> <field> <value>", "Update user profile field"),
        ("--help", "Show help message")
    ]
    
    for cmd, desc in commands:
        print(f"{cmd:35} : {desc}")
    
    print("\n📝 Profile Fields You Can Update:")
    fields = [
        "name", "city", "profession", "expertise_level", 
        "interests", "preferred_topics"
    ]
    print("   " + ", ".join(fields))

def main():
    """Main function to run examples."""
    print("🎯 Personalized Search AI Agent Examples")
    print("=" * 70)
    
    # Print example queries
    print_example_queries()
    
    # Print personalization examples
    print_personalization_examples()
    
    # Print advanced usage
    print_advanced_usage()
    
    # Print personalization benefits
    print_personalization_benefits()
    
    # Print user management commands
    print_user_management_commands()
    
    print("\n" + "=" * 70)
    print("💡 To run these examples:")
    print("1. Make sure you have set up your API keys in .env")
    print("2. Run: python main.py 'Your query here'")
    print("3. Try personalization: python main.py --user-id user123 'Your query'")
    print("4. Or run with default query: python main.py")
    print("5. Test your setup: python test_agent.py")
    print("=" * 70)

if __name__ == "__main__":
    main() 