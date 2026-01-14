#!/usr/bin/env python
# src/financial_researcher/main.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Find .env - try project root first, then top-level agents folder
project_env = Path(__file__).resolve().parents[2] / ".env"
top_level_env = Path(__file__).resolve().parents[4] / ".env"

# Debug: print paths to verify
print(f"Looking for .env at: {project_env} (exists: {project_env.exists()})")
print(f"Fallback .env at: {top_level_env} (exists: {top_level_env.exists()})")

env_to_use = project_env if project_env.exists() else top_level_env
print(f"Using: {env_to_use}")
loaded = load_dotenv(env_to_use, override=True)
print(f"Loaded: {loaded}, OPENAI_API_KEY set: {bool(os.environ.get('OPENAI_API_KEY'))}")

from financial_researcher.crew import FinancialResearcher
# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    """
    Run the financial researcher crew.
    """
    inputs = {
        'company': 'OpenAI'
    }

    # Create and run the crew
    result = FinancialResearcher().crew().kickoff(inputs=inputs)

    # Print the result
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print("\n\nReport has been saved to output/report.md")

if __name__ == "__main__":
    run()