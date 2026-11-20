import shutil
from pathlib import Path
from thumbnail_agent.state import ThumbnailState


def saver(state: ThumbnailState) -> dict:
    print("\nSaving final thumbnail and report...")
    history = state["history"]
    if not history:
        raise ValueError(
            "Cannot save thumbnail because history is empty."
        )
    output_dir = Path(state["output_dir"])
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )
    # Select highest-rated image
    best_iteration = max(
        history,
        key=lambda item: item["rating"]
    )
    best_image_path = Path(
        best_iteration["image_path"]
    )
    final_image_path = output_dir / "final.png"
    shutil.copy2(
        best_image_path,
        final_image_path
    )
    # Build markdown report
    report_lines = [
        "# YouTube Thumbnail Designer Report",
        "",
        f"## Topic",
        "",
        state["topic"],
        "",
        "## Execution Summary",
        "",
        f"- Total iterations: {state['iteration']}",
        f"- Target rating: {state['target_rating']}",
        f"- Maximum iterations: {state['max_iterations']}",
        f"- Best iteration: {best_iteration['iteration']}",
        f"- Best rating: {best_iteration['rating']}/10",
        "",
        "## Iteration History",
        ""
    ]

    for entry in history:
        report_lines.extend([
            f"### Iteration {entry['iteration']}",
            "",
            f"**Rating:** {entry['rating']}/10",
            "",
            f"**Image:** `{Path(entry['image_path']).name}`",
            "",
            "#### Prompt",
            "",
            "```text",
            str(entry["prompt"]),
            "```",
            "",
            "#### Critique",
            "",
            str(entry["critique"]),
            "",
            "---",
            ""
        ])

    report_lines.extend([
        "## Final Selection",
        "",
        f"Selected iteration: {best_iteration['iteration']}",
        "",
        f"Final rating: {best_iteration['rating']}/10",
        "",
        "Final image: `final.png`",
        ""
    ])

    report_path = output_dir / "report.md"
    report_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )
    print(f"Final image: {final_image_path}")
    print(f"Report: {report_path}")
    return {}