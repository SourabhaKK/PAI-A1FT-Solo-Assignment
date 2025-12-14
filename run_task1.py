"""
Run Script for Task 1: Health Dashboard
Entry point for the Public Health Data Insights Dashboard
Author: Sourabha K Kallapur
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from health_dashboard.cli import HealthDashboardCLI


def main():
    """Main entry point for Task 1"""
    try:
        # Create and run the CLI
        cli = HealthDashboardCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check the logs for more details.")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
