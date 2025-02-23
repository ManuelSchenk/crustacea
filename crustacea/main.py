import textual.app as app
import textual.widgets as widg 
import crustacea.src.editor as edit
from crustacea.src.statistics import CrustaceaStatistics
from crustacea.src.header import CrustaceaHeader
from textual.reactive import Reactive


from crustacea.utils.logging import ic 

input_text = ""
with open("./tutorials/stopwatch.py", "r") as text:
    lines = text.readlines()             
    cleaned_lines = [line.rstrip() for line in lines]  
    input_text = "\n".join(cleaned_lines)  
  

class CrustaceaApp(app.App):
    
    BINDINGS = [
        ("ctrl+t", "toggle_auto_tab", "Toggle Automatic Tab"),
    ]
    
    time_elapsed = Reactive(0.00001)
    
    def compose(self) -> app.ComposeResult:  
        try:
            self.header = CrustaceaHeader()
            yield self.header
            yield widg.Footer()
            self.statistics = CrustaceaStatistics()
            
            # To enable syntax highlighting, you'll need to install the `syntax` extra dependencies:
            # pip install "textual[syntax]"
            self.editor = edit.CrustaceaTextArea.code_editor(input_text, language="python", theme="vscode_dark")
            self.editor.read_only = True
            
            # connect statistics with the editor
            self.editor.count_error_up = self.statistics.count_error_up
            self.editor.count_char_up = self.statistics.count_char_up
            
            yield self.editor
            yield self.statistics
            
        except Exception as e:
            ic(e)
    
    def action_toggle_auto_tab(self):
        '''
        toggles the automatic usage of tabs at line start after pressing return at line end 
        '''
        self.editor.auto_tab = not self.editor.auto_tab
        
            

if __name__ == "__main__":
    ic("CrustaceaApp started...")
    CrustaceaApp().run()
        
