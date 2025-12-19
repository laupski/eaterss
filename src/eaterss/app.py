"""EateRSS TUI Application."""

import feedparser
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Input, Label, ListItem, ListView, Markdown, Static


class FeedItem(ListItem):
    """A single feed item in the list."""

    def __init__(self, title: str, link: str, summary: str, published: str = "") -> None:
        super().__init__()
        self.item_title = title
        self.item_link = link
        self.item_summary = summary
        self.item_published = published

    def compose(self) -> ComposeResult:
        """Compose the feed item display."""
        yield Label(self.item_title, classes="item-title")
        if self.item_published:
            yield Label(self.item_published, classes="item-date")


class EateRSSApp(App):
    """A TUI RSS feed reader application."""

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        height: 100%;
    }

    #input-container {
        height: auto;
        padding: 1;
        background: $boost;
    }

    #feed-input {
        width: 100%;
    }

    #content-area {
        height: 1fr;
    }

    #feed-list {
        width: 40%;
        min-width: 30;
        border-right: solid $primary;
    }

    #item-detail {
        width: 60%;
        padding: 1 2;
    }

    .item-title {
        text-style: bold;
    }

    .item-date {
        color: $text-muted;
        text-style: italic;
    }

    #detail-title {
        text-style: bold;
        color: $primary;
        margin-bottom: 1;
    }

    #detail-link {
        color: $secondary;
        margin-bottom: 1;
    }

    #detail-date {
        color: $text-muted;
        text-style: italic;
        margin-bottom: 1;
    }

    #detail-content {
        height: 1fr;
    }

    #status-bar {
        height: auto;
        padding: 0 1;
        background: $boost;
        color: $text-muted;
    }

    #loading-label {
        text-align: center;
        padding: 2;
        color: $warning;
    }

    #error-label {
        text-align: center;
        padding: 2;
        color: $error;
    }

    ListView > ListItem {
        padding: 1;
    }

    ListView > ListItem.--highlight {
        background: $primary 20%;
    }

    ListView:focus > ListItem.--highlight {
        background: $primary 40%;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("escape", "focus_input", "Focus Input"),
    ]

    def __init__(self, feed_url: str | None = None) -> None:
        super().__init__()
        self.initial_feed_url = feed_url
        self.current_feed = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Vertical(id="main-container"):
            with Container(id="input-container"):
                yield Input(
                    placeholder="Enter RSS feed URL and press Enter...",
                    id="feed-input",
                    value=self.initial_feed_url or "",
                )
            with Horizontal(id="content-area"):
                yield ListView(id="feed-list")
                with VerticalScroll(id="item-detail"):
                    yield Label("", id="detail-title")
                    yield Label("", id="detail-link")
                    yield Label("", id="detail-date")
                    yield Markdown("", id="detail-content")
            yield Static("Enter an RSS feed URL to get started", id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Handle app mount event."""
        self.title = "EateRSS"
        self.sub_title = "RSS Feed Reader"
        if self.initial_feed_url:
            self.load_feed(self.initial_feed_url)
        else:
            self.query_one("#feed-input", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle feed URL submission."""
        url = event.value.strip()
        if url:
            self.load_feed(url)

    def load_feed(self, url: str) -> None:
        """Load and parse an RSS feed."""
        status_bar = self.query_one("#status-bar", Static)
        status_bar.update(f"Loading feed: {url}...")

        try:
            feed = feedparser.parse(url)

            if feed.bozo and not feed.entries:
                status_bar.update(f"Error: Failed to parse feed - {feed.bozo_exception}")
                return

            self.current_feed = feed
            self.populate_feed_list(feed)

            feed_title = feed.feed.get("title", "Unknown Feed")
            status_bar.update(f"Loaded: {feed_title} ({len(feed.entries)} items)")

            # Focus the feed list after loading
            feed_list = self.query_one("#feed-list", ListView)
            feed_list.focus()

        except Exception as e:
            status_bar.update(f"Error: {e}")

    def populate_feed_list(self, feed) -> None:
        """Populate the feed list with entries."""
        feed_list = self.query_one("#feed-list", ListView)
        feed_list.clear()

        for entry in feed.entries:
            title = entry.get("title", "No title")
            link = entry.get("link", "")
            summary = entry.get("summary", entry.get("description", ""))
            published = entry.get("published", entry.get("updated", ""))

            item = FeedItem(title=title, link=link, summary=summary, published=published)
            feed_list.append(item)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle feed item selection."""
        item = event.item
        if isinstance(item, FeedItem):
            self.show_item_detail(item)

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        """Handle feed item highlight (cursor movement)."""
        item = event.item
        if isinstance(item, FeedItem):
            self.show_item_detail(item)

    def show_item_detail(self, item: FeedItem) -> None:
        """Display the detail view for a feed item."""
        title_label = self.query_one("#detail-title", Label)
        link_label = self.query_one("#detail-link", Label)
        date_label = self.query_one("#detail-date", Label)
        content_md = self.query_one("#detail-content", Markdown)

        title_label.update(item.item_title)
        link_label.update(f"🔗 {item.item_link}")
        date_label.update(f"📅 {item.item_published}" if item.item_published else "")

        # Clean up HTML in summary for markdown display
        summary = item.item_summary
        content_md.update(summary)

    def action_refresh(self) -> None:
        """Refresh the current feed."""
        feed_input = self.query_one("#feed-input", Input)
        url = feed_input.value.strip()
        if url:
            self.load_feed(url)

    def action_focus_input(self) -> None:
        """Focus the URL input field."""
        self.query_one("#feed-input", Input).focus()


def main(feed_url: str | None = None) -> None:
    """Run the EateRSS application."""
    app = EateRSSApp(feed_url=feed_url)
    app.run()


if __name__ == "__main__":
    main()
