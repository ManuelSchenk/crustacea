from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, RadioSet, RadioButton, Button
from pathlib import Path

from crustacea.src.editor import EditorScreen
from crustacea.src.language_map import language_map


input_text = ""
text_folder = Path("./crustacea/texts")

class MenuScreen(Screen):
    
    DEFAULT_CSS = """
    MenuScreen {
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
    
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        # Create a RadioSet with a couple of options.
        py_files = list(text_folder.glob("*.*"))
        # Create a RadioSet with a radio button for each file.
        yield RadioSet(*(RadioButton(label=py_file.name) for py_file in py_files), id="radio_set")
        yield Button("Start Typing...", id="submit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            radio_set = self.query_one(RadioSet)
            # Retrieve the selected radio button’s id
            # selected_button = next(
            #     (radio for radio in radio_set.children if radio.pressed), None
            # )
            
            for radio in radio_set.children:
                if radio.value:
                    file_name = radio.label._text[0]
                    with open( text_folder / f"{file_name}", "r") as text:
                        lines = text.readlines()             
                        cleaned_lines = [line.rstrip() for line in lines]  
                        input_text = "\n".join(cleaned_lines)  
                    break
            
            # Get the file extension and look up the corresponding language
            ext = Path(file_name).suffix
            language = language_map.get(ext, "unknown")
            if input_text:
                # selected_option = selected_button.id  # or any property you set for your option
                self.app.push_screen(
                    EditorScreen(
                        input_text=input_text, 
                        language=language)
                    )
            else:
                self.app.log("No option selected.")