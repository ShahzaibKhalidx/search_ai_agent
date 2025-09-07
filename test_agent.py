#!/usr/bin/env python3
"""
Test script for Personalized Search AI Agent
Run this to verify your setup is working correctly
"""

import asyncio
import sys
from config import validate_config, print_setup_instructions

def test_configuration():
    """Test if the configuration is valid."""
    print("🔧 Testing configuration...")
    
    # Load environment variables first
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    
    if not validate_config():
        print("❌ Configuration validation failed!")
        print_setup_instructions()
        return False
    
    print("✅ Configuration is valid!")
    return True

def test_imports():
    """Test if all required modules can be imported."""
    print("📦 Testing imports...")
    
    try:
        from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, ModelSettings
        from dotenv import load_dotenv, find_dotenv
        from tavily import AsyncTavilyClient
        print("✅ All required modules imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")
        return False

def test_environment_loading():
    """Test if environment variables can be loaded."""
    print("🌍 Testing environment loading...")
    
    try:
        from dotenv import load_dotenv, find_dotenv
        load_dotenv(find_dotenv())
        print("✅ Environment variables loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Environment loading error: {e}")
        return False

def test_user_profile_system():
    """Test the user profile and personalization system."""
    print("👤 Testing user profile system...")
    
    try:
        from user_profile import UserProfile, UserProfileManager, get_user_context, update_user_profile
        
        # Test profile creation
        profile = UserProfile("test_user")
        print("✅ UserProfile class created successfully")
        
        # Test profile manager
        manager = UserProfileManager("test_profiles.json")
        print("✅ UserProfileManager created successfully")
        
        # Test profile operations
        test_profile = manager.get_or_create_profile("test_user_123")
        print("✅ Profile creation/retrieval successful")
        
        # Test personalization context
        context = get_user_context("test_user_123")
        print("✅ Personalization context generated")
        
        # Test profile update
        success = update_user_profile("test_user_123", name="Test User")
        print("✅ Profile update successful")
        
        # Clean up test file
        import os
        if os.path.exists("test_profiles.json"):
            os.remove("test_profiles.json")
        
        print("✅ User profile system working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ User profile system test failed: {e}")
        return False

async def test_tavily_connection():
    """Test if Tavily API is accessible."""
    print("🔍 Testing Tavily API connection...")
    
    try:
        from tavily import AsyncTavilyClient
        from config import TAVILY_API_KEY
        
        client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
        
        # Try a simple search
        response = await client.search("test", max_results=1)
        print("✅ Tavily API connection successful!")
        return True
    except Exception as e:
        print(f"❌ Tavily API connection failed: {e}")
        return False

async def test_gemini_connection():
    """Test if Gemini API is accessible."""
    print("🤖 Testing Gemini API connection...")
    
    try:
        from agents import AsyncOpenAI
        from config import GEMINI_API_KEY, GEMINI_BASE_URL
        
        provider = AsyncOpenAI(
            api_key=GEMINI_API_KEY,
            base_url=GEMINI_BASE_URL,
        )
        
        print("✅ Gemini API connection successful!")
        return True
    except Exception as e:
        print(f"❌ Gemini API connection failed: {e}")
        return False

def test_personalized_agent():
    """Test the personalized search agent creation."""
    print("🎯 Testing personalized agent creation...")
    
    try:
        from main import PersonalizedSearchAgent, create_agent
        
        # Mock model and tools for testing
        class MockModel:
            pass
        
        class MockTools:
            pass
        
        # Test agent creation
        agent = create_agent(MockModel(), MockTools())
        print("✅ PersonalizedSearchAgent created successfully")
        
        # Test agent type
        if isinstance(agent, PersonalizedSearchAgent):
            print("✅ Agent is correct type")
        else:
            print("❌ Agent is not correct type")
            return False
        
        print("✅ Personalized agent system working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Personalized agent test failed: {e}")
        return False

async def run_tests():
    """Run all tests."""
    print("🧪 Running Personalized Search AI Agent tests...")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_configuration),
        ("Imports", test_imports),
        ("Environment", test_environment_loading),
        ("User Profile System", test_user_profile_system),
        ("Personalized Agent", test_personalized_agent),
        ("Tavily API", test_tavily_connection),
        ("Gemini API", test_gemini_connection),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Print results summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    print(f"Total: {total}, Passed: {passed}, Failed: {total - passed}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Personalized Search AI Agent is ready to use.")
        print("💡 Run 'python main.py' to start using the agent.")
        print("💡 Try personalization features:")
        print("   python main.py --user-id user123 'Research AI trends'")
        print("   python main.py --list-users")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before using the agent.")
        return False
    
    return True

def main():
    """Main function to run tests."""
    try:
        success = asyncio.run(run_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test runner failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 