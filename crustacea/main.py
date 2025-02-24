import textual.app as app
import textual.widgets as widg 
import crustacea.src.editor as edit
from crustacea.src.statistics import CrustaceaStatistics
from crustacea.src.header import CrustaceaHeader
from textual.reactive import Reactive
from time import monotonic 

from crustacea.utils.logging import ic 

input_text = ""
with open("./tutorials/stopwatch.py", "r") as text:
    lines = text.readlines()             
    cleaned_lines = [line.rstrip() for line in lines]  
    input_text = "\n".join(cleaned_lines)  
  

class CrustaceaApp(app.App):
    
    BINDINGS = [
        ("ctrl+t", "toggle_auto_tab", "Toggle Automatic Tab"),
        ("ctrl+b", "pause_timer", "Pause Timer"),
        ("ctrl+n", "toggle_cursor_navigation", "Enable Cursor Navigation"),
    ]

    start_time = monotonic()
    time_elapsed = Reactive(0.00001)
    pause = False
    time_paused = Reactive(0.00001)
    enable_arrow_keys = False
    
    def compose(self) -> app.ComposeResult:  
        try:
            self.header = CrustaceaHeader()
            yield self.header
            yield widg.Footer()
            self.statistics = CrustaceaStatistics()
            
            self.editor = edit.CrustaceaTextArea.code_editor(input_text, language="python", theme="vscode_dark")
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
            

if __name__ == "__main__":
    ic("CrustaceaApp started...")
    CrustaceaApp().run(mouse=False)
        
