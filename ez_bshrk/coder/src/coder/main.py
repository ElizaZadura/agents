#!/usr/bin/env python
import sys
import warnings
import os
from pathlib import Path

from datetime import datetime
from dotenv import load_dotenv

# CRITICAL: Load .env BEFORE importing CrewAI to ensure env vars are set
# Try multiple possible .env locations
possible_env_paths = [
    Path(__file__).parent.parent.parent.parent.parent / '.env',  # agents root
    Path(__file__).parent.parent.parent.parent.parent.parent / '.env',  # agents_mine root
    Path(__file__).parent.parent.parent.parent.parent.parent.parent / '.env',  # ai_engineer_agentic_track root
]

env_loaded = False
for env_path in possible_env_paths:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=True)
        env_loaded = True
        print(f"✓ Loaded .env from: {env_path}")
        break

if not env_loaded:
    # Fallback: try loading from current directory and system env
    load_dotenv(override=True)
    print("⚠️  No .env file found in expected locations, using system environment")

# Explicitly ensure OPENAI_API_KEY is set in environment
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    # Remove any quotes or whitespace that might have been introduced
    api_key = api_key.strip().strip('"').strip("'")
    os.environ['OPENAI_API_KEY'] = api_key
    print(f"✓ OPENAI_API_KEY set (length: {len(api_key)}, starts with: {api_key[:7]}...)")
else:
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment")
    print(f"   Checked .env files at:")
    for env_path in possible_env_paths:
        print(f"     - {env_path} (exists: {env_path.exists()})")

# Now import CrewAI after environment is set
from coder.crew import Coder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

assignment = 'Write a python program to calculate the first 10,000 terms of this series, multiplying the total by 4: 1 - 1/3 + 1/5 - 1/7 + ...'
def run():
    """
    Run the crew.
    """
    inputs = {
        'assignment': assignment
    }
    result = Coder().crew().kickoff(inputs=inputs)
    print(result.raw)