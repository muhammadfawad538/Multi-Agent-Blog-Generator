"""
Test script to demonstrate the agent functionality
"""
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
from agents import Agent, Runner, function_tool, RunContextWrapper, set_tracing_disabled
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from pydantic import BaseModel
from datetime import datetime

set_tracing_disabled(True)

# Context Model
class TaskManagerContext(BaseModel):
    user_id: str | None = None
    current_project: str | None = None
    tasks_added: int = 0
    tasks: list[dict] = []

# Tools
@function_tool
def add_task(
    ctx: RunContextWrapper[TaskManagerContext],
    title: str,
    priority: int = 1
) -> str:
    """
    Add a new task to the task list.

    Args:
        title: The task description
        priority: Priority level 1-5 where 5 is highest

    Returns:
        Confirmation message with task ID
    """
    task_id = f"task_{len(ctx.context.tasks) + 1:03d}"
    task = {
        "id": task_id,
        "title": title,
        "priority": priority,
        "status": "pending",
        "created": datetime.now().isoformat(),
        "project": ctx.context.current_project
    }
    ctx.context.tasks.append(task)
    ctx.context.tasks_added += 1

    return f"Created {task_id}: '{title}' (priority {priority})"

@function_tool
def list_tasks(ctx: RunContextWrapper[TaskManagerContext]) -> str:
    """List all tasks for the current project."""
    project = ctx.context.current_project
    tasks = [t for t in ctx.context.tasks if t["project"] == project]

    if not tasks:
        return f"No tasks found for project '{project}'"

    lines = [f"Tasks for '{project}':"]
    for t in tasks:
        status = "[ ]" if t["status"] == "pending" else "[x]"
        lines.append(f"  {status} {t['id']}: {t['title']} (P{t['priority']})")

    return "\n".join(lines)

@function_tool
def complete_task(
    ctx: RunContextWrapper[TaskManagerContext],
    task_id: str
) -> str:
    """
    Mark a task as complete.

    Args:
        task_id: The ID of the task to complete (e.g., 'task_001')

    Returns:
        Confirmation message
    """
    for task in ctx.context.tasks:
        if task["id"] == task_id:
            task["status"] = "complete"
            return f"Completed task {task_id}: '{task['title']}'"

    return f"Task {task_id} not found"

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

# Agent with task management capabilities
task_manager = Agent[TaskManagerContext](
    name="task_manager",
    instructions="""You are a task management assistant. Help users:
    - Add new tasks with priorities (1=low, 5=critical)
    - List their current tasks
    - Mark tasks as complete

    Always confirm actions and provide helpful summaries.""",
    model=gemini_model,
    tools=[add_task, list_tasks, complete_task]
)

# Example usage - run a series of commands
if __name__ == "__main__":
    context = TaskManagerContext(
        user_id="developer_42",
        current_project="Digital FTE MVP"
    )

    print("Testing the task manager agent...\n")

    # Test 1: Add a task
    print("Test 1: Adding a task")
    result = Runner.run_sync(
        task_manager,
        "Add a task to design the user interface with priority 4",
        context=context
    )
    print(f"Response: {result.final_output}\n")

    # Test 2: Add another task
    print("Test 2: Adding another task")
    result = Runner.run_sync(
        task_manager,
        "Add a task to implement the authentication system with priority 5",
        context=context
    )
    print(f"Response: {result.final_output}\n")

    # Test 3: List all tasks
    print("Test 3: Listing all tasks")
    result = Runner.run_sync(
        task_manager,
        "Show me all my tasks",
        context=context
    )
    print(f"Response: {result.final_output}\n")

    # Test 4: Complete a task
    print("Test 4: Completing a task")
    result = Runner.run_sync(
        task_manager,
        "Complete task task_001",
        context=context
    )
    print(f"Response: {result.final_output}\n")

    # Test 5: List tasks again to see the completed task
    print("Test 5: Listing tasks after completion")
    result = Runner.run_sync(
        task_manager,
        "Show me all my tasks",
        context=context
    )
    print(f"Response: {result.final_output}\n")

    print("All tests completed!")