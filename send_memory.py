import argparse
import datetime as dt
import requests

import load_notes
import load_travellerspoint

_NTFY_HOST = "https://ntfy.sh/"

PRIORITY_MAX = 5
PRIORITY_HIGH = 4
PRIORITY_NORMAL = 3


def send_notification(
    topic: str,
    title: str,
    message: str,
    priority: int = PRIORITY_NORMAL,
    icon: str | None = None,  # see: https://docs.ntfy.sh/emojis/
    **kwargs,
):
    """Sends a notification via netfy.sh."""
    # See: https://docs.ntfy.sh/publish/#publish-as-json
    response = requests.post(
        _NTFY_HOST,
        json={
            "topic": topic,
            "title": title,
            "message": message,
            "priority": priority,
            "tags": [icon] if icon else [],
            **kwargs,
        },
    )
    if response.status_code != 200:
        print(
            f"Error: Could not send notification! Status code was {response.status_code}."
            f"\n\nResponse was:\n{response.text}"
        )
        exit(1)


def create_title_for_date(search_date: dt.date) -> str:
    return f"Travel Memory - {search_date.strftime('%a, %d %b %Y')}"


def create_message_for_date(search_date: dt.date) -> str | None:
    note = load_notes.get_notes_for_date(search_date)
    location = load_travellerspoint.get_location_for_date(search_date)
    if not location and not note:
        return None

    message = ""
    if location:
        message += f"📌 {location}\n"
    if note:
        message += f"{note}"
    return message


def main():
    parser = argparse.ArgumentParser(description="Send a memory of a specific day.")
    parser.add_argument(
        "--date",
        type=str,
        help="The date to send the memory for (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--years-ago",
        type=int,
        help="The number of years ago to send the memory for",
    )
    parser.add_argument(
        "--send-topic",
        type=str,
        help="Set ntfy.sh topic to send to, otherwise print it.",
    )
    args = parser.parse_args()

    if args.date:
        search_date = dt.datetime.strptime(args.date, "%Y-%m-%d").date()
    elif args.years_ago:
        today = dt.date.today()
        search_date = today.replace(year=today.year - args.years_ago)
    else:
        print("Please provide either --date or --years-ago!")
        exit(1)

    title = create_title_for_date(search_date)
    message = create_message_for_date(search_date)
    timeline_url = f"https://www.google.com/maps/timeline?pb=!1m2!1m1!1s{search_date.isoformat()}"
    if not message:
        print(f"No data for date {search_date.isoformat()}!")
        exit(0)

    if args.send_topic:
        send_notification(
            args.send_topic,
            title,
            message,
            icon="earth_asia",
            click=timeline_url,
        )
        print("Sent!")
    else:
        print("==== Memory ====")
        print("#", title)
        print(message)
        print("\nTimeline:", timeline_url)


if __name__ == "__main__":
    main()
