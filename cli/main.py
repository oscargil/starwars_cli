from typing import List, Optional
import typer
from config import API_BASE_URL
from services.api_client import ApiClient, ApiError
from services.table_renderer import render_table
from rich.console import Console

app = typer.Typer()

api_client = ApiClient(API_BASE_URL)

PAGE_SIZE = 10
console = Console()

def print_pagination_info(page: int, total_count: int):
    """Print pagination info for the current result set."""
    total_pages = (total_count // PAGE_SIZE) + (1 if total_count % PAGE_SIZE > 0 else 0)
    typer.echo(f"Page {page} of {total_pages}. Total registers: {total_count}")

@app.command()
def list_planets(
    page: int = typer.Option(1, "--page", "-p", help="Number of pages."),
    sort_by: str = typer.Option(None, "--sort-by", "-sb", help="Order by: name, diameter, climate, etc."),
    search: str = typer.Option(None, "--search", "-s", help="Search by name or other fields."),
):
    """List Star Wars planets with pagination, search, and sorting."""
    with console.status("[bold green]Loading planets..."):
        try:
            data = api_client.get_resource("planets", page=page, sort_by=sort_by, search=search)
        except ApiError as e:
            typer.secho(f"API Error: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        except Exception as e:
            typer.secho(f"Unexpected error: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
    items = data.get("results", [])
    render_table(
        title="🪐 Star Wars planets 🪐",
        columns=["name", "diameter", "climate", "terrain"],
        items=items
    )
    print_pagination_info(page, data.get('count', 0))

@app.command()
def list_people(
    page: int = typer.Option(1, "--page", "-p", help="Page number."),
    sort_by: str = typer.Option(None, "--sort-by", "-sb", help="Order by: name, height, mass, etc."),
    search: str = typer.Option(None, "--search", "-s", help="Search by name or other fields."),
):
    """List Star Wars people with pagination, search, and sorting."""
    with console.status("[bold green]Loading people..."):
        try:
            data = api_client.get_resource("people", page=page, sort_by=sort_by, search=search)
        except ApiError as e:
            typer.secho(f"API Error: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
        except Exception as e:
            typer.secho(f"Unexpected error: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)
    items = data.get("results", [])
    render_table(
        title="🧑‍🚀 Star Wars people 🧑‍🚀",
        columns=["name", "height", "mass", "gender", "birth_year"],
        items=items
    )
    print_pagination_info(page, data.get('count', 0))

if __name__ == "__main__":
    app()