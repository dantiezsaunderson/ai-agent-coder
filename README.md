# Multi-Skill Super-Agent

A modular multi-skill super-agent using Python for personal automation, with a unified Telegram bot interface.

## Features

- **Code Generation Agent**: Generates Python code based on natural language descriptions
- **Image Generation Agent**: Creates images using DALL·E 3 or other image generation APIs
- **Web Research & Summarizer Agent**: Searches the web, scrapes content, and provides summaries
- **Task Automation Agent**: Handles recurring tasks, reminders, and system triggers
- **Personal Assistant Agent**: Manages calendar events, drafts emails, and creates summaries

## Architecture

The system follows a modular architecture with the following key components:

1. **Interface Layer**: Telegram Bot Interface with command handlers
2. **Orchestration Layer**: Agent Router and Factory for directing requests
3. **Agent Modules**: Specialized agents for different tasks
4. **Persistence Layer**: Database for task history and agent state

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package manager)
- Git (for version control)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/dantiezsaunderson/ai-agent-coder.git
   cd ai-agent-coder
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the template:
   ```bash
   cp .env.template .env
   ```

5. Edit the `.env` file with your API keys and configuration settings.

## Usage

### Starting the Agent

Run the main application:

```bash
python main.py
```

### Telegram Bot Commands

- `/start` - Initialize the bot and get welcome message
- `/help` - Display available commands and usage information
- `/code <description>` - Generate Python code based on your description
- `/image <description>` - Generate an image based on your description
- `/research <topic>` - Research a topic on the web and provide a summary

### Examples

#### Code Generation
```
/code create a function to calculate fibonacci numbers recursively
```

#### Image Generation
```
/image a futuristic city with flying cars and neon lights
```

#### Web Research
```
/research latest developments in quantum computing
```

## API Integrations

The system integrates with various APIs to provide its functionality:

### AI Model APIs
- **OpenAI API**: Used for code generation and text processing
- **Claude API**: Alternative AI model for text generation
- **DeepSeek API**: Additional AI model option

### Image Generation
- **DALL·E 3**: Via OpenAI API for image generation
- **Stability AI**: Optional integration for alternative image generation

### Development & Deployment
- **GitHub API**: For code repository management
- **Render API**: For deployment automation

### Cryptocurrency APIs
- **Ethereum API**: For Ethereum blockchain integration
- **Solana API**: For Solana blockchain integration

## Configuration

All configuration is managed through environment variables in the `.env` file:

### Required Configuration
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `OPENAI_API_KEY`: Your OpenAI API key

### Optional Configuration
- `CLAUDE_API_KEY`: Anthropic Claude API key
- `DEEPSEEK_API_KEY`: DeepSeek API key
- `GITHUB_TOKEN`: GitHub personal access token
- `GITHUB_REPO`: GitHub repository name
- `RENDER_API_KEY`: Render API key
- `ETHEREUM_API_KEY`: Ethereum API key
- `SOLANA_API_KEY`: Solana API key

## Extending the Agent

The modular architecture makes it easy to add new capabilities:

1. Create a new agent class in `src/agents/` that inherits from `base_agent.py`
2. Implement the `process()` method to handle requests
3. Add a routing method in `src/orchestration/router.py`
4. Add a factory method in `src/orchestration/agent_factory.py`
5. Add command handler in `src/interface/telegram_bot.py`

## Testing

Run the test suite to verify functionality:

```bash
python -m tests.test_agents
python -m tests.test_telegram
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Python, LangChain, and python-telegram-bot
- Uses OpenAI, Claude, and DeepSeek for AI capabilities
