from icecream import ic
from datetime import datetime
import inspect
import os


def custom_ic_output(arg):
    frame = inspect.currentframe().f_back.f_back
    line_number = frame.f_lineno
    with open('ic.log', 'a') as f:
        f.write(f"{datetime.now().strftime('%Y%m%d_%H:%M:%S')} | Line: {line_number} | {arg[3:].strip()}\n")

ic.configureOutput(includeContext=True, outputFunction=custom_ic_output)
