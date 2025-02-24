
from textual import events
import textual.widgets as widg 
from crustacea.utils.logging import ic 
from textual.reactive import Reactive
from rich.style import Style
from textual.strip import Strip
from rich.text import Text
from textual.document._document import _utf8_encode
from textual.expand_tabs import expand_text_tabs_from_widths
from textual.widgets._text_area import build_byte_to_codepoint_dict

class CrustaceaTextArea(widg.TextArea):
     
      
    auto_tab = Reactive(True)
    
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type_error_flag = False

    async def _on_key(self, event: events.Key) -> None:
        """Handle key presses which correspond to document inserts."""
        # block everything if an type error is active till you press backspace
        if self.type_error_flag:
            if event.key == "backspace":
                self.type_error_flag = False
            else: 
                self.app.statistics.count_error_up()
                return
            
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
                self.app.statistics.count_char_up()
            elif insert == "\n" and current_col == len(self.document[current_row]):
                next_row = 1 + (self.next_row_with_content(current_row))
                first_char = self.first_char_in_row(next_row)
                self.move_cursor((next_row, first_char))
                self.app.statistics.count_char_up()
            else:
                self.app.statistics.count_error_up()
                self.type_error_flag = True if self.app.forced_backspace_error else False
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
    
    
    
    # overwritten textual text area functions ########################
    
    def scroll_cursor_visible(self, center: bool = True, animate: bool = True):
        """This activates the center and animate of the original textual scroll function"""
        super().scroll_cursor_visible(center, animate)

    def action_cursor_down(self, select: bool = False) -> None:
        if self.app.enable_arrow_keys:
            super().action_cursor_down(select)
            
    def action_cursor_up(self, select: bool = False) -> None:
        if self.app.enable_arrow_keys:
            super().action_cursor_up(select)
            
    def action_cursor_left(self, select: bool = False) -> None:
        if self.app.enable_arrow_keys:
            super().action_cursor_left(select)
            
    def action_cursor_right(self, select: bool = False) -> None:
        if self.app.enable_arrow_keys:
            super().action_cursor_right(select)
            
    def action_cursor_word_left(self, select: bool = False) -> None:
        if self.app.enable_arrow_keys:
            super().action_cursor_word_left(select)
            
    def action_cursor_word_right(self, select: bool = False) -> None:
        if self.app.enable_arrow_keys:
            super().action_cursor_word_right(select)
            
    def action_cursor_line_end(self, select: bool = False) -> None:
        if self.app.enable_arrow_keys:
            super().action_cursor_line_end(select)
            
    def action_cursor_line_start(self, select: bool = False) -> None:
        if self.app.enable_arrow_keys:
            super().action_cursor_line_start(select)
            
 
    def render_line(self, y: int) -> Strip:
        """Render a single line of the TextArea. Called by Textual.

        this is the original function from TextArea,
        i have manipulate only two parts to make the cursor red and the current line bold
        """
        theme = self._theme
        if theme:
            theme.apply_css(self)

        wrapped_document = self.wrapped_document
        scroll_x, scroll_y = self.scroll_offset

        # Account for how much the TextArea is scrolled.
        y_offset = y + scroll_y

        # If we're beyond the height of the document, render blank lines
        out_of_bounds = y_offset >= wrapped_document.height

        if out_of_bounds:
            return Strip.blank(self.size.width)

        # Get the line corresponding to this offset
        try:
            line_info = wrapped_document._offset_to_line_info[y_offset]
        except IndexError:
            line_info = None

        if line_info is None:
            return Strip.blank(self.size.width)

        line_index, section_offset = line_info

        line = self.get_line(line_index)
        line_character_count = len(line)
        line.tab_size = self.indent_width
        line.set_length(line_character_count + 1)  # space at end for cursor
        virtual_width, _virtual_height = self.virtual_size

        selection = self.selection
        start, end = selection
        cursor_row, cursor_column = end

        selection_top, selection_bottom = sorted(selection)
        selection_top_row, selection_top_column = selection_top
        selection_bottom_row, selection_bottom_column = selection_bottom

        cursor_line_style = theme.cursor_line_style if theme else None
        if cursor_line_style and cursor_row == line_index:
            line.stylize(cursor_line_style)
            
        # dim the lines the cursor is not currently in
        if cursor_row != line_index:
            non_cursor_line_style = Style(bold=True, dim=True, frame=True)
            line.stylize(non_cursor_line_style)

        # Selection styling
        if start != end and selection_top_row <= line_index <= selection_bottom_row:
            # If this row intersects with the selection range
            selection_style = theme.selection_style if theme else None
            cursor_row, _ = end
            if selection_style:
                if line_character_count == 0 and line_index != cursor_row:
                    # A simple highlight to show empty lines are included in the selection
                    line = Text("▌", end="", style=Style(color=selection_style.bgcolor))
                else:
                    if line_index == selection_top_row == selection_bottom_row:
                        # Selection within a single line
                        line.stylize(
                            selection_style,
                            start=selection_top_column,
                            end=selection_bottom_column,
                        )
                    else:
                        # Selection spanning multiple lines
                        if line_index == selection_top_row:
                            line.stylize(
                                selection_style,
                                start=selection_top_column,
                                end=line_character_count,
                            )
                        elif line_index == selection_bottom_row:
                            line.stylize(selection_style, end=selection_bottom_column)
                        else:
                            line.stylize(selection_style, end=line_character_count)

        highlights = self._highlights
        if highlights and theme:
            line_bytes = _utf8_encode(line.plain)
            byte_to_codepoint = build_byte_to_codepoint_dict(line_bytes)
            get_highlight_from_theme = theme.syntax_styles.get
            line_highlights = highlights[line_index]
            for highlight_start, highlight_end, highlight_name in line_highlights:
                node_style = get_highlight_from_theme(highlight_name)
                if node_style is not None:
                    line.stylize(
                        node_style,
                        byte_to_codepoint.get(highlight_start, 0),
                        byte_to_codepoint.get(highlight_end) if highlight_end else None,
                    )

        # Highlight the cursor
        matching_bracket = self._matching_bracket_location
        match_cursor_bracket = self.match_cursor_bracket
        draw_matched_brackets = (
            match_cursor_bracket and matching_bracket is not None and start == end
        )

        if cursor_row == line_index:
            draw_cursor = (
                self.has_focus
                and not self.cursor_blink
                or (self.cursor_blink and self._cursor_visible)
            )
            if draw_matched_brackets:
                matching_bracket_style = theme.bracket_matching_style if theme else None
                if matching_bracket_style:
                    line.stylize(
                        matching_bracket_style,
                        cursor_column,
                        cursor_column + 1,
                    )

            if draw_cursor:
                if self.type_error_flag:
                    cursor_style=Style(color="#eeeeee", bgcolor="#ff0800", bold=True, blink=False)
                    self._pause_blink(True)  # to make the cursor visible immediately

                else:
                    cursor_style = theme.cursor_style if theme else None
                    
                if cursor_style:
                    line.stylize(cursor_style, cursor_column, cursor_column + 1)

        # Highlight the partner opening/closing bracket.
        if draw_matched_brackets:
            # mypy doesn't know matching bracket is guaranteed to be non-None
            assert matching_bracket is not None
            bracket_match_row, bracket_match_column = matching_bracket
            if theme and bracket_match_row == line_index:
                matching_bracket_style = theme.bracket_matching_style
                if matching_bracket_style:
                    line.stylize(
                        matching_bracket_style,
                        bracket_match_column,
                        bracket_match_column + 1,
                    )

        # Build the gutter text for this line
        gutter_width = self.gutter_width
        if self.show_line_numbers:
            if cursor_row == line_index:
                gutter_style = theme.cursor_line_gutter_style
            else:
                gutter_style = theme.gutter_style

            gutter_width_no_margin = gutter_width - 2
            gutter_content = (
                str(line_index + self.line_number_start) if section_offset == 0 else ""
            )
            gutter = Text(
                f"{gutter_content:>{gutter_width_no_margin}}  ",
                style=gutter_style or "",
                end="",
            )
        else:
            gutter = Text("", end="")

        # TODO: Lets not apply the division each time through render_line.
        #  We should cache sections with the edit counts.
        wrap_offsets = wrapped_document.get_offsets(line_index)
        if wrap_offsets:
            sections = line.divide(wrap_offsets)  # TODO cache result with edit count
            line = sections[section_offset]
            line_tab_widths = wrapped_document.get_tab_widths(line_index)
            line.end = ""

            # Get the widths of the tabs corresponding only to the section of the
            # line that is currently being rendered. We don't care about tabs in
            # other sections of the same line.

            # Count the tabs before this section.
            tabs_before = 0
            for section_index in range(section_offset):
                tabs_before += sections[section_index].plain.count("\t")

            # Count the tabs in this section.
            tabs_within = line.plain.count("\t")
            section_tab_widths = line_tab_widths[
                tabs_before : tabs_before + tabs_within
            ]
            line = expand_text_tabs_from_widths(line, section_tab_widths)
        else:
            line.expand_tabs(self.indent_width)

        base_width = (
            self.scrollable_content_region.size.width
            if self.soft_wrap
            else max(virtual_width, self.region.size.width)
        )
        target_width = base_width - self.gutter_width
        console = self.app.console
        gutter_segments = console.render(gutter)

        text_segments = list(
            console.render(line, console.options.update_width(target_width))
        )

        gutter_strip = Strip(gutter_segments, cell_length=gutter_width)
        text_strip = Strip(text_segments)

        # Crop the line to show only the visible part (some may be scrolled out of view)
        if not self.soft_wrap:
            text_strip = text_strip.crop(scroll_x, scroll_x + virtual_width)

        # Stylize the line the cursor is currently on.
        if cursor_row == line_index:
            line_style = cursor_line_style
        else:
            line_style = theme.base_style if theme else None

        text_strip = text_strip.extend_cell_length(target_width, line_style)
        strip = Strip.join([gutter_strip, text_strip]).simplify()

        return strip.apply_style(
            theme.base_style
            if theme and theme.base_style is not None
            else self.rich_style
        )