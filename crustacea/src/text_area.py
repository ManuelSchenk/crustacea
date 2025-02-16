
from textual import events
import textual.widgets as widg 

class CrustaceaTextArea(widg.TextArea):
    def _on_key(self, event: events.Key) -> None:
    next_row, next_col = self.editor.cursor_location
    next_char_position =  (
            (next_row, next_col), 
            (next_row, next_col + 1)
        )
    expected_char = self.editor.document.get_text_range(*next_char_position)
    # ic(str(character))

    if event.character:    
        if event.key == expected_char:
            self.editor.document.replace_range(
                    *next_char_position,
                    event.key
                )
            self.editor.move_cursor_relative(0, 1)
        event.prevent_default(True)
    
    event.prevent_default(False)

async def _on_key(self, event: events.Key) -> None:
        """Handle key presses which correspond to document inserts."""
        self._restart_blink()
        if self.read_only:
            return

        key = event.key
        insert_values = {
            "enter": "\n",
        }
        if self.tab_behavior == "indent":
            if key == "escape":
                event.stop()
                event.prevent_default()
                self.screen.focus_next()
                return
            if self.indent_type == "tabs":
                insert_values["tab"] = "\t"
            else:
                insert_values["tab"] = " " * self._find_columns_to_next_tab_stop()

        if event.is_printable or key in insert_values:
            event.stop()
            event.prevent_default()
            insert = insert_values.get(key, event.character)
            # `insert` is not None because event.character cannot be
            # None because we've checked that it's printable.
            assert insert is not None
            start, end = self.selection
            self._replace_via_keyboard(insert, start, end)
