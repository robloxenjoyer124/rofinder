import argparse
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from api import RobloxAPI
from ui import RoFinderUI
from exporter import RoFinderExporter

console = Console()
api = RobloxAPI()
ui = RoFinderUI()
exporter = RoFinderExporter()

def main():
    parser = argparse.ArgumentParser(description="RoFinder v2.2 - Ultimate Roblox Intelligence")
    parser.add_argument("user", help="Username or User ID")
    parser.add_argument("--detailed", action="store_true", help="Fetch deep data (Badges, Groups, Assets)")
    parser.add_argument("--save", help="Save output to file (e.g., report.json or report.txt)")
    parser.add_argument("--format", choices=['json', 'txt'], default='txt', help="Format for saving file")
    
    args = parser.parse_args()
    
    # Clean UI start
    ui.print_banner()

    user_input = args.user
    user_id = None

    # 1. Resolve User
    with Progress(SpinnerColumn(), TextColumn("[bold cyan]Targeting user..."), transient=True) as progress:
        progress.add_task("", total=None)
        if user_input.isdigit():
            user_id = int(user_input)
        else:
            user_id = api.get_id_by_username(user_input)

    if not user_id:
        console.print(f"[bold red]❌ Error:[/bold red] User '{user_input}' not found.")
        sys.exit(1)

    # 2. Fetch Intelligence
    with Progress(SpinnerColumn(), TextColumn("[bold magenta]Extracting data..."), transient=True) as progress:
        task = progress.add_task("", total=None)
        
        # Core
        user_info = api.get_user_info(user_id)
        if not user_info:
            console.print("[bold red]❌ Error:[/bold red] API Connection failed.")
            sys.exit(1)
            
        friends = api.get_friends_count(user_id)
        followers = api.get_followers_count(user_id)
        following = api.get_following_count(user_id)
        presence = api.get_presence(user_id)
        premium = api.get_premium_status(user_id)
        avatar = api.get_avatar_thumbnail(user_id)
        
        # Extended
        badges = []
        groups = []
        assets = []
        favorites = []
        
        if args.detailed or args.save:
            progress.update(task, description="[bold magenta]Fetching deep history & assets...[/bold magenta]")
            badges = api.get_badges(user_id)
            groups = api.get_groups(user_id)
            assets = api.get_currently_wearing(user_id)
            favorites = api.get_favorites(user_id)

    # 3. Construct Data Object
    full_data = {
        "profile": user_info,
        "stats": {"friends": friends, "followers": followers, "following": following},
        "status": {"presence": presence, "premium": premium},
        "avatar_url": avatar,
        "badges": badges,
        "groups": groups,
        "assets": assets,
        "favorites": favorites
    }

    # 4. Display UI
    console.print(ui.create_user_panel(user_info, friends, followers, following, avatar, presence, premium))
    
    if args.detailed:
        console.print("\n")
        if assets: console.print(ui.create_wearing_table(assets))
        if favorites: console.print(ui.create_favorites_table(favorites))
        if badges: console.print(ui.create_badges_table(badges))
        if groups: console.print(ui.create_groups_table(groups))

    # 5. Handle Export
    if args.save:
        filename = args.save
        saved_path = ""
        
        with console.status("[bold yellow]Saving report..."):
            if args.format == 'json' or filename.endswith('.json'):
                saved_path = exporter.export_json(full_data, filename)
            else:
                saved_path = exporter.export_txt(full_data, filename)
        
        console.print(f"\n[bold green]✅ Report saved successfully:[/bold green] {saved_path}")

    console.print("\n[dim]RoFinder v2.2.0[/dim]", justify="center")

if __name__ == "__main__":
    main()