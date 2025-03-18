# Deep Research Agent with OpenAI Agents SDK and Firecrawl

A powerful research assistant that leverages OpenAI's Agents SDK and Firecrawl's deep research capabilities to perform comprehensive web research on any topic and any question.

## Features

- **Deep Web Research**: Automatically searches the web, extracts content, and synthesizes findings
- **Enhanced Analysis**: Uses OpenAI's Agents SDK to elaborate on research findings with additional context and insights
- **Interactive UI**: Clean Streamlit interface for easy interaction
- **Downloadable Reports**: Export research findings as markdown files

## Architecture

The project is organized into the following structure:

```
deep-research-assistant/
│
├── app/
│   └── main.py                # Main Streamlit application
│
├── utils/
│   ├── research_tools.py      # Utility functions for research
│   └── config.py              # Configuration management
│
├── models/
│   ├── agents.py              # Agent creation and management
│
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

- **app/main.py**: Contains the Streamlit application logic.
- **utils/**: Includes utility functions and configuration management.
- **models/**: Contains agent creation and management logic.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/deep-research-assistant.git
   cd deep-research-assistant
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app/main.py
   ```

2. Enter your API keys in the sidebar:
   - OpenAI API key
   - Firecrawl API key

3. Enter your research topic in the main input field

4. Click "Start Research" and wait for the process to complete

5. View and download your enhanced research report

## Deployment Strategy

To deploy the Streamlit app, you can use Streamlit Sharing or any cloud platform that supports Python applications.

### Streamlit Sharing

1. Push your project to a GitHub repository.
2. Sign up for Streamlit Sharing and link your GitHub account.
3. Deploy the app by selecting the repository and specifying the `app/main.py` file as the entry point.

### Other Platforms

- **Heroku**: Use a `Procfile` to specify the command to run the app.
- **AWS**: Deploy using Elastic Beanstalk or Lambda with API Gateway.
- **Docker**: Containerize the app and deploy on any container orchestration platform.

Ensure that your API keys are securely managed and not hardcoded in the source code.

## Example Research Topics

- "Latest developments in quantum computing"
- "Impact of climate change on marine ecosystems"
- "Advancements in renewable energy storage"
- "Ethical considerations in artificial intelligence"
- "Emerging trends in remote work technologies"

## Technical Details

The application uses two specialized agents:

1. **Research Agent**: Utilizes Firecrawl's deep research endpoint to gather comprehensive information from multiple web sources.

2. **Elaboration Agent**: Enhances the initial research by adding detailed explanations, examples, case studies, and practical implications.

The Firecrawl deep research tool performs multiple iterations of web searches, content extraction, and analysis to provide thorough coverage of the topic.

## Privacy & Ethics

This tool uses your own API keys and runs on your infrastructure. No research data is stored on our servers. All research is conducted ethically, with proper attribution to original sources.

## About the Creator

ResearchGenius AI was created to democratize access to high-quality research capabilities. In a world where premium research services can cost hundreds of dollars per month, this tool provides similar capabilities using your own API keys at a fraction of the cost.

# Footer

© 2025 ResearchGenius AI. Built with OpenAI Agents SDK and Firecrawl.

