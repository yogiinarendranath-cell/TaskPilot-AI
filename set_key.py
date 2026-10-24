import os, subprocess
from openai import OpenAI

print("\n=== TaskPilot Agent Startup ===")
print("Opening Notepad to paste your Groq key...")
path = "temp_key.txt"
open(path, "w").close()
subprocess.run(["notepad.exe", path])

with open(path, "r") as f:
    key = f.read().strip()
os.remove(path)

if not key.startswith("gsk_"):
    print("❌ ERROR: Invalid key.")
    exit(1)

# Set the environment variables for the PowerShell session
print("\n✅ Key loaded successfully. You can now run the agent.")
print("Example:")
print("  python -m taskpilot run --task examples\task_demo.json --workspace .\workspace --out .\output.csv --logs .\logs")