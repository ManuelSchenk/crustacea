
from textual import events
import textual.widgets as widg 
from rich.style import Style
from textual.strip import Strip

from crustacea.src.results_visualization import ResultVisualization

class CrustaceaTextArea(widg.TextArea):
    
    def __init__(self, *args, **kwargs) -> None:
        """This is the main TextArea/CodeEditor Component for Crustacea"""
        super().__init__(*args, **kwargs)
        self.type_error_flag = False
        self.original_theme_cursor_style = self._theme.cursor_style
        # suppress all mouse events on screen start
        self.app._driver._disable_mouse_support()
        self.insert_values = {
            "enter": "\n",
            "tab": "\t" if self.indent_type == "tabs" else (" " * self._find_columns_to_next_tab_stop())
        }
        

    async def _on_key(self, event: events.Key) -> None:
        """Handle key presses which correspond to document inserts."""
        # block everything if an type error is active till you press backspace
        if self.type_error_flag:
            if event.key == "backspace":
                self.type_error_flag = False
                self.toggle_cursor_style()
            else: 
                self.screen.statistics.count_error_up()
                return
            
        if event.is_printable or event.key in self.insert_values:
            event.stop()
            event.prevent_default()
            insert = self.insert_values.get(event.key, event.character)

            current_row, current_col = self.cursor_location
            next_char_position =  (
                    (current_row, current_col), 
                    (current_row, current_col + len(insert))
                )
            expected_char = self.document.get_text_range(*next_char_position)
                       
            # if the right character is typed
            if insert == expected_char:
                self.document.replace_range(
                        *next_char_position,
                        insert
                    )
                self.move_cursor_relative(0, len(insert))
                self.screen.statistics.count_char_up()
                
                # if auto return is enabled jump from last line clumn to next char available
                if self.screen.auto_return and current_col == len(self.document[current_row]) - 1:
                    self.move_to_next_char(current_row)
            
            # when return is pressed at the end of a line
            elif insert == "\n" and current_col == len(self.document[current_row]):
                self.move_to_next_char(current_row)
                self.screen.statistics.count_char_up()
                
            # this is the case if an typing fault is made  
            else: 
                self.screen.statistics.count_error_up()
                self.type_error_flag = True if not self.screen.auto_backspace else False
                # change cursor color to read and refresh the line immediately
                self.toggle_cursor_style()
            
    def move_to_next_char(self, current_row):
        """
        moves to the next available char after a return (or auto-return)
        If the end of the document is reached, this will fail and the except
        block will forward the user to the final statistics screen
        """
        try:
            next_row = 1 + (self.next_row_with_content_recursive(current_row))
            first_char = self.first_char_in_row(next_row)
            self.move_cursor((next_row, first_char))
        except: # this will fire when the cursor reach the last_line+1
            # close the editor and show statistic history for this filename as Sparkline
            self.screen.statistics.store_stats()  
            self.app.push_screen(ResultVisualization())
        
    def next_row_with_content_recursive(self, current_row: int) -> int: 
        """
        gives back the offset to the next row which contains content that is not only spaces
        """ 
        if len(set(self.document[current_row + 1])) <= 1: 
            current_row = self.next_row_with_content_recursive(current_row + 1)
        return current_row
    
    def first_char_in_row(self, row):
        """
        Return the index of the first non-space, non-tab character in the given line.
        """
        if not self.screen.auto_tab:
            return 0
        line = self.document[row]
        # Calculate the number of leading spaces and tabs
        index = len(line) - len(line.lstrip(" \t"))
        return index
                
    def toggle_cursor_style(self):
        """change the cursor color to red and refresh the line immediately"""
        if self.type_error_flag:
            self._theme.cursor_style = Style(color="#eeeeee", bgcolor="#ff0800", bold=True, blink=False)
            self._pause_blink(True)  
        else:
            self._theme.cursor_style = self.original_theme_cursor_style
            self._pause_blink(True)
            self._restart_blink()
        _, cursor_y = self._cursor_offset
        self.refresh_lines(cursor_y)
    

    # overwritten textual text_area functions ########################
    def render_line(self, y: int) -> Strip:
        """This dims all the lines except the current cursor_line for better focus at training."""
        self.styles.text_style = Style.combine([self.styles.text_style, Style(dim=True)])
        if self.screen.pause:
            self._theme.cursor_line_style = Style.combine([self._theme.cursor_line_style, Style(dim=True)])
        else:    
            self._theme.cursor_line_style = Style.combine([self._theme.cursor_line_style, Style(dim=False)])
        strip = super().render_line(y)
        return strip
        
    def scroll_cursor_visible(self, center: bool = True, animate: bool = True):
        """This centers the TextArea vertically, relative to the cursor line position"""
        super().scroll_cursor_visible(center, animate)

    def action_cursor_down(self, select: bool = False) -> None:
        if self.screen.enable_arrow_keys:
            super().action_cursor_down(select)
            
    def action_cursor_up(self, select: bool = False) -> None:
        if self.screen.enable_arrow_keys:
            super().action_cursor_up(select)
            
    def action_cursor_left(self, select: bool = False) -> None:
        if self.screen.enable_arrow_keys:
            super().action_cursor_left(select)
            
    def action_cursor_right(self, select: bool = False) -> None:
        if self.screen.enable_arrow_keys:
            super().action_cursor_right(select)
            
    def action_cursor_word_left(self, select: bool = False) -> None:
        if self.screen.enable_arrow_keys:
            super().action_cursor_word_left(select)
            
    def action_cursor_word_right(self, select: bool = False) -> None:
        if self.screen.enable_arrow_keys:
            super().action_cursor_word_right(select)
            
    def action_cursor_line_end(self, select: bool = False) -> None:
        if self.screen.enable_arrow_keys:
            super().action_cursor_line_end(select)
            
    def action_cursor_line_start(self, select: bool = False) -> None:
        if self.screen.enable_arrow_keys:
            super().action_cursor_line_start(select)
