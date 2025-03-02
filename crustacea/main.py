import textual.app as app
from crustacea.src.filemenu import FileMenuScreen


class Crustacea(app.App):
    
    def on_mount(self) -> None:
        # Start with the menu screen.
        self.push_screen(FileMenuScreen())

        
if __name__ == "__main__":
    Crustacea().run(mouse=True)
