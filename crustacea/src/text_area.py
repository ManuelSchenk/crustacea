
from textual import events
import textual.widgets as widg 
from crustacea.utils.logging import ic 
from textual.reactive import Reactive
from rich.style import Style
from textual.strip import Strip
from textual.document._document import _utf8_encode
from textual.expand_tabs import expand_text_tabs_from_widths
from textual.widgets._text_area import build_byte_to_codepoint_dict

class CrustaceaTextArea(widg.TextArea):
     
      
    auto_tab = Reactive(True)
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type_error_flag = False
        self.original_theme_cursor_style = self._theme.cursor_style
        # suppress all mouse events on screen start
        self.app._driver._disable_mouse_support()

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
            assert insert is not None

            # The following is the custom crustacea logic:
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
                self.screen.statistics.count_char_up()
            elif insert == "\n" and current_col == len(self.document[current_row]):
                next_row = 1 + (self.next_row_with_content(current_row))
                first_char = self.first_char_in_row(next_row)
                self.move_cursor((next_row, first_char))
                self.screen.statistics.count_char_up()
            else: # this is the case if an typing fault is made
                self.screen.statistics.count_error_up()
                self.type_error_flag = True if self.screen.forced_backspace_error else False
                # change cursor color to read and refresh the line immediately
                self.toggle_cursor_style()
                
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
    
    def next_row_with_content(self, current_row: int) -> int: 
        """gives back the offset int to the next row with content that is not only spaces"""
        if len(set(self.document[current_row + 1])) <= 1: 
            current_row = self.next_row_with_content(current_row + 1)
        return current_row
    
    def first_char_in_row(self, row):
        """
        Return the index of the first non-space, non-tab character in the given line.
        """
        if not self.auto_tab:
            return 0
        line = self.document[row]
        # Calculate the number of leading spaces and tabs
        index = len(line) - len(line.lstrip(" \t"))
        ic(index)
        return index
    
    
    # overwritten textual text_area functions ########################
    def render_line(self, y: int) -> Strip:
        # dim all lines except the cursor_line
        self.styles.text_style = Style.combine([self.styles.text_style, Style(dim=True)])
        if self.screen.pause:
            self._theme.cursor_line_style = Style.combine([self._theme.cursor_line_style, Style(dim=True)])
        else:    
            self._theme.cursor_line_style = Style.combine([self._theme.cursor_line_style, Style(dim=False)])
        strip = super().render_line(y)
        return strip
        
    def scroll_cursor_visible(self, center: bool = True, animate: bool = True):
        """This activates the center and animate of the original textual scroll function"""
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
