from textual.app import App
from textual.widgets import Footer, Header, Button

from crispy_crustacea.utils.logging import ic

class StopwatchApp(App):
    
    # to add a shortcut binding, we need to define a triple in the BINDING list
    # of the form (key, action_method_name (methods which should run), description)
    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle Dark Mode"),
    ]
    
    def compose(self):
        '''
        Textual expect this method in each app because,
        It defines of which widgets the app is COMPOSED of!
        '''
        yield Header(show_clock=True)
        yield Button("Start")
        yield Button("Stop")
        yield Button("Reset")        
        yield Footer()

    def action_toggle_dark_mode(self):
        '''
        An textual ACTION method toggles the dark mode state
        the prefix 'action_' makes it to a ACTION method and is important!
        '''
        self.theme = ("textual-dark" if self.theme == 'textual-light' else 'textual-light')
        ic(self.theme)

if __name__ == "__main__":
    StopwatchApp().run()
    
