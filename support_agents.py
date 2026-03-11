import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled, handoff
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from support_team_models import SupportContext

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

def filter_context_for_intent_agent(context: SupportContext) -> dict:
    """Filter context to only include fields needed by the intent detection agent"""
    return {
        "customer_query": context.customer_query,
        "conversation_history": context.conversation_history[-3:] if context.conversation_history else []  # Last 3 exchanges
    }

def filter_context_for_knowledge_agent(context: SupportContext) -> dict:
    """Filter context to only include fields needed by the knowledge retrieval agent"""
    return {
        "intent": context.intent,
        "customer_query": context.customer_query
    }

def filter_context_for_solution_agent(context: SupportContext) -> dict:
    """Filter context to only include fields needed by the solution generation agent"""
    return {
        "intent": context.intent,
        "knowledge_docs": context.knowledge_docs,
        "customer_query": context.customer_query
    }

def filter_context_for_escalation_agent(context: SupportContext) -> dict:
    """Filter context to only include fields needed by the escalation agent"""
    return {
        "intent": context.intent,
        "solution": context.solution,
        "customer_query": context.customer_query,
        "knowledge_docs": context.knowledge_docs
    }

def filter_context_for_response_agent(context: SupportContext) -> dict:
    """Filter context to only include fields needed by the response agent"""
    return {
        "solution": context.solution,
        "response": context.response,
        "customer_query": context.customer_query,
        "conversation_history": context.conversation_history[-2:] if context.conversation_history else []
    }

# Intent Detection Agent
intent_agent = Agent(
    name="Intent Detection Agent",
    instructions="""You are an intent detection specialist. Your job is to analyze the customer's query and determine the intent.
    Possible intents are:
    - billing_issue: Questions about charges, payments, invoices, subscriptions
    - refund_request: Requests for refunds or chargebacks
    - login_problem: Issues with account access, passwords, authentication
    - bug_report: Reports of software bugs or technical issues
    - general_question: General inquiries about products or services

    Respond with just the detected intent as a single word. After determining the intent, hand off to the Knowledge Retrieval Agent.""",
    model=gemini_model
)

# Knowledge Retrieval Agent
knowledge_agent = Agent(
    name="Knowledge Retrieval Agent",
    instructions="""You are a knowledge retrieval specialist. Your job is to search the knowledge base for relevant documents based on the detected intent.
    Use the customer query and intent to find the most relevant articles, guides, or solutions.
    Return the relevant documents as a list of dictionaries containing 'title', 'content', and 'relevance_score'.
    After retrieving knowledge, hand off to the Solution Generation Agent.""",
    model=gemini_model
)

# Solution Generation Agent
solution_agent = Agent(
    name="Solution Generation Agent",
    instructions="""You are a solution generation specialist. Your job is to create a helpful solution based on the intent and retrieved knowledge documents.
    Create a clear, actionable solution that addresses the customer's specific issue.
    Consider the customer's query and the knowledge documents when crafting your solution.
    After generating a solution, hand off to the Escalation Agent.""",
    model=gemini_model
)

# Escalation Agent
escalation_agent = Agent(
    name="Escalation Agent",
    instructions="""You are an escalation specialist. Your job is to determine if the issue needs to be escalated to a human agent.
    Escalate if:
    - The customer is angry or upset
    - The issue involves sensitive information
    - The solution requires human verification
    - The customer specifically requests to speak with a human
    - The issue is complex and the knowledge base doesn't provide adequate solutions

    Set escalation_required to true if escalation is needed, otherwise false.
    After making the escalation decision, hand off to the Response Agent.""",
    model=gemini_model
)

# Response Agent
response_agent = Agent(
    name="Response Agent",
    instructions="""You are a response specialist. Your job is to craft the final response to the customer.
    If escalation is required, create a polite response explaining that a human agent will contact them shortly.
    If no escalation is needed, create a helpful response that includes the solution.
    Ensure the response is empathetic, professional, and directly addresses the customer's query.
    Add the final response to the context and complete the interaction.""",
    model=gemini_model
)