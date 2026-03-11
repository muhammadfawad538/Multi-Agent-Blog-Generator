import os
import logging
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from support_team_models import SupportContext
from support_agents import (
    intent_agent, knowledge_agent, solution_agent,
    escalation_agent, response_agent,
    filter_context_for_intent_agent, filter_context_for_knowledge_agent,
    filter_context_for_solution_agent, filter_context_for_escalation_agent,
    filter_context_for_response_agent
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
set_tracing_disabled(True)

# Create an async OpenAI client pointing to Google's endpoint
gemini_client = AsyncOpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Create a model using Gemini
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=gemini_client
)

def run_support_workflow(customer_query: str) -> SupportContext:
    """
    Run the complete customer support workflow with context filtering
    """
    logger.info(f"Starting support workflow for query: {customer_query}")

    # Initialize context
    context = SupportContext(
        customer_query=customer_query,
        conversation_history=[{"role": "customer", "message": customer_query}]
    )

    # Step 1: Intent Detection
    logger.info("Running Intent Detection Agent...")
    filtered_context = filter_context_for_intent_agent(context)
    intent_prompt = f"Analyze this customer query and detect the intent: {filtered_context['customer_query']}"

    intent_result = Runner.run_sync(intent_agent, intent_prompt)
    context.intent = intent_result.final_output.strip().lower()
    logger.info(f"Detected intent: {context.intent}")

    # Step 2: Knowledge Retrieval
    logger.info("Running Knowledge Retrieval Agent...")
    filtered_context = filter_context_for_knowledge_agent(context)
    knowledge_prompt = f"Retrieve relevant knowledge documents for intent '{filtered_context['intent']}' related to query: {filtered_context['customer_query']}"

    knowledge_result = Runner.run_sync(knowledge_agent, knowledge_prompt)
    # In a real implementation, this would return structured knowledge documents
    context.knowledge_docs = [{"title": "Relevant Article", "content": knowledge_result.final_output, "relevance_score": 0.9}]

    # Step 3: Solution Generation
    logger.info("Running Solution Generation Agent...")
    filtered_context = filter_context_for_solution_agent(context)
    solution_prompt = f"Generate a solution for intent '{filtered_context['intent']}' using these knowledge documents: {filtered_context['knowledge_docs'][:2]} and query: {filtered_context['customer_query']}"

    solution_result = Runner.run_sync(solution_agent, solution_prompt)
    context.solution = solution_result.final_output

    # Step 4: Escalation Decision
    logger.info("Running Escalation Agent...")
    filtered_context = filter_context_for_escalation_agent(context)
    escalation_prompt = f"Determine if this issue needs escalation. Intent: {filtered_context['intent']}, Solution: {filtered_context['solution'][:200]}, Query: {filtered_context['customer_query'][:200]}"

    escalation_result = Runner.run_sync(escalation_agent, escalation_prompt)
    # Parse the escalation decision (in a real system this would be more structured)
    escalation_text = escalation_result.final_output.lower()
    context.escalation_required = "yes" in escalation_text or "true" in escalation_text or "escalate" in escalation_text

    # Step 5: Response Generation
    logger.info("Running Response Agent...")
    filtered_context = filter_context_for_response_agent(context)
    response_prompt = f"Create a final response. Solution: {filtered_context['solution'][:300]}, Escalation required: {context.escalation_required}, Query: {filtered_context['customer_query'][:200]}"

    response_result = Runner.run_sync(response_agent, response_prompt)
    context.response = response_result.final_output

    logger.info("Support workflow completed successfully!")
    return context

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python support_team_main.py \"Customer complaint or question\"")
        print("Example: python support_team_main.py \"I'm having trouble logging into my account\"")
        sys.exit(1)

    customer_query = " ".join(sys.argv[1:])

    try:
        result = run_support_workflow(customer_query)

        print("\n" + "="*60)
        print("CUSTOMER SUPPORT RESULT")
        print("="*60)
        print(f"QUERY: {result.customer_query}")
        print(f"INTENT: {result.intent}")
        print(f"ESCALATION REQUIRED: {result.escalation_required}")
        print(f"\nRESPONSE:\n{result.response}")
        print("="*60)

    except Exception as e:
        logger.error(f"Error during support workflow: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()