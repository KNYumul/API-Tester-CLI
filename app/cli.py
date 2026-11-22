
from dbm import error
import json

import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.syntax import Syntax

from app.api_client import send_request
from app.response_handler import display_response


console = Console()

request_history = []


def display_banner():
    console.clear()

    banner = """
     █████╗ ██████╗ ██╗
    ██╔══██╗██╔══██╗██║
    ███████║██████╔╝██║
    ██╔══██╗██╔═══╝ ██║
    ██║  ██║██║     ██║
    ╚═╝  ╚═╝╚═╝     ╚═╝

       REST API TESTER CLI
    """

    console.print(
        Panel(
            banner,
            border_style="bright_blue",
            subtitle="Interactive API Testing Tool"
        )
    )


def display_menu():
    table = Table(
        title="MAIN MENU",
        border_style="cyan"
    )

    table.add_column("Option", style="bold yellow")
    table.add_column("Function", style="white")

    table.add_row("1", "Send GET Request")
    table.add_row("2", "Send POST Request")
    table.add_row("3", "Send PUT Request")
    table.add_row("4", "Send DELETE Request")
    table.add_row("5", "View Request History")
    table.add_row("6", "Run Automated Tests")
    table.add_row("7", "Exit")

    console.print(table)


def execute_request(method):
    console.print(
        Panel(
            f"[bold cyan]{method} REQUEST[/bold cyan]",
            border_style="cyan"
        )
    )

    url = Prompt.ask("Enter API endpoint")

    headers = {
        "Accept": "application/json"
    }

    body = None

    if method in ["POST", "PUT"]:
        console.print(
            "\n[yellow]Enter JSON request body.[/yellow]"
        )

        body_input = Prompt.ask(
            "JSON Body",
            default='{"title": "Test Post", "body": "API testing", "userId": 1}'
        )

        try:
            body = json.loads(body_input)

        except json.JSONDecodeError:
            console.print("[bold red]Invalid JSON format![/bold red]")
            return

    try:
        console.print("\n[yellow]Sending request...[/yellow]")

        response = send_request(
            method=method,
            url=url,
            headers=headers,
            body=body
        )

        request_history.append({
            "method": method,
            "url": url,
            "status": response.status_code
        })

        display_response(response)

    except requests.exceptions.Timeout:
        console.print(
            "[bold red]Request Timeout![/bold red]"
        )

    except requests.exceptions.ConnectionError:
        console.print(
            "[bold red]Connection Error! Check your internet connection.[/bold red]"
        )

    except requests.exceptions.InvalidURL:
        console.print(
            "[bold red]Invalid API URL![/bold red]"
        )

    except requests.exceptions.RequestException as error:
        console.print(
            f"[bold red]Request Failed:[/bold red] {error}"
        )


def display_history():
    if not request_history:
        console.print("[yellow]No request history available.[/yellow]")
        return

    table = Table(title="REQUEST HISTORY")

    table.add_column("Method", style="cyan")
    table.add_column("Endpoint", style="white")
    table.add_column("Status", style="green")

    for item in request_history:
        table.add_row(
            item["method"],
            item["url"],
            str(item["status"])
        )

    console.print(table)


def main_menu():
    while True:
        display_banner()
        display_menu()

        choice = Prompt.ask(
            "\n[bold cyan]Select an option[/bold cyan]",
            choices=["1", "2", "3", "4", "5", "6", "7"]
        )

        if choice == "1":
            execute_request("GET")

        elif choice == "2":
            execute_request("POST")

        elif choice == "3":
            execute_request("PUT")

        elif choice == "4":
            execute_request("DELETE")

        elif choice == "5":
            display_history()

        elif choice == "6":
            console.print("[yellow]Automated Tests coming in Phase 5.[/yellow]")

        elif choice == "7":
            console.print("[bold red]Exiting API Tester CLI...[/bold red]")
            break

        Prompt.ask("\nPress Enter to continue", default="")


if __name__ == "__main__":
    main_menu()
