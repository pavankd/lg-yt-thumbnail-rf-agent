LangGraph youtube thumbnail reflection agent 

# 1. Install dependencies
uv sync

# 2. Generate graph visualization
uv run python make_diagram.py

# 3. Execute the agent
uv run python main.py --topic "Why Python is the best language for AI" --target 8 --max-iterations 3

# 4. Verify output files
dir outputs

