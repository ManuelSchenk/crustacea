from textual.app import ComposeResult

from textual.screen import Screen
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Static

from crustacea.src.results_storage import StorageContext
from crustacea.src.results_sparkline import StatisticHorizontal


class ResultVisualization(Screen):
    
    DEFAULT_CSS = """\
        #headline {
            content-align: center middle;
            padding-top:2;
            color: $foreground 40%;
        }
        #underline {
            content-align: center middle;
        }
        VerticalScroll {
            padding-bottom: 4;
            padding-left: 10;
            padding-right: 10;
        }
        #table_title {
            padding-top: 2;
            height: 3;
            color: $foreground 30%;
        }
        Horizontal > Static.type_title {
            width: 20%;
            content-align: right middle;
        }
        Horizontal > Static.history_title {
            content-align: center middle;
            width: 60%;
        }
        Horizontal > Static.result_title {
            content-align: left middle;
            width: 20%;
        }
    """


    def compose(self) -> ComposeResult:
        # Huge Headline centered
        yield Static("""
 ██████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗  █████╗ ████████╗██╗   ██╗██╗      █████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗
██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██╔══██╗╚══██╔══╝██║   ██║██║     ██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
██║     ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝███████║   ██║   ██║   ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║███████╗
██║     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██╔══██║   ██║   ██║   ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║╚════██║
╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝███████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║███████║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
            """, id="headline")
        yield Static("You have finished the Lecture!", id="underline")
            
        # Table Title
        with Horizontal(id="table_title"):
            yield Static("Result Type", classes="type_title")
            yield Static("History (global)", classes="history_title")
            yield Static("Current Result", classes="result_title")
        
        # Results visualized with Sparklines
        with VerticalScroll():
            for result_name in reversed([
                "Char Counter", "Error Counter", "Error Rate (%)", "Char/min", "Score"
                ]):
                yield StatisticHorizontal(result_name, self.get_data_for(result_name))

        
    def get_data_for(self, result_name):
        """Calls the historical results from StorageContext for visualization"""
        clean_res_name = result_name.lower().replace(" (%)", "").replace(" ", "_").replace("/", "_")
        
        with StorageContext() as db:
            sqlite_response = db.query(f"SELECT {clean_res_name} FROM score_table")
            # transform the sqlite data into a plain list
            data = [row[0] for row in sqlite_response]
        return data
        
            
