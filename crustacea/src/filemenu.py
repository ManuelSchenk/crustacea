from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, RadioSet, RadioButton, Button
from pathlib import Path
from textual.binding import Binding

from crustacea.src.editor import EditorScreen
from crustacea.src.language_map import language_map


text_folder = Path(__file__).parents[1] / "texts"

class FileMenuScreen(Screen):
    
    DEFAULT_CSS = """
    FileMenuScreen {
        align: center middle;
    }
    #radio_set {
        width: 50%;
    }
    #submit {
        width: 50%;
        margin: 1;
        margin-right: 3;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", 
                tooltip="Quit the app and return to the command prompt.", 
                show=True, priority=True),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        # Create a RadioSet with a couple of options.
        py_files = list(text_folder.glob("*.*"))
        # Create a RadioSet with a radio button for each file.
        yield RadioSet(*(RadioButton(label=py_file.name) for py_file in py_files), id="radio_set")
        yield Button("Start Typing...", variant="primary", id="submit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        input_text = ""
        if event.button.id == "submit":
            radio_set = self.query_one(RadioSet)
            
            for radio in radio_set.children:
                if radio.value:
                    file_name = radio.label._text[0]
                    with open( text_folder / f"{file_name}", "r") as text:
                        lines = text.readlines()             
                        cleaned_lines = [line.rstrip() for line in lines]  
                        input_text = "\n".join(cleaned_lines)  
                    break
                
            if not input_text:
                return
            
            # Get the file extension and look up the corresponding language
            ext = Path(file_name).suffix
            language = language_map.get(ext, "unknown")
            if input_text:
                # selected_option = selected_button.id  # or any property you set for your option
                self.app.push_screen(
                    EditorScreen(
                        filename=file_name,
                        input_text=input_text, 
                        language=language)
                    )
