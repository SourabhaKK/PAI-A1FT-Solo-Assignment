"""
Run Script for Task 2: Basket Analysis
Entry point for the Supermarket Basket Analysis System
Author: Sourabha K Kallapur
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from basket_analysis.cli import BasketAnalysisCLI


def main():
    """Main entry point for Task 2"""
    try:
        # Create and run the CLI
        cli = BasketAnalysisCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check the error message above for details.")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
