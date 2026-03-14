# Multi-Agent Blog Generator

A production-quality multi-agent system that implements the Orchestrator Pattern using the OpenAI Agents SDK. This system generates high-quality blog posts by orchestrating multiple specialist agents.

## 🚀 Features

- **Orchestrator Pattern**: Central manager agent coordinates specialist agents
- **Five Specialist Agents**:
  - Research Agent: Gathers information and facts
  - Outline Agent: Creates structured blog outlines
  - Writer Agent: Generates content for each section
  - SEO Agent: Optimizes content for search engines
  - Editor Agent: Polishes and refines the final content
- **Structured Data Flow**: Pydantic models ensure consistent data exchange
- **Quality Validation**: Decision logic validates outputs and re-executes if needed
- **API Integration**: Compatible with Google Gemini API

## 🏗️ Architecture

```
User Topic → Research Agent → Outline Agent → Writer Agent → SEO Agent → Editor Agent → Final Blog
```

### Decision Logic
- Ensures outline has at least 5 sections
- Ensures blog length exceeds 800 words
- Re-runs writer agent if content is too short
- Always runs editor as the final step

## 📁 Project Structure

```
├── main.py              # Orchestrator that manages the complete workflow
├── models.py           # Pydantic models for structured data flow
├── specialist_agents.py # Five specialist agents
├── orchestrator_pattern.py # Demonstrates as_tool functionality
├── agent_as_tool_example.py # Additional examples of agent tools
├── test_system.py      # Validates the system models
├── test_agent.py       # Tests the agent functionality
└── pyproject.toml      # Project dependencies
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/muhammadfawad538/Multi-Agent-Blog-Generator.git
cd Multi-Agent-Blog-Generator
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
Create a `.env` file in the root directory and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## 🚀 Usage

Generate a blog post with a specific topic:

```bash
python main.py "Your Blog Topic Here"
```

Example:
```bash
python main.py "The Future of Artificial Intelligence"
```

## 🧩 Pydantic Models

The system uses structured Pydantic models for data consistency:

- `ResearchOutput`: Topic, key points, facts, references
- `OutlineOutput`: Blog title, sections
- `WriterOutput`: Title, section contents
- `SEOOutput`: SEO title, meta description, keywords
- `EditorOutput`: Final blog, readability score, improvements
- `FinalBlogOutput`: Complete blog with SEO information

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License.

## Additional Component: Autonomous AI Customer Support Team

This repository also includes an advanced multi-agent system that collaborates to solve customer support issues using a shared context object and agent-to-agent handoffs with optimized context filtering, comprehensive guardrails, and persistent session memory.

### Support Team Features:
- **Distributed Architecture**: Five specialized agents collaborate without a central orchestrator
- **Context Filtering**: Each agent receives only the minimal context needed for its task
- **Token Efficiency**: Reduces token usage by filtering irrelevant information
- **Complete Workflow**: End-to-end support from query to resolution
- **Intelligent Escalation**: Automatic escalation to human agents when needed
- **Security Guardrails**: Input/output validation to prevent PII exposure and prompt injection
- **Persistent Sessions**: Customer context and conversation history maintained across interactions
- **Ticket Management**: Automatic ticket creation and tracking

### Support Team Architecture:
```
Customer Query → Intent Detection → Knowledge Retrieval → Solution Generation → Escalation Decision → Response Generation
```

The Autonomous AI Customer Support Team is located in the support-team related files within this repository.