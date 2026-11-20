from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient
from thumbnail_agent.state import ThumbnailState


def web_search(state: ThumbnailState) -> dict:
    topic = state["topic"]
    print(f"\n Searching web for: {topic}")
    response = TavilyClient().search(
        query=(
            f"{topic} YouTube thumbnail ideas "
            "visual hooks interesting facts"
        ),
        search_depth="basic",
        max_results=5
    )
    results = response.get("results", [])
    summary_parts = []
    for result in results:
        title = result.get("title", "")
        content = result.get("content", "")
        summary_parts.append(
            f"Title: {title}\n"
            f"Summary: {content}"
        )
    search_summary = "\n\n".join(summary_parts)
    print("Web search completed")
    return {
        "search_summary": search_summary
    }