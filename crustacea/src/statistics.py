from textual.reactive import Reactive
import os

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
    
    error_counter = Reactive(0)
    char_counter = Reactive(0)
    
    def updated_statistics(self):
        char_ctr = f"Char Counter: {self.char_counter}"
        err_ctr = f"Error Counter: {self.error_counter}"
        err_rate = f"Error Rate (err/100): {round((self.error_counter / (1 + self.char_counter)) * 100, 2)}" 
        total_length = len(char_ctr) + len(err_ctr) + len(err_rate)
        spacing = (os.get_terminal_size().columns - total_length) // 4
        return f"{char_ctr}{' ' * spacing}{err_ctr}{' ' * spacing}{err_rate}"
    
    def _on_mount(self, event):
        self.update(self.updated_statistics())
    
    def count_error_up(self):
        self.error_counter += 1
        self.update(self.updated_statistics())
        
    def count_char_up(self):
        self.char_counter += 1
        self.update(self.updated_statistics())
        
    # def watch_error_counter(self):
    #     self.update(f"Current Error Counter: {self.error_counter}")
        