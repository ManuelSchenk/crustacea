import textual.app as app
import textual.widgets as widg 
import crustacea.src.text_area as edit
from crustacea.src.statistics import CrustaceaStatistics
from textual.reactive import Reactive


from crustacea.utils.logging import ic 

input_text = ""
with open("./tutorials/stopwatch.py", "r") as text:
    raw_text = text.read()
    input_text = raw_text .replace(" \n", "\n")


class CrustaceaApp(app.App):
    
    def compose(self) -> app.ComposeResult:  
        try:
            yield widg.Header(show_clock=True)
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
            

if __name__ == "__main__":
    CrustaceaApp().run()
        
