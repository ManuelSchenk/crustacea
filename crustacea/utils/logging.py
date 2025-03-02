from icecream import ic
from datetime import datetime
import inspect


def custom_ic_output(arg):
    frame = inspect.currentframe().f_back.f_back
    line_number = frame.f_lineno
    output_string = f"{datetime.now().strftime('%Y%m%d_%H:%M:%S')} | Line: {line_number} | {arg[3:].strip()}\n"
    with open('ic.log', 'a') as f:
        f.write(output_string)

ic.configureOutput(includeContext=True, outputFunction=custom_ic_output)
