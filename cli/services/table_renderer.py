from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.style import Style

def render_table(title: str, columns: List[str], items: List[Dict[str, Any]]) -> None:
    """Render a styled table using rich with the given title, columns, and items."""
    console = Console()
    table = Table(title=title, header_style="bold yellow", show_lines=True)
    for i, col in enumerate(columns):
        if i == 0:
            table.add_column(col.replace("_", " ").title(), style="bold cyan")
        else:
            table.add_column(col.replace("_", " ").title(), style="white")
    for idx, item in enumerate(items):
        row_values = []
        for i, col in enumerate(columns):
            value = str(item.get(col, "n/a"))
            if i == 0:
                value = f"[bold]{value}[/bold]"
            row_values.append(value)
        style = "on grey15" if idx % 2 == 1 else ""
        table.add_row(*row_values, style=style)
    console.print(table) 