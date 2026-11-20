import operator

from typing import Annotated, TypedDict


class ThumbnailState(TypedDict):

    # Input
    topic: str

    # Web search
    search_summary: str

    # Prompt generation
    current_prompt: str

    # Image generation
    image_path: str

    # Evaluation
    rating: int
    critique: str

    # Iteration management
    iteration: int

    # Configuration
    target_rating: int
    max_iterations: int

    # History with append reducer
    history: Annotated[list[dict], operator.add]

    # Output directory
    output_dir: str