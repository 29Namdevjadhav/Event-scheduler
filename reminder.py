import time
from datetime import datetime, timedelta
from utils import load_events

DATA_FILE = "events.json"

def check_reminders():
    while True:
        now = datetime.now()
        upcoming = now + timedelta(hours=1)
        events = load_events(DATA_FILE)
        for event in events:
            start_time = datetime.fromisoformat(event["start_time"])
            if now <= start_time <= upcoming:
                print(f"Reminder: {event['title']} at {event['start_time']}")
        time.sleep(60)

check_reminders()
