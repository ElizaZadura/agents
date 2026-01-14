#!/usr/bin/env python
import sys
import warnings
from pathlib import Path

from dotenv import load_dotenv
from datetime import datetime

from stock_picker.crew import StockPicker

# Load .env from project root (5 levels up from this file)
project_root = Path(__file__).parent.parent.parent.parent.parent
load_dotenv(dotenv_path=project_root / '.env', override=True)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
       'sector': 'Defense & Aerospace (non-consumer, non-cyber)'
    }

    try:
        # Create and run the crew
        result = StockPicker().crew().kickoff(inputs=inputs)
        # Print the result
        print("\n\n=== FINAL DECISION ===\n\n")
        print(result.raw)
    # Handle any errors
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

if __name__ == "__main__":
    run()