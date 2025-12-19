# EateRSS

A TUI (Terminal User Interface) RSS feed reader built with Python, Textual, and feedparser.

## Features

- 📰 Load any RSS feed by URL
- 📜 Scroll through feed items in a list view
- 📖 View article details including title, link, date, and summary
- ⌨️ Keyboard navigation for efficient browsing
- 🎨 Clean, modern terminal UI

## Installation

### Using uv (recommended)

```bash
uv pip install -e .
```

## Usage

### Start with empty feed

```bash
eaterss
```

### Load a feed directly

```bash
eaterss https://news.ycombinator.com/rss
```

### Example feeds to try

```bash
# Hacker News
eaterss https://news.ycombinator.com/rss

# BBC News
eaterss https://feeds.bbci.co.uk/news/rss.xml

# Reddit (various subreddits)
eaterss https://www.reddit.com/r/python/.rss
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑` / `↓` | Navigate feed items |
| `Enter` | Select item |
| `r` | Refresh current feed |
| `Escape` | Focus URL input |
| `q` | Quit application |

## Development

### Prerequisites

- Python 3.14+
- uv package manager

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd eaterss

# Install dependencies
uv sync

# Run the application
uv run eaterss
```
