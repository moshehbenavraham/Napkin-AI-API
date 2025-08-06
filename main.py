#!/usr/bin/env python
"""
Napkin AI API Playground - Main entry point.

Python client for the Napkin AI Visual Generation API.
"""

import sys
from src.cli.commands import main


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}", file=sys.stderr)
        sys.exit(1)
