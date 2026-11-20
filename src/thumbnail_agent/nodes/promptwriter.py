from langchain_core.messages import HumanMessage, SystemMessage
from thumbnail_agent.config import get_prompt_llm
from thumbnail_agent.state import ThumbnailState


def prompt_writer(state: ThumbnailState) -> dict:
    print("\n Writing thumbnail prompt...")
    llm = get_prompt_llm()
    topic = state["topic"]
    search_summary = state["search_summary"]
    iteration = state["iteration"]
    critique = state["critique"]
    system_prompt = """
    You are an expert YouTube thumbnail designer.
    Your responsibility is to create highly engaging
    image-generation prompts.
    Thumbnail design requirements:

    1. Aspect ratio 16:9.
    2. Resolution 1792x1024.
    3. Strong visual hierarchy.
    4. High contrast.
    5. Large readable text.
    6. Eye-catching colors.
    7. Professional composition.
    8. Clear focal point.
    9. Minimal clutter.
    10. Suitable for YouTube.

    Return only the image-generation prompt.
    """
    user_prompt = f"""
    Video topic:
    {topic}
    Research:
    {search_summary}
    """
    if iteration > 0:
        user_prompt += f"""
        IMPORTANT:
        The previous thumbnail received a rating of
        {state["rating"]}/10.
        Previous critique:
        {critique}
        Create an improved prompt.
        Address every issue identified in the critique.
        Do not repeat the previous design mistakes.
        """
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)
    new_prompt = response.content
    print("Prompt generated")
    return {
        "current_prompt": new_prompt
    }