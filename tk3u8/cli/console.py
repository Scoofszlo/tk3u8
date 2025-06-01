from rich.console import Console
from rich.live import Live
from rich.table import Table


console = Console()


def render_lines(*args):
    table = Table.grid()
    for message in args:
        table.add_row(message)
    return table
