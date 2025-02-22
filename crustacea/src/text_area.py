
from textual import events
import textual.widgets as widg 
# from crustacea.utils.logging import ic 


class CrustaceaTextArea(widg.TextArea):
   
    async def _on_key(self, event: events.Key) -> None:
        """Handle key presses which correspond to document inserts."""
        self._restart_blink()       
        insert_values = {
            "enter": "\n",
        }
        if self.tab_behavior == "indent":  # this is true for code_editor
            if event.key == "escape":
                event.stop()
                event.prevent_default()
                self.screen.focus_next()
                return
            if self.indent_type == "tabs":  # this is not default
                insert_values["tab"] = "\t"
            else:
                insert_values["tab"] = " " * self._find_columns_to_next_tab_stop()

        if event.is_printable or event.key in insert_values:
            event.stop()
            event.prevent_default()
            insert = insert_values.get(event.key, event.character)
            # `insert` is not None because event.character cannot be
            # None because we've checked that it's printable.
            assert insert is not None

            # The following is the crustacea logic:
            current_row, current_col = self.cursor_location
            next_char_position =  (
                    (current_row, current_col), 
                    (current_row, current_col + len(insert))
                )
            expected_char = self.document.get_text_range(*next_char_position)
            if insert == expected_char:
                self.document.replace_range(
                        *next_char_position,
                        insert
                    )
                self.move_cursor_relative(0, len(insert))
                self.count_char_up()
            elif insert == "\n" and current_col == len(self.document[current_row]):
                self.move_cursor((1 + (self.next_row_with_content(current_row)), 0))
                self.count_char_up()
            else:
                self.count_error_up()
                # ic(f"The wrong key was pressed: {event.key}")
    
    def next_row_with_content(self, current_row: int) -> int: 
        """gives back the offset int to the next row with content that is not only spaces"""
        if len(set(self.document[current_row + 1])) <= 1: 
            current_row = self.next_row_with_content(current_row + 1)
        return current_row
    
    def assign_error_counter(self, count_up_func):
        self.count_up = count_up_func
        
            
            
                
