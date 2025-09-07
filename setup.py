#!/usr/bin/env python3
"""
Setup script for Search AI Agent
This script helps you set up the environment and install dependencies
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print a welcome banner."""
    print("=" * 60)
    print("🚀 Welcome to Search AI Agent Setup!")
    print("=" * 60)
    print("This script will help you set up your Search AI Agent")
    print("and verify that everything is working correctly.")
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 13):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   This project requires Python 3.13 or higher")
        print("   Please upgrade your Python installation")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        # Try using pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies with pip: {e}")
        print("💡 Trying alternative installation methods...")
        
        try:
            # Try using uv if available
            subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], 
                          check=True, capture_output=True, text=True)
            print("✅ Dependencies installed successfully with uv!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Failed to install with uv as well")
            print("\n💡 Manual installation required:")
            print("   pip install -r requirements.txt")
            return False

def create_env_file():
    """Create a .env file template."""
    print("\n🌍 Setting up environment variables...")
    
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ {env_file} already exists")
        return True
    
    try:
        with open(env_file, "w") as f:
            f.write("# Search AI Agent Environment Variables\n")
            f.write("# Copy this file to .env and fill in your actual API keys\n\n")
            f.write("# Gemini API Key (Google AI)\n")
            f.write("# Get from: https://makersuite.google.com/app/apikey\n")
            f.write("GEMINI_API_KEY=your_gemini_api_key_here\n\n")
            f.write("# Tavily API Key\n")
            f.write("# Get from: https://tavily.com/\n")
            f.write("TAVILY_API_KEY=your_tavily_api_key_here\n")
        
        print(f"✅ Created {env_file} template")
        print("💡 Please edit this file and add your actual API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create {env_file}: {e}")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("=" * 60)
    print("1. Edit the .env file and add your API keys:")
    print("   - GEMINI_API_KEY: Get from https://makersuite.google.com/app/apikey")
    print("   - TAVILY_API_KEY: Get from https://tavily.com/")
    print()
    print("2. Test your setup:")
    print("   python test_agent.py")
    print()
    print("3. Run the Search AI Agent:")
    print("   python main.py")
    print()
    print("4. Or run with a custom query:")
    print("   python main.py 'Your search query here'")
    print()
    print("💡 For more information, see README.md")
    print("=" * 60)

def main():
    """Main setup function."""
    try:
        print_banner()
        
        # Check Python version
        if not check_python_version():
            sys.exit(1)
        
        # Install dependencies
        if not install_dependencies():
            print("\n⚠️  Setup incomplete due to dependency installation failure")
            print("   Please install dependencies manually and try again")
            sys.exit(1)
        
        # Create environment file
        create_env_file()
        
        # Print next steps
        print_next_steps()
        
        print("\n🎉 Setup completed successfully!")
        print("   Your Search AI Agent is ready to be configured!")
        
    except KeyboardInterrupt:
        print("\n👋 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 