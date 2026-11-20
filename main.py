import argparse
import os
import re

from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from thumbnail_agent.graph import build_graph


load_dotenv()


def create_output_directory(topic: str) -> str:

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    safe_topic = re.sub(
        r"[^a-zA-Z0-9]+",
        "_",
        topic.lower()
    ).strip("_")[:60]

    if not safe_topic:
        safe_topic = "thumbnail"

    output_dir = (
        Path("outputs")
        / f"{timestamp}_{safe_topic}"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return str(output_dir)


def main():

    parser = argparse.ArgumentParser(
        description="YouTube Thumbnail Reflexion Agent"
    )

    parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="YouTube video topic"
    )

    parser.add_argument(
        "--target",
        type=int,
        default=int(
            os.getenv("TARGET_RATING", "8")
        )
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=int(
            os.getenv("MAX_ITERATIONS", "3")
        )
    )

    args = parser.parse_args()

    if not 1 <= args.target <= 10:
        parser.error("--target must be between 1 and 10")

    if args.max_iterations < 1:
        parser.error("--max-iterations must be at least 1")

    output_dir = create_output_directory(
        args.topic
    )

    initial_state = {
        "topic": args.topic,

        "search_summary": "",

        "current_prompt": "",

        "image_path": "",

        "rating": 0,

        "critique": "",

        "iteration": 0,

        "target_rating": args.target,

        "max_iterations": args.max_iterations,

        "history": [],

        "output_dir": output_dir
    }

    print("\n====================================")
    print("YouTube Thumbnail Reflexion Agent")
    print("====================================")

    print(f"Topic: {args.topic}")
    print(f"Target rating: {args.target}")
    print(f"Max iterations: {args.max_iterations}")

    graph = build_graph()

    final_state = graph.invoke(
        initial_state,
        config={
            "recursion_limit": max(
                25,
                args.max_iterations * 4 + 10
            )
        }
    )

    print("\n====================================")
    print("Execution Completed")
    print("====================================")

    print(
        f"Total iterations: "
        f"{final_state['iteration']}"
    )

    print(
        f"Last rating: "
        f"{final_state['rating']}/10"
    )

    print(
        f"Output directory: "
        f"{final_state['output_dir']}"
    )


if __name__ == "__main__":
    main()