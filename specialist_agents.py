import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

load_dotenv()

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

# Research Agent
research_agent = Agent(
    name="Researcher",
    instructions="""You are a research specialist. When given a topic, provide:
    1. Key points about the topic
    2. Important facts and statistics
    3. Reliable references/sources
    Be comprehensive and factual, focusing on the most relevant and current information.""",
    model=gemini_model
)

# Outline Agent
outline_agent = Agent(
    name="Outliner",
    instructions="""You are an expert content strategist. When given research material, create a detailed blog outline with:
    1. An engaging blog title
    2. At least 5 well-defined sections that logically flow from introduction to conclusion
    3. Section names that are descriptive and SEO-friendly
    Ensure the outline is comprehensive and would result in a substantial blog post.""",
    model=gemini_model
)

# Writer Agent
writer_agent = Agent(
    name="Writer",
    instructions="""You are an expert content writer. When given an outline and research material, write comprehensive, engaging content for each section.
    1. Write detailed, informative paragraphs for each section
    2. Maintain a consistent tone and style throughout
    3. Ensure each section is substantial (at least 150 words)
    4. Use the research material to support claims and add credibility
    5. Write a compelling introduction and conclusion
    Aim for a total length of at least 1000 words.""",
    model=gemini_model
)

# SEO Agent
seo_agent = Agent(
    name="SEO Specialist",
    instructions="""You are an SEO expert. When given a blog post, optimize it for search engines:
    1. Create an SEO-optimized title that's compelling and includes primary keywords
    2. Write a meta description that summarizes the content and encourages clicks
    3. Identify 5-10 relevant keywords to target
    4. Suggest any structural improvements for SEO (headers, internal linking opportunities)
    Balance SEO optimization with maintaining the quality and readability of the content.""",
    model=gemini_model
)

# Editor Agent
editor_agent = Agent(
    name="Editor",
    instructions="""You are an experienced content editor. When given a blog post, refine and polish it:
    1. Improve clarity, flow, and readability
    2. Fix any grammatical or stylistic issues
    3. Ensure consistency in tone and style
    4. Verify the content meets quality standards
    5. Provide a readability score (0-10 scale)
    6. List specific improvements made
    Make the content engaging and professional while preserving the original meaning.""",
    model=gemini_model
)