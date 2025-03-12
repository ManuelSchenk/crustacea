import textual.app as app
from crustacea.src.filemenu import FileMenuScreen


class Crustacea(app.App):
    
    def on_mount(self) -> None:
        # Start with the menu screen.
        self.push_screen(FileMenuScreen())


def main():
    Crustacea().run(mouse=True)
    
        
if __name__ == "__main__":
    main()
