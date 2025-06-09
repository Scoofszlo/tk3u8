from rich.console import Console
from rich.live import Live  # noqa: F401
from rich.table import Table


console = Console()


def render_lines(*args: str) -> Table:
    table = Table.grid()
    for message in args:
        table.add_row(message)
    return table
