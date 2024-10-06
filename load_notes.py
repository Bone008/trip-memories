import datetime as dt
import pathlib
import re
import functools


_NOTES_DATA_FILE = pathlib.Path('data_notes.txt')

def get_notes_for_date(search_date: dt.date) -> str|None:
  """Returns the formatted note of a given date, or None if none were recorded."""
  search_key = search_date.isoformat()
  day_lines = get_notes_dict().get(search_key, None)
  if not day_lines:
    return None
  return "\n".join(f"- {line}" for line in day_lines)

@functools.cache
def get_notes_dict() -> dict[str, list[str]]:
  raw_text = _NOTES_DATA_FILE.read_text(encoding='utf-8')
  notes_dict = _parse_raw_notes(raw_text)
  print(f"Loaded {len(notes_dict)} notes entries.")
  return notes_dict

def _parse_raw_notes(raw_text: str) -> dict[str, list[str]]:
  data_dict = {}
  current_month_year = None
  current_day = None
  current_lines = []

  lines = raw_text.split("\n")
  for line in lines:
    line = line.strip()
    if not line:
      continue

    month_year_match = re.match(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})", line)
    if month_year_match:
      current_month_year = month_year_match.group(0)
      continue

    day_match = re.match(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\d+):", line)
    if day_match:
      if not current_month_year:
        raise ValueError("Day found before month/year")
      
      day_of_week = day_match.group(1)
      day_number = day_match.group(2)
      try:
        date_str = f"{current_month_year} {day_of_week} {day_number}"
        current_day = dt.datetime.strptime(date_str, '%b %Y %a %d')
      except ValueError:
        raise ValueError(f"Could not parse date: {date_str}")
        current_day = None
      current_lines = None
      continue
    
    if current_day:
      if current_lines is None:
        current_lines = []
        data_dict[current_day.date().isoformat()] = current_lines
      current_lines.append(line)
  return data_dict
