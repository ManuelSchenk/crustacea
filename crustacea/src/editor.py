from textual.screen import Screen
from textual.widgets import Footer
import textual.app as app
from textual.reactive import Reactive
from textual.binding import Binding

from crustacea.utils.logging import ic 
from crustacea.src.statistics import CrustaceaStatistics
from crustacea.src.header import CrustaceaHeader
import crustacea.src.text_area as edit
from time import monotonic 


class EditorScreen(Screen):
    """The main editor screen for the Crustacea app"""
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", 
                tooltip="Quit the app and return to the command prompt.", 
                show=True, priority=True),
        ("ctrl+s", "pause_timer", "Pause"),
        ("ctrl+b", "auto_backspace", "Enable Automatic Backspace"),
        ("ctrl+r", "auto_return", "Enable Automatic Return"),
        ("ctrl+t", "auto_tab", "Disable Automatic Tab"),
        ("ctrl+n", "cursor_navigation", "Enable Cursor Navigation"),
    ]

    time_elapsed = Reactive(0.00001)
    time_paused = Reactive(0.00001)

    
    def __init__(self, filename: str, input_text: str, language: str, **kwargs):
        super().__init__(**kwargs)
        self.filename=filename
        self.input_text = input_text
        self.pause = False
        self.language = language
        self.start_time = monotonic()
        
        # initial states for the key bindings
        self.enable_arrow_keys = False
        self.auto_backspace = False
        self.auto_return = False
        self.auto_tab = True


    def compose(self) -> app.ComposeResult:  
        try:
            yield CrustaceaHeader()
            yield Footer()
            self.statistics = CrustaceaStatistics()
            
            self.text_area = edit.CrustaceaTextArea.code_editor(
                text=self.input_text, 
                language=self.language, 
                theme="vscode_dark"
                )
            self.text_area.read_only = True
  
            yield self.text_area
            yield self.statistics
            
        except Exception as e:
            ic(e)
            
    def update_time_elapsed(self): 
        if self.pause:
            self.start_time = monotonic() - self.time_elapsed
        else: 
            self.time_elapsed = monotonic() - self.start_time
            self.text_area.focus()
    
    def on_mount(self): 
        self.update_timer = self.set_interval(  # calls the method given in an interval
            interval=1/2,
            callback=self.update_time_elapsed, 
            pause=False  
        )

    def action_auto_tab(self):
        '''toggles the usage of TAB at line start after return at end of line'''
        self.auto_tab = not self.auto_tab
        ic(f"Toggle Automatic TAB into {self.auto_tab}")

    def action_auto_return(self):
        '''toggles the usage of automatic RETURN at end of line'''
        self.auto_return = not self.auto_return
        ic(f"Toggle Automatic RETURN into {self.auto_return}")
        
    def action_auto_backspace(self):
        '''enable the navigation with arrow keys in the code editor'''
        self.auto_backspace = not self.auto_backspace 
        ic(f"Toggle Automatic BACKSPACE into {self.auto_backspace}")
                    
    def action_pause_timer(self):
        '''paused the elapse timer'''
        self.pause = not self.pause
        self.text_area.disabled = not self.text_area.disabled
        ic(f"Pause Crustacea App {self.text_area.disabled}")
        
    def action_cursor_navigation(self):
        '''enable the navigation with arrow keys in the code editor'''
        self.enable_arrow_keys = not self.enable_arrow_keys        
        ic(f"Toggle CURSOR Navigation into {self.enable_arrow_keys}")
