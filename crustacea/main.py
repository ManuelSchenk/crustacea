import textual.app as app
import textual.widgets as widg 
import crustacea.src.text_area as editor


from crustacea.utils.logging import ic 

example_text = ""
with open("./tutorials/stopwatch.py", "r") as text:
    example_text = text.read()

class CrustaceaApp(app.App):
    
    
    def compose(self):  
        yield widg.Header(show_clock=True)
        yield widg.Footer()
        
        # To enable syntax highlighting, you'll need to install the `syntax` extra dependencies:
        # pip install "textual[syntax]"
        self.editor = editor.CrustaceaTextArea.code_editor(example_text, language="python", theme="vscode_dark")
        # self.editor.read_only = True
        yield self.editor
            
            
        
        

if __name__ == "__main__":
    CrustaceaApp().run()
        
