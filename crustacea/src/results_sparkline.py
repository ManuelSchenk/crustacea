from textual.widgets import Sparkline
from textual.containers import Horizontal
from textual.widgets import Static

class StatisticHorizontal(Horizontal):
    
    DEFAULT_CSS = """
        StatisticHorizontal {
            height: 5;
        }
        /* Target elements inside Static using IDs */
        StatisticHorizontal > Static#title {
            width: 20%;
            height: 100%;
            content-align: right middle;
            padding-right: 4;
            border: solid $boost; 
        }
        StatisticHorizontal > Sparkline#spark_line {
            content-align: center middle;
            width: 60%;
            height: 100%;
            border: solid $boost; 
            padding-left: 2;
            padding-right: 2;
        }
        StatisticHorizontal > Static#current_result {
            content-align: left middle;
            width: 20%;
            height: 100%;
            border: solid $boost; 
            padding-left: 4;
        }
    """
    
    def __init__(self, title, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.data = data
        self.current_result = str(data[-1])
        
        
    def compose(self):
        yield Static(self.title, id="title")
        yield Sparkline(
            # [random.randint(0, 100) for _ in range(20)], 
            self.data,
            summary_function=max,
            id="spark_line")
        yield Static(self.current_result, id="current_result")