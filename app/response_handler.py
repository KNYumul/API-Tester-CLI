
import json

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

console = Console()


def get_status_message(status_code):
    if 200 <= status_code < 300:
        return "SUCCESS"

    elif 300 <= status_code < 400:
        return "REDIRECTION"

    elif 400 <= status_code < 500:
        return "CLIENT ERROR"

    elif 500 <= status_code < 600:
        return "SERVER ERROR"

    return "UNKNOWN STATUS"


def display_response(response):
    status = response.status_code
    status_message = get_status_message(status)

    status_color = (
        "green" if 200 <= status < 300
        else "yellow" if 300 <= status < 400
        else "red"
    )

    console.print(
        Panel(
            f"[bold {status_color}]{status} - {status_message}[/bold {status_color}]",
            title="HTTP STATUS",
            border_style=status_color
        )
    )

    # Response time
    response_time = response.elapsed.total_seconds() * 1000

    console.print(
        f"[bold cyan]Response Time:[/bold cyan] {response_time:.2f} ms"
    )

    # Response headers
    header_table = Table(title="RESPONSE HEADERS")

    header_table.add_column("Header", style="cyan")
    header_table.add_column("Value", style="white")

    for key, value in response.headers.items():
        header_table.add_row(key, value)

    console.print(header_table)

    # Response body
    console.print("\n[bold cyan]RESPONSE BODY[/bold cyan]")

    try:
        json_data = response.json()

        formatted_json = json.dumps(
            json_data,
            indent=4,
            ensure_ascii=False
        )

        syntax = Syntax(
            formatted_json,
            "json",
            theme="monokai",
            line_numbers=True
        )

        console.print(
            Panel(
                syntax,
                border_style="green"
            )
        )

    except (ValueError, json.JSONDecodeError):
        console.print(
            Panel(
                response.text or "(Empty response body)",
                border_style="yellow"
            )
        )

    # HTTP error details
    if not response.ok:
        console.print(
            f"\n[bold red]HTTP Error: {status_message}[/bold red]"
        )

        console.print(
            "[red]The server returned an unsuccessful HTTP status.[/red]"
        )
