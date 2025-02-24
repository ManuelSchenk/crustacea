import operator

from textual.app import App, ComposeResult
from textual.widgets import Button, Digits
from textual.containers import Grid
from textual.reactive import reactive
from textual import on   # event listener decorator

from crustacea.utils.logging import ic

class CalculatorApp(App[None]):
    
    CSS_PATH = "styles/calculator.tcss"
    
    # we use reactive attributes to show the last clicked button on the display
    # each time such an reactive attribute changes you get an event/notification (like REACT states)
    number_displayed = reactive("0")
    result = reactive(0)
    
    
    def compose(self) -> ComposeResult:
        yield Digits(id='display')
        with Grid():
            yield Button("AC", classes="top-bottom")
            yield Button("+/-", classes="top-bottom")
            yield Button("%", classes="top-bottom")
            yield Button.warning("/", id="truediv", classes="operator")
            yield Button("7", id="number-7", classes="number-button")
            yield Button("8", id="number-8", classes="number-button")
            yield Button("9", id="number-9", classes="number-button")
            yield Button.warning("x", id="mul", classes="operator")
            yield Button("4", id="number-4", classes="number-button")
            yield Button("5", id="number-5", classes="number-button")
            yield Button("6", id="number-6", classes="number-button")
            yield Button.warning("-", id="sub", classes="operator")
            yield Button("1", id='number-1', classes="number-button")
            yield Button("2", id='number-2', classes="number-button")
            yield Button("3", id='number-3', classes="number-button")
            yield Button.warning("+", id="add", classes="operator")
            yield Button("0", id="number-0", classes='number-button')
            yield Button(",")
            yield Button.warning("=")
    
    @on(Button.Pressed, ".number-button")  # creates a event listener for Button presses which have class 'number_button' 
    def update_number_displayed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        __, __, digit = button_id.partition("-")
        self.number_displayed = self.number_displayed.lstrip("0") + digit
        ic("button was pressed")
    
    # special function with `watch_` prefix to react on reactive attribute changed
    def watch_number_displayed(self, new_value: str) -> None:
        """this watch method listen on the reactive attribute number_displayed
        and will run each time it changes and update the digits display"""
        self.query_one(Digits).update(new_value)
        ic("display was updated")
        
    @on(Button.Pressed, ".operator")
    def handle_operator(self, event: Button.Pressed) -> None:
        op_name = event.button.id
        operation = getattr(operator, op_name)
        ic(f"operator {op_name} was pressed")
        self.result = operation(self.result, int(self.number_displayed))    
        self.number_displayed = str(self.result)
        
if __name__ == "__main__":
    CalculatorApp().run()
        