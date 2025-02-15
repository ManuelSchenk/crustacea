
import textual.app as app
import textual.widgets as widg # Footer, Header, Button, Static
from textual import events


from crustacea.utils.logging import ic 

example_text = ""
with open("./tutorials/stopwatch.py", "r") as text:
    example_text = text.read()

class CrustaceaApp(app.App):
    
    def _on_key(self, event: events.Key) -> None:
        next_row, next_col = self.editor.cursor_location
        
        ic(str(self.editor.document.get_text_range(
            self.editor.cursor_location, 
            (next_row, next_col + 1))
            ))
        # event.prevent_default()
    
    def compose(self):
        
        yield widg.Header(show_clock=True)
        yield widg.Footer()
        
        self.editor = widg.TextArea.code_editor(example_text, language="python", theme="vscode_dark")
        yield self.editor
            
            
        
    # To enable syntax highlighting, you'll need to install the `syntax` extra dependencies:
    # pip install "textual[syntax]"
        

if __name__ == "__main__":
    CrustaceaApp().run()
        
