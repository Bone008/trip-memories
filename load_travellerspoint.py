import dataclasses
import functools
import json
from typing import Any
import datetime as dt
import pathlib

# response of API call:
# https://www.travellerspoint.com/ajax/MappingService.cfc?method=_getUserMapJSON&userid=XXXX&tripid=YYYY
_LOCATION_DATA_FILE = pathlib.Path("data_travellerspoint.json")


def get_location_for_date(search_date: dt.date) -> str | None:
    """Returns the location at a given date, or None if none was recorded."""
    search_key = search_date.isoformat()
    return get_locations_dict().get(search_key, None)


@functools.cache
def get_locations_dict() -> dict[str, str]:
    data_dict = json.loads(_LOCATION_DATA_FILE.read_text(encoding="utf-8"))
    location_entries = _parse_travellerspoint_data(data_dict)
    locations_dict = _locations_to_dict(location_entries)
    print(
        f"Loaded {len(location_entries)} location entries "
        f"for {len(locations_dict)} days "
        f"({min(locations_dict.keys())} - {max(locations_dict.keys())})."
    )
    return locations_dict


@dataclasses.dataclass
class _LocationEntry:
    arrival_date: dt.date
    departure_date: dt.date
    to_location: str


def _parse_travellerspoint_data(data_dict: dict[str, Any]) -> list[_LocationEntry]:
    location_entries = []
    for entry in data_dict["data"]["trips"][0]["ss"]:
        arrival_date = dt.datetime.strptime(entry["ad"], "%Y-%m-%d").date()
        # NOTE: I patched this manually, only worked when i replaced 0000-00-00 with
        # the real departure date.
        if entry["dd"] == "0000-00-00":
            departure_date = dt.date(1, 1, 1)
        else:
            departure_date = dt.datetime.strptime(entry["dd"], "%Y-%m-%d").date()
        to_location = entry["l"]
        location_entries.append(
            _LocationEntry(arrival_date, departure_date, to_location)
        )
    return location_entries


def _locations_to_dict(location_entries: list[_LocationEntry]) -> dict[str, str]:
    """Converts a list of LocationEntry objects to a dictionary keyed by dates."""
    locations_dict = {}
    for entry in location_entries:
        duration_days = (entry.departure_date - entry.arrival_date).days
        duration_days = max(1, duration_days)  # Ensure at least one day
        for i in range(duration_days):
            date = entry.arrival_date + dt.timedelta(days=i)
            key = date.isoformat()
            if key in locations_dict:
                locations_dict[key] += f" + {entry.to_location}"
            else:
                locations_dict[key] = entry.to_location
    return locations_dict


if __name__ == "__main__":
    for date, location in get_locations_dict.items():
        print(f"{date}: {location}")
