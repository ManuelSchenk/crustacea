from textual.reactive import Reactive
import os

import textual.widgets as widg 


class CrustaceaStatistics(widg.Static):    
    """Display statistics of the editor."""
    
    DEFAULT_CSS = """  
    CrustaceaStatistics {
        height: 1;
        content-align: center middle;
        layout: horizontal;
        background: $boost;  /* this is a dynamic css color toggles when switch color mode */
        margin: 1; 
        padding-left: 2;
        text-opacity: 50%;
        width: 100%
    }
    """   
    
    def __init__(self):
        super().__init__()
        self.error_counter = 0
        self.char_counter = 0
    
    def on_mount(self):
        self.update_timer = self.set_interval(  # calls the callback given in an interval
            interval=1,
            callback=self.update_time_elapsed, 
            pause=False   
        )
    
    def update_time_elapsed(self): 
        self.update(self.updated_statistics())
    
    def updated_statistics(self):
        # poll timer from main app
        elapsed = self.screen.time_elapsed
        char_per_minute = round(self.char_counter / (elapsed / 60), 1)

        output_strings = [
            f"Char Counter: {self.char_counter:<6}",
            f"Error Counter: {self.error_counter:<6}",
            f"Error Rate (%): {round((self.error_counter / (1 + self.char_counter)) * 100, 2):<6}",
            f"Char/min: {char_per_minute:<6}",
            f"Score: {self.score(char_per_minute):<8}"
        ]
        self.space = self.spacing(output_strings)

        return f"{' ' * self.space}".join(output_strings)
    
    def score(self, char_per_minute):
        base_points = (self.char_counter * char_per_minute // 10)
        reducer = self.error_counter * 10
        difficulty = 1 - (
                (0.4 * self.screen.auto_backspace) +
                (0.2 * self.screen.auto_return) +
                (0.1 * self.screen.auto_tab)
                )
        return max(int((base_points - reducer) * difficulty), 0)
    
    def spacing(self, output_strings) -> int:
        total_string_length = len("".join(output_strings))
        return ((os.get_terminal_size().columns - total_string_length) // 5)
    
    def count_error_up(self):
        self.error_counter += 1
        self.update(self.updated_statistics())
        
    def count_char_up(self):
        self.char_counter += 1
        self.update(self.updated_statistics())
        