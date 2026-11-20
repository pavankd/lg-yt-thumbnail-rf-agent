from pathlib import Path

from thumbnail_agent.graph import build_graph

def main():
    graph = build_graph()
    image_data = (
        graph.get_graph().draw_mermaid_png()
    )
    output_path = Path("graph.png")
    output_path.write_bytes(image_data)
    print(
        f"Graph diagram saved to: "
        f"{output_path.resolve()}"
    )

if __name__ == "__main__":
    main()