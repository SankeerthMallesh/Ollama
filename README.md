# Tastemaker Ollama Bridge

A bridge that connects Ollama LLMs to the Tastemaker design skill, allowing AI agents to generate professional, contrast-checked, and on-brand UIs.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Ensure Ollama is running.
3. Run the bridge: `python3 tastemaker_bridge.py`

## How it Works
The bridge uses a specialized system prompt to force the AI into a design-first workflow. When the AI needs to generate a palette, check contrast, or fetch assets, it issues an `S-CALL` command which the bridge executes locally using the Tastemaker Python scripts.

## Repository Structure
- `tastemaker-skill/`: The core design rules and scripts.
- `tastemaker_bridge.py`: The Python agent bridge.
- `tastemaker_ollama_prompt.md`: The system instructions for the model.

