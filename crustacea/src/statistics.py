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
    # reactive counter will automatically update the static element if changed
    error_counter = Reactive(0)
    char_counter = Reactive(0)
    
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
        elapsed = self.app.time_elapsed
        char_per_minute = round(self.char_counter / (elapsed / 60), 1)
        char_min = f"Char/min: {char_per_minute}"
        # calculate counter statistics
        char_ctr = f"Char Counter: {self.char_counter:<6}"
        err_ctr = f"Error Counter: {self.error_counter:<6}"
        err_rate = f"Error Rate (err/100): {round((self.error_counter / (1 + self.char_counter)) * 100, 2):<6}" 
        score = f"Score: {int(self.char_counter * char_per_minute / (1 + self.error_counter)):<8}"
        # calculate spacing
        total_length = len(char_ctr) + len(err_ctr) + len(err_rate) + len(char_min) + len(score)
        spacing = (os.get_terminal_size().columns - total_length) // 5
        return f"{char_ctr}{' ' * spacing}{err_ctr}{' ' * spacing}{err_rate}{' ' * spacing}{char_min}{' ' * spacing}{score}"
    
    def count_error_up(self):
        self.error_counter += 1
        self.update(self.updated_statistics())
        
    def count_char_up(self):
        self.char_counter += 1
        self.update(self.updated_statistics())
        