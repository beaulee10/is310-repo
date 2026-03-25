import cloudscraper
from bs4 import BeautifulSoup
import csv
from rich.console import Console
from rich.table import Table

console = Console()
# We add a browser-like "User-Agent" to look more like a human
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})

def scrape_wiki():
    # Switching to Star Wars Bounty Hunters - usually very stable for scraping
    url = "https://starwars.fandom.com/wiki/Category:Bounty_hunters"
    console.print(f"[bold yellow]Attempting to scrape:[/bold yellow] {url}")
    
    try:
        response = scraper.get(url, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # This targets the main list container for almost ALL Fandom wikis
        items = []
        
        # Strategy A: Standard Fandom Category Class
        items = soup.find_all('a', class_='category-page__member-link')
        
        # Strategy B: If A fails, look for links inside the member-views div
        if not items:
            container = soup.find('div', class_='category-page__members')
            if container:
                items = container.find_all('a', href=True)

        results = []
        for item in items:
            name = item.get_text().strip()
            link = item.get('href')
            
            # Filter out images, "next page" links, and duplicates
            if name and "/wiki/" in link and "Category:" not in link and ":" not in name:
                full_link = "https://starwars.fandom.com" + link
                if {"name": name, "link": full_link} not in results:
                    results.append({"name": name, "link": full_link})
                    console.print(f"[green]✔ Found:[/green] {name}")
            
            if len(results) >= 20: # Stop at 20
                break

        if not results:
            console.print("[red]❌ Still no data. Let's check the status code:[/red]", response.status_code)
            # Print a bit of the HTML to see what's happening
            return

        # Save to CSV
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "link"])
            writer.writeheader()
            writer.writerows(results)
            
        table = Table(title="Scraped Wiki Data")
        table.add_column("Name", style="cyan")
        table.add_column("Link", style="magenta")
        for r in results:
            table.add_row(r['name'], r['link'])
        console.print(table)
        console.print(f"\n[bold green]Success! Saved {len(results)} items to scraped_data.csv[/bold green]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    scrape_wiki()
