import base64
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from thumbnail_agent.config import get_critic_llm
from thumbnail_agent.schemas import ThumbnailReview
from thumbnail_agent.state import ThumbnailState


def critic(state: ThumbnailState) -> dict:
    print("\n Evaluating thumbnail...")
    llm = get_critic_llm()
    structured_llm = llm.with_structured_output(
        ThumbnailReview
    )
    image_path = Path(state["image_path"])
    with open(image_path, "rb") as file:
        image_bytes = file.read()
    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")
    system_prompt = """
    You are a strict professional YouTube thumbnail critic.
    Evaluate the provided thumbnail using these criteria:
    1. Visual appeal
    2. Text readability
    3. Contrast
    4. Composition
    5. Topic relevance
    6. Click-through potential
    7. Mobile readability
    8. Professional quality
    Return:
    rating:
        Integer between 1 and 10.
    critique:
        Specific actionable feedback.
    Be strict.
    Do not give a high rating unless the thumbnail
    genuinely deserves it.
    Your critique must explain how the next
    iteration can improve.
    """

    user_message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": (
                    f"Evaluate this YouTube thumbnail "
                    f"for the topic: {state['topic']}"
                )
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": (
                        "data:image/png;base64,"
                        f"{encoded_image}"
                    )
                }
            }
        ]
    )
    review = structured_llm.invoke([
        SystemMessage(content=system_prompt),
        user_message
    ])
    print(f"Rating: {review.rating}/10")
    print(f"Critique: {review.critique}")
    history_entry = {
        "iteration": state["iteration"],
        "prompt": state["current_prompt"],
        "image_path": state["image_path"],
        "rating": review.rating,
        "critique": review.critique
    }
    return {
        "rating": review.rating,
        "critique": review.critique,
        # Append reducer handles accumulation
        "history": [history_entry]
    }