# Autonomous AI Customer Support Team

An advanced multi-agent system that collaborates to solve customer support issues using a shared context object and agent-to-agent handoffs with optimized context filtering, comprehensive guardrails, and persistent session memory.

## 🚀 Features

- **Distributed Architecture**: Five specialized agents collaborate without a central orchestrator
- **Context Filtering**: Each agent receives only the minimal context needed for its task
- **Token Efficiency**: Reduces token usage by filtering irrelevant information
- **Complete Workflow**: End-to-end support from query to resolution
- **Intelligent Escalation**: Automatic escalation to human agents when needed
- **Security Guardrails**: Input/output validation to prevent PII exposure and prompt injection
- **Persistent Sessions**: Customer context and conversation history maintained across interactions
- **Ticket Management**: Automatic ticket creation and tracking

## 🏗️ Architecture

```
Customer Query → Intent Detection → Knowledge Retrieval → Solution Generation → Escalation Decision → Response Generation
```

### Agent Responsibilities

1. **Intent Detection Agent**: Identifies the customer's issue category
2. **Knowledge Retrieval Agent**: Finds relevant documentation
3. **Solution Generation Agent**: Creates tailored solutions
4. **Escalation Agent**: Determines if human intervention is needed
5. **Response Agent**: Crafts the final customer response

### Security Features

- **PII Detection**: Blocks sensitive information like credit cards, SSNs, and phone numbers
- **Injection Prevention**: Detects prompt injection attempts and malicious instructions
- **Output Protection**: Prevents accidental disclosure of internal data

### Session Management

- **Persistent Context**: Customer data saved between interactions
- **Conversation History**: Maintains context across sessions
- **Ticket Tracking**: Unique ticket IDs for each support request
- **Multi-User Isolation**: Separate sessions for different customers

## 📁 Project Structure

```
├── support_team_models.py    # Pydantic models for shared context
├── support_agents.py        # Specialist agents with context filters
├── support_guardrails.py    # Security guardrails for input/output validation
├── support_sessions.py      # Session management and persistent storage
├── support_team_main.py     # Main workflow orchestrator
├── run_support.bat          # Windows batch file for easy execution
└── README.md              # This file
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/support-desk-agent.git
cd support-desk-agent
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

Process a customer query:

```bash
python support_team_main.py "Customer complaint or question here" [customer_id]
```

Examples:
```bash
python support_team_main.py "I'm having trouble logging into my account" user123
python support_team_main.py "I forgot my password" user456
```

## 🧩 Context Optimization

The system implements context filtering to minimize token usage:

- `filter_context_for_intent_agent()`: Only passes customer query
- `filter_context_for_knowledge_agent()`: Only passes intent and query
- `filter_context_for_solution_agent()`: Only passes intent, docs, and query
- `filter_context_for_escalation_agent()`: Only passes relevant decision factors
- `filter_context_for_response_agent()`: Only passes solution and conversation history

## 🛡️ Security Features

### Input Guardrails
- PII Detection: Blocks credit cards, SSNs, phone numbers, emails
- Injection Prevention: Detects prompt injection attempts

### Output Guardrails
- Secret Protection: Blocks API keys, passwords, internal IPs
- Data Leakage Prevention: Prevents accidental disclosure

## 🔄 Session Management

The system maintains persistent sessions allowing customers to:
- Resume conversations across different interactions
- Maintain ticket history
- Access previous support resolutions
- Have personalized experiences based on past interactions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License.