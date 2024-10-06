# Trip Memories Notification Sender

A simple tool that sends notes about a single day of a past trip as phone notifications
through the netfy.sh service.

Best to be run as a daily cronjob.

Requires at least Python 3.10.

## How to run

```
usage: send_memory.py [-h] [--date DATE] [--years-ago YEARS_AGO] [--send-topic SEND_TOPIC]

Send a memory of a specific day.

options:
  -h, --help            show this help message and exit
  --date DATE           The date to send the memory for (YYYY-MM-DD)
  --years-ago YEARS_AGO
                        The number of years ago to send the memory for
  --send-topic SEND_TOPIC
                        Set ntfy.sh topic to send to, otherwise print it.
```

Either `--date` or `--years-ago` must be provided.

## How to automate

Run `sudo crontab -e` to modify the crontab file and add this line:

```
0 11 * * * cd /path/to/your/script && /usr/bin/python3 send_memory.py --years-ago 1 --send-topic <topic>
```

Replace `0 11` with the daily time to run the script at (here: 11:00 am).

Replace `<topic>` with a random netfy topic that your phone is subscribed to.

## Local files

### data_notes.txt

Must contain the notes per day in a very specific format, example:

```
Sep 2024
Fri 13:
note line 1
note line 2
Thu 12:
note line 1

Aug 2024
Fri 30
note line 1
...
```

### data_travellerspoint.json

Must contain the response of the following TravellersPoint API call:

https://www.travellerspoint.com/ajax/MappingService.cfc?method=_getUserMapJSON&userid={xxx}&tripid={yyy}

Easiest to obtain using Developer Tools while logged in and opening a trip.
