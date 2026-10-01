import argparse
import json
import random
import string
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse




DATA_FILE = Path(__file__).parent / "urls.json"
CODE_LENGTH = 6
ALLOWED_CHARACTERS = string.ascii_letters + string.digits



def load_data():
    """Load URL data from urls.json."""

    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("Error: Database contains invalid data.")
            return {}

        return data

    except json.JSONDecodeError:
        print("Error: urls.json is corrupted.")
        return {}

    except OSError as error:
        print(f"Error reading database: {error}")
        return {}


def save_data(data):
    """Save URL data to urls.json."""

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(f"Error saving database: {error}")
        sys.exit(1)




def is_valid_url(url):
    """Check whether a URL is a valid HTTP/HTTPS URL."""

    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
            and "." in parsed.netloc
        )

    except ValueError:
        return False




def generate_code(data):
    """Generate a unique random short code."""

    while True:
        code = "".join(
            random.choices(
                ALLOWED_CHARACTERS,
                k=CODE_LENGTH
            )
        )

        if code not in data:
            return code


def is_valid_alias(alias):
    """Check whether a custom alias is valid."""

    if not alias:
        return False

    allowed = string.ascii_letters + string.digits + "_-"

    return all(character in allowed for character in alias)


# ============================================================


def shorten_url(url, alias=None):
    """Shorten a URL and save it to the database."""

    if not is_valid_url(url):
        print("\nError: Invalid URL.")
        print("Please enter a URL beginning with http:// or https://")
        return

    data = load_data()

    for code, details in data.items():
        if details.get("url") == url:

            if alias is None:
                print("\nThis URL has already been shortened.")
                print(f"Short code: {code}")
                print(f"Short URL:  {code}")
                return

    
    if alias:

        if not is_valid_alias(alias):
            print(
                "\nError: Invalid alias."
                "\nUse only letters, numbers, '-' or '_'."
            )
            return

        if alias in data:
            print(f"\nError: The alias '{alias}' is already in use.")
            return

        code = alias

    else:
        code = generate_code(data)

    data[code] = {
        "url": url,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "clicks": 0
    }

    save_data(data)

    print("\nURL shortened successfully!")
    print(f"Original URL: {url}")
    print(f"Short code:   {code}")
    print(f"Short URL:    {code}")


# ============================================================

def resolve_url(code, open_browser=False):
    """Resolve a short code to the original URL."""

    data = load_data()

    if code not in data:
        print(f"\nError: Short code '{code}' was not found.")
        return

    details = data[code]
    url = details["url"]

    # Increase click count.
    details["clicks"] = details.get("clicks", 0) + 1

    save_data(data)

    print(f"\nOriginal URL: {url}")
    print(f"Resolution count: {details['clicks']}")

    if open_browser:
        try:
            opened = webbrowser.open(url)

            if opened:
                print("Opening URL in your default browser...")
            else:
                print("Could not open the browser automatically.")

        except Exception as error:
            print(f"Could not open browser: {error}")




def list_urls():
    """Display all stored URL mappings."""

    data = load_data()

    if not data:
        print("\nNo shortened URLs found.")
        return

    print("\n" + "=" * 80)
    print("                        STORED URLS")
    print("=" * 80)

    for number, (code, details) in enumerate(data.items(), start=1):

        print(f"\n[{number}]")
        print(f"Short code : {code}")
        print(f"Original   : {details.get('url', 'Unknown')}")
        print(f"Created    : {details.get('created_at', 'Unknown')}")
        print(f"Clicks     : {details.get('clicks', 0)}")

    print("\n" + "=" * 80)
    print(f"Total URLs: {len(data)}")
    print("=" * 80)




def delete_url(code):
    """Delete a shortened URL."""

    data = load_data()

    if code not in data:
        print(f"\nError: Short code '{code}' was not found.")
        return

    url = data[code]["url"]

    del data[code]
    save_data(data)

    print("\nURL deleted successfully.")
    print(f"Short code: {code}")
    print(f"Original URL: {url}")




def interactive_mode():
    """Run the interactive menu."""

    while True:

        print("\n" + "=" * 45)
        print("           MINI URL SHORTENER")
        print("=" * 45)
        print("1. Shorten URL")
        print("2. Resolve URL")
        print("3. List URLs")
        print("4. Delete URL")
        print("5. Exit")
        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            url = input("Enter URL: ").strip()

            alias = input(
                "Enter custom alias (press Enter to skip): "
            ).strip()

            if alias:
                shorten_url(url, alias)
            else:
                shorten_url(url)

        elif choice == "2":

            code = input("Enter short code: ").strip()

            open_choice = input(
                "Open in browser? (y/n): "
            ).strip().lower()

            resolve_url(
                code,
                open_browser=(open_choice == "y")
            )

        elif choice == "3":
            list_urls()

        elif choice == "4":

            code = input(
                "Enter short code to delete: "
            ).strip()

            delete_url(code)

        elif choice == "5":

            print("\nGoodbye!")
            break

        else:
            print(
                "\nInvalid choice. "
                "Please enter a number from 1 to 5."
            )




def create_parser():
    """Create command-line argument parser."""

    parser = argparse.ArgumentParser(
        description="A simple command-line URL shortener."
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

  

    shorten_parser = subparsers.add_parser(
        "shorten",
        help="Shorten a URL"
    )

    shorten_parser.add_argument(
        "url",
        help="The long URL to shorten"
    )

    shorten_parser.add_argument(
        "--alias",
        help="Optional custom short code"
    )

    
    resolve_parser = subparsers.add_parser(
        "resolve",
        help="Resolve a short code"
    )

    resolve_parser.add_argument(
        "code",
        help="The short code"
    )

    resolve_parser.add_argument(
        "--open",
        action="store_true",
        help="Open the original URL in the browser"
    )



    subparsers.add_parser(
        "list",
        help="List all shortened URLs"
    )

  

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a shortened URL"
    )

    delete_parser.add_argument(
        "code",
        help="The short code to delete"
    )



    subparsers.add_parser(
        "interactive",
        help="Start interactive mode"
    )

    return parser




def main():

    parser = create_parser()

    
    if len(sys.argv) == 1:
        interactive_mode()
        return

    args = parser.parse_args()

    if args.command == "shorten":

        shorten_url(
            args.url,
            args.alias
        )

    elif args.command == "resolve":

        resolve_url(
            args.code,
            args.open
        )

    elif args.command == "list":

        list_urls()

    elif args.command == "delete":

        delete_url(
            args.code
        )

    elif args.command == "interactive":

        interactive_mode()

    else:

        parser.print_help()


if __name__ == "__main__":
    main()

