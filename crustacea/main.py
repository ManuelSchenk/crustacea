import textual.app as app
from crustacea.src.menu import MenuScreen


class Crustacea(app.App):
    

    def on_mount(self) -> None:
        # Start with the menu screen.
        self.push_screen(MenuScreen())

        
if __name__ == "__main__":
    Crustacea().run(mouse=True)
