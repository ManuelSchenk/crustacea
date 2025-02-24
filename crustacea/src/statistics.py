from textual.reactive import Reactive
import os
from time import monotonic 


import textual.widgets as widg 


class CrustaceaStatistics(widg.Static):    
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
    # timer 
    time_elapsed = Reactive(0.0001)
    start_time = monotonic()
    
    # counter
    error_counter = Reactive(0)
    char_counter = Reactive(0)
    
    def updated_statistics(self):
        # timer
        # time = self.time_elapsed
        # time, seconds = divmod(time, 60)
        # hours, minutes = divmod(time, 60)
        # time_str = f"Elapsed Time: {hours:02.0f}:{minutes:02.0f}:{seconds:02.1f}"
        
        char_per_minute = round(self.char_counter / (self.time_elapsed / 60), 1)
        char_min = f"Char/min: {char_per_minute}"
        # counter
        char_ctr = f"Char Counter: {self.char_counter}"
        err_ctr = f"Error Counter: {self.error_counter}"
        err_rate = f"Error Rate (err/100): {round((self.error_counter / (1 + self.char_counter)) * 100, 2)}" 
        points = f"Points: {int(self.char_counter * char_per_minute / (1 + self.error_counter))}"
        total_length = len(char_ctr) + len(err_ctr) + len(err_rate) + len(char_min) + len(points)
        spacing = (os.get_terminal_size().columns - total_length) // 5
        return f"{char_ctr}{' ' * spacing}{err_ctr}{' ' * spacing}{err_rate}{' ' * spacing}{char_min}{' ' * spacing}{points}"
    
    def update_time_elapsed(self): 
        self.time_elapsed = monotonic() - self.start_time
    
    def _on_mount(self):
        self.update_timer = self.set_interval(  # calls the method given in an interval
            1,
            self.update_time_elapsed, 
            pause=False   
        )
        self.update(self.updated_statistics())
    
    def count_error_up(self):
        self.error_counter += 1
        self.update(self.updated_statistics())
        
    def count_char_up(self):
        self.char_counter += 1
        self.update(self.updated_statistics())
        
    def watch_time_elapsed(self):  # functions with watch_ prefix react on changes of the Reactive variable with the same name
        self.update(self.updated_statistics()) 