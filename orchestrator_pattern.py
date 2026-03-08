"""
Demonstration of the Orchestrator Pattern with as_tool() functionality

This file shows how the system would work when the agents library supports the as_tool() function,
which converts agents into callable tools that can be orchestrated by a manager agent.
"""

import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, set_tracing_disabled
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from models import ResearchOutput, OutlineOutput, WriterOutput, SEOOutput, EditorOutput, FinalBlogOutput

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

# Research Agent
research_agent = Agent(
    name="Researcher",
    instructions="""You are a research specialist. When given a topic, provide:
    1. Key points about the topic
    2. Important facts and statistics
    3. Reliable references/sources
    Be comprehensive and factual, focusing on the most relevant and current information.
    Return your response as a structured ResearchOutput object.""",
    model=gemini_model
)

# Outline Agent
outline_agent = Agent(
    name="Outliner",
    instructions="""You are an expert content strategist. When given research material, create a detailed blog outline with:
    1. An engaging blog title
    2. At least 5 well-defined sections that logically flow from introduction to conclusion
    3. Section names that are descriptive and SEO-friendly
    Ensure the outline is comprehensive and would result in a substantial blog post.
    Return your response as a structured OutlineOutput object.""",
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
    Aim for a total length of at least 1000 words.
    Return your response as a structured WriterOutput object.""",
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
    Balance SEO optimization with maintaining the quality and readability of the content.
    Return your response as a structured SEOOutput object.""",
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
    Make the content engaging and professional while preserving the original meaning.
    Return your response as a structured EditorOutput object.""",
    model=gemini_model
)

# NOTE: The as_tool() function may not be available in all versions of the agents library
# The following demonstrates how it would be used when available:

try:
    # Convert agents to tools using as_tool (when available)
    from agents import as_tool

    research_tool = as_tool(
        research_agent,
        name="research_agent",
        description="Researches the blog topic and returns facts"
    )

    outline_tool = as_tool(
        outline_agent,
        name="outline_agent",
        description="Creates a detailed blog outline"
    )

    writer_tool = as_tool(
        writer_agent,
        name="writer_agent",
        description="Writes comprehensive blog content based on outline"
    )

    seo_tool = as_tool(
        seo_agent,
        name="seo_agent",
        description="Optimizes blog content for SEO"
    )

    editor_tool = as_tool(
        editor_agent,
        name="editor_agent",
        description="Edits and polishes the final blog content"
    )

    # Manager/Orchestrator Agent
    manager_agent = Agent(
        name="Blog Manager",
        instructions=f"""You are an orchestrator that manages the blog generation pipeline.
        Your job is to coordinate the following specialist agents:
        1. Use research_agent to gather information about the topic
        2. Use outline_agent to create a blog outline
        3. Use writer_agent to generate the content
        4. Use seo_agent to optimize for search engines
        5. Use editor_agent to polish the final content

        Decision Logic:
        - Ensure outline has at least 5 sections
        - Ensure blog length exceeds 800 words
        - If content is too short, request the writer to expand it
        - Always run the editor as the final step

        Return the final blog in the specified structured format.""",
        model=gemini_model,
        tools=[research_tool, outline_tool, writer_tool, seo_tool, editor_tool]
    )

    def run_orchestrated_blog_generation(topic: str) -> FinalBlogOutput:
        """
        Run the blog generation using the orchestrated approach
        """
        result = Runner.run_sync(
            manager_agent,
            f"Generate a comprehensive blog post about '{topic}'. Follow the complete pipeline: research, outline, write, optimize for SEO, and edit."
        )

        # Process the final result into the expected format
        # This would parse the structured output from the manager agent
        final_output = FinalBlogOutput(
            title="Generated Blog Title",  # Would come from the actual result
            blog=result.final_output,  # Would be the final blog content
            seo={
                'meta_description': 'Generated meta description',
                'keywords': ['AI', 'agents', 'technology', 'future']
            }
        )

        return final_output

except ImportError:
    print("as_tool() function not available in this version of the agents library.")
    print("The orchestrator pattern would work as described in the comments above.")

    # Alternative implementation without as_tool
    def run_orchestrated_blog_generation(topic: str) -> FinalBlogOutput:
        """
        Alternative implementation when as_tool is not available
        """
        # In this case, we would implement the orchestration manually
        # by calling each agent in sequence, similar to our main implementation
        pass

if __name__ == "__main__":
    print("Orchestrator Pattern Demonstration")
    print("This shows how agents can be converted to tools for orchestration.")
    print("When as_tool() is available, agents become callable tools that can be managed by a central orchestrator.")