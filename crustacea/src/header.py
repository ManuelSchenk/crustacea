from textual.reactive import Reactive
from time import monotonic

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
        width: 25;
        padding: 0 1;
    }
    """

    elapsed = Reactive(0.00001)

    def update_time_elapsed(self): 
        """polls the current timer from the main app"""
        self.elapsed = self.screen.time_elapsed
    
    def on_mount(self):
        self.update_timer = self.set_interval(  
            interval=1,
            callback=self.update_time_elapsed, 
            pause=False   
        )
        
    def render(self) -> RenderResult:
        """Render the header clock as elapsed timer"""
        time, seconds = divmod(self.elapsed, 60)
        hours, minutes = divmod(time, 60)
        return f"Elapsed Time: {hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"


class CrustaceaHeader(Header):
    """Modified header using an elapsed timer instead of a clock"""
    
    def compose(self):
        yield HeaderIcon().data_bind(Header.icon)
        yield HeaderTitle()
        yield HeaderClock()