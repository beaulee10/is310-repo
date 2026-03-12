import json
import os
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()
FILENAME = "top_songs_data.json"

def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return []

def main():
    songs = load_data()
    console.print("[bold magenta]Music Database Loaded![/bold magenta]\n")
    
    if songs:
        table = Table(title="Current Collection")
        table.add_column("Year", style="cyan")
        table.add_column("Artist", style="green")
        table.add_column("Song", style="bold white")
        for s in songs:
            table.add_row(s.get("Year", "N/A"), s.get("Artist", "N/A"), s.get("Song", "N/A"))
        console.print(table)

    new_entries = []
    while True:
        console.print("\n[bold cyan]Add a new hit:[/bold cyan]")
        year = Prompt.ask("Enter the release year")
        artist = Prompt.ask("Enter the artist")
        song_title = Prompt.ask("Enter the song title")

        console.print(f"\n[yellow]Confirming:[/yellow] [bold]{song_title}[/bold] by [bold]{artist}[/bold] ({year})")
        if Confirm.ask("Is this correct?"):
            new_entries.append({"Year": year, "Artist": artist, "Song": song_title})
            console.print("[green]Added to queue![/green]")
        
        if not Confirm.ask("Add another song?"):
            break

    if new_entries:
        all_songs = songs + new_entries
        with open(FILENAME, "w") as f:
            json.dump(all_songs, f, indent=4)
        console.print(f"\n[bold green]Success![/bold green] Database updated.")
    else:
        console.print("\n[yellow]No changes made.[/yellow]")

if __name__ == "__main__":
    main()
