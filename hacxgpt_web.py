#!/usr/bin/env python3
"""
HacxGPT Web Launcher
Launch the web-based UI for HacxGPT
"""

import sys
import argparse
from hacxgpt.web_ui import launch_web_ui


def main():
    parser = argparse.ArgumentParser(
        description="HacxGPT Web Interface - Neural Link Console",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hacxgpt_web.py                    # Launch on localhost:7860
  python hacxgpt_web.py --port 8080        # Launch on custom port
  python hacxgpt_web.py --share            # Create public share link
  python hacxgpt_web.py --host 0.0.0.0     # Allow external connections
        """
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=7860,
        help='Port to run the server on (default: 7860)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1, use 0.0.0.0 for external access)'
    )
    
    parser.add_argument(
        '--share',
        action='store_true',
        help='Create a public share link (Gradio share)'
    )
    
    args = parser.parse_args()
    
    try:
        launch_web_ui(
            share=args.share,
            server_port=args.port,
            server_name=args.host
        )
    except KeyboardInterrupt:
        print("\n\n🔴 Server shutdown requested")
        print("✓ Neural link terminated")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error launching server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
