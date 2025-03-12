import os
import textual.widgets as widg 

from crustacea.src.results_storage import StorageContext


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
        self.char_per_minute = 0.0
        self.error_rate = 0.0
    
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
        self.char_per_minute = round(self.char_counter / (elapsed / 60), 1)
        self.error_rate = round((self.error_counter / (1 + self.char_counter)) * 100, 2)

        output_strings = [
            f"Char Counter: {self.char_counter:<6}",
            f"Error Counter: {self.error_counter:<6}",
            f"Error Rate (%): {self.error_rate:<6}",
            f"Char/min: {self.char_per_minute:<6}",
            f"Score: {self.score():<8}"
        ]
        self.space = self.spacing(output_strings)

        return f"{' ' * self.space}".join(output_strings)

    def store_stats(self):
        with StorageContext() as db:
            row_id = db.insert_result(
                filename=self.screen.filename,
                char_counter=self.char_counter,
                error_counter=self.error_counter,
                error_rate=self.error_rate,
                char_per_min=self.char_per_minute,
                score=self.score(),
                )
    
    def score(self):
        base_points = (self.char_counter * self.char_per_minute // 10)
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
        
        