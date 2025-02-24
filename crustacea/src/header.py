from textual.reactive import Reactive
from time import monotonic
from rich.text import Text

from textual.widget import Widget
from textual.app import RenderResult
from textual.widgets._header import Header, HeaderIcon, HeaderTitle


class HeaderClock(Widget):
    """Display a clock on the right of the header."""

    DEFAULT_CSS = """
    HeaderClock {
        background: $foreground-darken-1 5%;
        color: $foreground;
        text-opacity: 85%;
        content-align: center middle;
        dock: right;
        width: 27;
        padding: 0 1;
    }
    """
    
    time_elapsed = Reactive(0.0001)
    start_time = monotonic()
    
    def update_time_elapsed(self): 
        self.time_elapsed = monotonic() - self.start_time
    
    def _on_mount(self):
        # self.set_interval(1/10, callback=self.refresh, name="update header clock")
        self.update_timer = self.set_interval(  # calls the method given in an interval
            1 / 10,
            self.update_time_elapsed, 
            pause=False   
        )
        
    def render(self) -> RenderResult:
        """Render the header clock.

        Returns:
            The rendered clock.
        """
        self.time_elapsed = monotonic() - self.start_time
        time, seconds = divmod(self.time_elapsed, 60)
        hours, minutes = divmod(time, 60)
        return f"Elapsed Time: {hours:02.0f}:{minutes:02.0f}:{seconds:02.1f}"


class CrustaceaHeader(Header):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.clock = HeaderClock()      
    
    def compose(self):
        yield HeaderIcon().data_bind(Header.icon)
        yield HeaderTitle()
        yield self.clock