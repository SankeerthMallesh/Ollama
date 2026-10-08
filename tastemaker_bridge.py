import ollama
import subprocess
import os
import re
import sys

# --- CONFIGURATION ---
MODEL = "llama3"  # Change this to your preferred Ollama model (e.g., "mistral", "phi3")
SKILL_DIR = "./tastemaker-skill"
PROMPT_FILE = "tastemaker_ollama_prompt.md"
# ---------------------

def load_prompt():
    try:
        with open(PROMPT_FILE, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {PROMPT_FILE} not found. Please ensure it's in the current directory.")
        sys.exit(1)

def run_tastemaker_script(script_call):
    """
    Executes a Tastemaker script and returns the output.
    Expected format: "scripts/generate_palette.py --mood warm"
    """
    # Split the script path and the arguments
    parts = script_call.split(' ', 1)
    script_rel_path = parts[0]
    args = parts[1] if len(parts) > 1 else ""

    # Construct the absolute path to the script
    # The scripts are inside the tastemaker-skill folder
    full_path = os.path.join(SKILL_DIR, script_rel_path)

    print(f"\n[Executing Tool]: {full_path} {args}")

    try:
        # Run the script using python3
        # We use a shell because some scripts might need shell expansion or environment variables
        result = subprocess.run(
            ["python3", full_path, *args.split()],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return f"--- SCRIPT OUTPUT ---\\n{result.stdout}"
        else:
            return f"--- SCRIPT ERROR ---\\n{result.stderr}"

    except Exception as e:
        return f"--- EXECUTION FAILURE ---\\n{str(e)}"

def main():
    system_prompt = load_prompt()
    messages = [{"role": "system", "content": system_prompt}]

    print("--- Tastemaker Ollama Bridge ---")
    print(f"Model: {MODEL}")
    print("Type 'exit' to quit.")
    print("-------------------------------\n")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        messages.append({"role": "user", "content": user_input})

        while True:
            response = ollama.chat(model=MODEL, messages=messages)
            assistant_msg = response['message']['content']

            # Check if the model is calling a tool
            match = re.search(r"S-CALL: ([\w\./-]+ .*)$", assistant_msg, re.MULTILINE)

            if match:
                script_call = match.group(1).strip()
                # We provide the tool call to the user so they know what's happening
                print(f"\nAI: {assistant_msg}")

                # Run the tool
                tool_result = run_tastemaker_script(script_call)

                # Feed the result back to the AI
                messages.append({"role": "assistant", "content": assistant_msg})
                messages.append({"role": "user", "content": f"TOOL RESULT: {tool_result}"})

                # Continue the loop to get the AI's interpretation of the result
                continue
            else:
                # No tool call, just a normal response
                print(f"\nAI: {assistant_msg}")
                messages.append({"role": "assistant", "content": assistant_msg})
                break

if __name__ == "__main__":
    main()
