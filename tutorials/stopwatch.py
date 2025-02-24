# ~ @'/?\|-_
    

   

from time import monotonic 
from textual import on 
from textual.app import App
from textual.widgets import Footer, Header, Button, Static
from textual.reactive import Reactive
from textual.containers import ScrollableContainer

from crustacea.utils.logging import ic

class TimeDisplay(Static):
    """Custom time display widget."""
    accumulated_time = 0
    time_elapsed = Reactive(0)
    start_time = monotonic()
    
    def on_mount(self): # handler method which is triggered when TimeDisplay is shown
        self.update_timer = self.set_interval(  # calls the method given in an interval
            1 / 60,
            self.update_time_elapsed, 
            pause=True   # this starts the timer paused (can be "resume()"")
        )
    
    def update_time_elapsed(self): 
        self.time_elapsed = (monotonic() - self.start_time) + self.accumulated_time
    
    def watch_time_elapsed(self):  # functions with watch_ prefix react on changes of the Reactive variable with the same name
        time = self.time_elapsed
        time, seconds = divmod(time, 60)
        hours, minutes = divmod(time, 60)
        time_string = f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"
        self.update(str(time_string)) # this updates the widget content with the given text
    
    def start(self):
        """start keeping track of elapsed time"""
        self.start_time = monotonic() 
        self.update_timer.resume()

    def stop(self):
        """stop the timer"""
        self.update_timer.pause()
        self.accumulated_time = self.time_elapsed

    def reset(self):
        """resets the counter"""
        self.time_elapsed = 0
        self.accumulated_time = 0



class Stopwatch(Static): # Static is a widget to display simple static content, or use as a base class for more complex widgets
    """Custom stopwatch widget."""
    def compose(self):
        yield Button(
            "Start", variant="success", id="start"
            )
        yield Button(
            "Stop", variant="error", id="stop"
            )
        yield Button("Reset", id="reset")      
        yield TimeDisplay("00:00:00.00")
    
    @on(Button.Pressed, "#start")
    def start_stopwatch(self):
        ic("START Button pressed...")
        self.add_class("started")
        self.query_one(TimeDisplay).start()   # you can query for the python class itself (no string)
        
    @on(Button.Pressed, "#stop")
    def stop_stopwatch(self):
        ic("STOP Button pressed...")
        self.remove_class("started")
        
        time_display = self.query_one("TimeDisplay")   # with this you can query for children of Stopwatch parent
        # time_display.time_elapsed = 7.3   # after getting the element with 'query_one' you can modifiy it as usual
        time_display.stop()
    
    @on(Button.Pressed, "#reset")
    def reset_stopwatch(self):
        id("RESET button pressed...")
        self.stop_stopwatch()
        self.query_one(TimeDisplay).reset()

        

class StopwatchApp(App):
    
    # to add a key-shortcut binding, we need to define a triple in the BINDING list
    # of the form (key, action_method_name (methods which should run), description)
    BINDINGS = [
        ("d", "toggle_dark_mode", "Toggle Dark Mode"),
        ("a", "add_stopwatch", "Add a watch"),
        ("r", "remove_stopwatch", "Remove a watch"),
    ]
    
    # to style our app we use textual CSS
    CSS_PATH = "styles/stopwatch.tcss"
    
    def compose(self):
        '''
        Textual expect this method in each app because,
        It defines of which widgets the app is COMPOSED of!
        '''
        yield Header(show_clock=True)
        with ScrollableContainer(id="stopwatches"): # to nest elements into containers you can use the WITH statement "context manager"
            yield Stopwatch(classes="started")
            yield Stopwatch()
            yield Stopwatch()
        yield Footer()

    def action_toggle_dark_mode(self):
        '''
        An textual ACTION method toggles the dark mode state
        the prefix 'action_' makes it to a ACTION method and is important!
        '''
        self.theme = ("textual-dark" if self.theme == 'textual-light' else 'textual-light')
        ic(self.theme)
        
    def action_add_stopwatch(self):
        new_stopwatch = Stopwatch()
        container = self.query_one("#stopwatches")
        container.mount(new_stopwatch)   #  this mounts the widget onto the App
        new_stopwatch.scroll_visible()  # makes the new one visible if outside of scroll scope
    
    def action_remove_stopwatch(self): 
        stopwatches = self.query(Stopwatch)   # this gives back all the Stopwatches
        if stopwatches:
            stopwatches.last().remove()  # removes the last stopwatch

if __name__ == "__main__":
    StopwatchApp().run()
    
