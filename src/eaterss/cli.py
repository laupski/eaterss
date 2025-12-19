"""EateRSS CLI entry point."""

import argparse
import sys

from eaterss.app import main as run_app


def main() -> int:
    """Main CLI entry point for EateRSS."""
    parser = argparse.ArgumentParser(
        prog="eaterss",
        description="A TUI RSS feed reader. Browse and read RSS feeds in your terminal.",
        epilog="Examples:\n"
        "  eaterss                                    # Start with empty feed\n"
        "  eaterss https://news.ycombinator.com/rss  # Load Hacker News feed\n"
        "  eaterss https://feeds.bbci.co.uk/news/rss.xml  # Load BBC News feed",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "feed_url",
        nargs="?",
        default=None,
        help="URL of the RSS feed to load on startup (optional)",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    try:
        run_app(feed_url=args.feed_url)
        return 0
    except KeyboardInterrupt:
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
