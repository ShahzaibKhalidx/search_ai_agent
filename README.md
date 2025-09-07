# Personalized Search AI Agent 🤖🔍👤

An intelligent AI agent that can search the web and extract information using current knowledge, with **personalization capabilities** that remember user preferences and tailor responses accordingly. Built with Gemini AI and Tavily search APIs.

## Features ✨

- **Web Search**: Search the internet for current information using Tavily's powerful search API
- **Content Extraction**: Extract detailed content from specific URLs
- **Intelligent Synthesis**: AI-powered analysis and synthesis of search results
- **Real-time Information**: Access to the latest information from the web
- **🎯 PERSONALIZATION**: Remember user preferences and tailor responses
- **User Profiles**: Persistent storage of user interests, profession, and expertise level
- **Context Memory**: Track interaction history and build understanding over time
- **Command Line Interface**: Easy-to-use CLI with personalization commands
- **Error Handling**: Robust error handling and user-friendly error messages

## Personalization Features 🎯

### Local Context & User Memory
- **User Profiles**: Automatically create and manage user profiles with mock data
- **Persistent Storage**: Save user preferences in JSON files for future sessions
- **Rich Context**: Include name, city, profession, interests, expertise level, and preferred topics
- **Dynamic Instructions**: Agent adapts responses based on user background and preferences

### How Personalization Works
1. **First Turn**: Agent creates a user profile with realistic mock data
2. **Subsequent Turns**: Agent prepends personalized instructions like:
   > "You're helping Alex from San Francisco who works as a Data Scientist who likes artificial intelligence, machine learning, data science with intermediate expertise and prefers topics like AI and machine learning, web development. Personalize examples and explanations accordingly."

3. **Tailored Responses**: 
   - Examples relevant to user's profession and interests
   - Technical depth matching expertise level
   - Location-specific references when relevant
   - Industry-specific insights

## Prerequisites 📋

- Python 3.13 or higher
- Gemini API key
- Tavily API key

## Installation 🚀

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd search_agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```
   
   Or set them directly in your environment:
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   export TAVILY_API_KEY="your_tavily_api_key_here"
   ```

## Usage 💻

### Basic Usage

Run the agent with a default query:
```bash
python main.py
```

### Personalized Usage

Search with user personalization:
```bash
python main.py --user-id user123 "Research recent developments in AI"
```

### User Management Commands

```bash
# List all user profiles
python main.py --list-users

# Show specific user profile
python main.py --show-profile user123

# Update user profile
python main.py --update-profile user123 name "Alex Johnson"
python main.py --update-profile user123 city "San Francisco"
python main.py --update-profile user123 profession "Data Scientist"

# Get help
python main.py --help
```

### Examples

```bash
# Generic search (no personalization)
python main.py "Research recent developments in AI"

# Personalized search (with user context)
python main.py --user-id user123 "Research recent developments in AI"

# Create new user profile automatically
python main.py --user-id newuser "What are quantum computing basics?"

# Update user preferences
python main.py --update-profile user123 interests "AI, blockchain, cybersecurity"
python main.py --update-profile user123 expertise_level "expert"
```

## How It Works 🔧

1. **Query Processing**: The agent receives your search query
2. **User Context**: Retrieves or creates user profile for personalization
3. **Personalized Instructions**: Generates context-aware instructions for the AI
4. **Web Search**: Uses Tavily API to search the web for relevant information
5. **Content Extraction**: Extracts detailed content from the most relevant URLs
6. **AI Analysis**: Gemini AI analyzes and synthesizes information with personalization
7. **Response Generation**: Provides a comprehensive, personalized answer
8. **Context Update**: Tracks interaction and updates user profile

## Personalization Benefits ✨

### 🎯 Tailored Responses
- Examples relevant to your profession and interests
- Technical depth matching your expertise level
- References to your location when relevant

### 🧠 Context Memory
- Remembers your preferences across sessions
- Builds understanding of your interests over time
- Tracks interaction history for better context

### 🔍 Relevant Suggestions
- Suggests topics aligned with your preferences
- Adapts explanations to your background
- Provides industry-specific insights

### 📊 Profile Management
- Easy profile creation and updates
- Persistent storage of preferences
- Multiple user support

## API Keys Setup 🔑

### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### Tavily API Key
1. Visit [Tavily](https://tavily.com/)
2. Sign up for an account
3. Get your API key from the dashboard
4. Add it to your `.env` file

## Project Structure 📁

```
search_agent/
├── main.py              # Main application with personalization
├── user_profile.py      # User profile management system
├── config.py            # Configuration and settings
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Project configuration
├── README.md           # This file
├── test_agent.py       # Testing suite
├── setup.py            # Setup automation
├── examples.py         # Usage examples
└── .env                # Environment variables (create this)
```

## Configuration ⚙️

The agent can be configured by modifying the `config.py` file:

- **Model Settings**: Temperature, max tokens, model name
- **Search Settings**: Default results count, default query
- **Personalization**: User profile fields and mock data options

## Testing 🧪

Test your setup with the comprehensive test suite:

```bash
python test_agent.py
```

This will test:
- Configuration validation
- Module imports
- Environment loading
- User profile system
- Personalized agent creation
- API connections

## Error Handling 🛡️

The agent includes comprehensive error handling for:
- Missing API keys
- Network connectivity issues
- API rate limits
- Invalid URLs
- Search failures
- User profile errors

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

If you encounter any issues:
1. Check that your API keys are correctly set
2. Verify your internet connection
3. Check the API service status
4. Run the test suite: `python test_agent.py`
5. Open an issue in the repository

## Roadmap 🗺️

- [x] Add personalization with user profiles
- [x] Implement local context memory
- [x] User profile management system
- [ ] Add support for more search engines
- [ ] Implement result caching
- [ ] Add web interface
- [ ] Support for file uploads and analysis
- [ ] Integration with other AI models
- [ ] Advanced filtering and sorting options
- [ ] Multi-language support
- [ ] Voice interface integration