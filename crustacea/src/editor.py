from textual.screen import Screen
from textual.widgets import Footer
import textual.app as app
from textual.reactive import Reactive


from crustacea.utils.logging import ic 
from crustacea.src.statistics import CrustaceaStatistics
from crustacea.src.header import CrustaceaHeader
import crustacea.src.text_area as edit
from time import monotonic 



class EditorScreen(Screen):
    
    BINDINGS = [
        ("ctrl+s", "pause_timer", "Pause Timer"),
        ("ctrl+b", "forced_backspace_error", "Disable Backspace Error correction"),
        ("ctrl+t", "toggle_auto_tab", "Toggle Automatic Tab"),
        ("ctrl+n", "toggle_cursor_navigation", "Enable Cursor Navigation"),
    ]

    time_elapsed = Reactive(0.00001)
    time_paused = Reactive(0.00001)

    
    def __init__(self, input_text: str, language: str, **kwargs):
        super().__init__(**kwargs)
        self.input_text = input_text
        self.pause = False
        self.language = language
        self.enable_arrow_keys = False
        self.forced_backspace_error = True
        self.start_time = monotonic()


    def compose(self) -> app.ComposeResult:  
        try:
            yield CrustaceaHeader()
            yield Footer()
            self.statistics = CrustaceaStatistics()
            
            self.editor = edit.CrustaceaTextArea.code_editor(
                text=self.input_text, 
                language=self.language, 
                theme="vscode_dark"
                )
            self.editor.read_only = True
  
            yield self.editor
            yield self.statistics
            
        except Exception as e:
            ic(e)
            
    def update_time_elapsed(self): 
        if self.pause:
            self.start_time = monotonic() - self.time_elapsed
        else: 
            self.time_elapsed = monotonic() - self.start_time
            self.editor.focus()
    
    def on_mount(self): 
        self.update_timer = self.set_interval(  # calls the method given in an interval
            interval=1/2,
            callback=self.update_time_elapsed, 
            pause=False  
        )

    def action_toggle_auto_tab(self):
        '''toggles the usage of tabs at line start after return at line end'''
        self.editor.auto_tab = not self.editor.auto_tab
                    
    def action_pause_timer(self):
        '''paused the elapse timer'''
        self.pause = not self.pause
        self.editor.disabled = not self.editor.disabled
        
    def action_toggle_cursor_navigation(self):
        '''enable the navigation with arrow keys in the code editor'''
        self.enable_arrow_keys = not self.enable_arrow_keys        
        
    def action_forced_backspace_error(self):
        '''enable the navigation with arrow keys in the code editor'''
        self.forced_backspace_error = not self.forced_backspace_error 
