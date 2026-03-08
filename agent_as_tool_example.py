from agents import Agent, Runner, function_tool, RunContextWrapper
from pydantic import BaseModel
from datetime import datetime

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

# NOTE: The actual as_tool functionality may not be available in this version of the agents library
# The following is conceptual code demonstrating the pattern

# Specialist agent for research
research_agent = Agent[TaskManagerContext](
    name="Researcher",
    instructions="""You are a research specialist.
    When given a topic, provide 3-5 key facts with sources.
    Be concise and factual."""
)

# Specialist agent for writing
writer_agent = Agent[TaskManagerContext](
    name="Writer",
    instructions="""You are a content writer.
    When given facts, transform them into engaging prose.
    Use clear, accessible language."""
)

# In a library that supports as_tool(), you would do something like:
# research_tool = as_tool(research_agent, name="do_research", description="Research a topic and provide key facts")
# write_tool = as_tool(writer_agent, name="write_content", description="Transform facts into engaging prose")

# Since as_tool() is not available in this version, we can simulate the behavior by defining function tools
# that internally call the agents. This is more complex and requires implementing the agent calls manually.

# For now, let's just demonstrate the concept with the available tools
manager = Agent[TaskManagerContext](
    name="Task Manager",
    instructions="""You are a task management assistant. Help users:
    - Add new tasks with priorities (1=low, 5=critical)
    - List their current tasks
    - Mark tasks as complete

    Always confirm actions and provide helpful summaries.""",
    tools=[add_task, list_tasks, complete_task]
)

# Example usage
if __name__ == "__main__":
    context = TaskManagerContext(
        user_id="developer_42",
        current_project="Content Creation Project"
    )

    # Run the manager agent
    result = Runner.run_sync(
        manager,
        "Add a task to research artificial intelligence trends with priority 4, then list all tasks.",
        context=context
    )

    print("Result from manager agent:")
    print(result.final_output)