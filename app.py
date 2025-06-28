from flask import Flask, request, jsonify
import uuid
import json
import os
import threading
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
DATA_FILE = "events.json"
EMAIL_ENABLED = False  # Set to True if email is configured
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# ---------- Utility Functions ----------

def load_events():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_events(events):
    with open(DATA_FILE, "w") as file:
        json.dump(events, file, indent=4)


def send_email_notification(subject, message, to_email):
    if not EMAIL_ENABLED:
        print("[Notification] Email disabled.")
        return
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

        print(f"Email sent to {to_email}")
    except Exception as e:
        print("Failed to send email:", e)


def check_reminders():
    while True:
        events = load_events()
        now = datetime.now()
        upcoming = []
        for event in events:
            start = datetime.fromisoformat(event["start_time"])
            if 0 <= (start - now).total_seconds() <= 3600:
                upcoming.append(event)
                print(f"[Reminder] {event['title']} at {event['start_time']}")

                if EMAIL_ENABLED and event.get("email"):
                    send_email_notification(
                        subject=f"Reminder: {event['title']}",
                        message=f"{event['description']} at {event['start_time']}",
                        to_email=event["email"]
                    )

            # Recurring events
            recurrence = event.get("recurrence")
            if recurrence:
                next_time = start
                while next_time < now:
                    if recurrence == "daily":
                        next_time += timedelta(days=1)
                    elif recurrence == "weekly":
                        next_time += timedelta(weeks=1)
                    elif recurrence == "monthly":
                        next_time += timedelta(days=30)
                    event["start_time"] = next_time.isoformat()
                    event["end_time"] = (next_time + (datetime.fromisoformat(event["end_time"]) - start)).isoformat()

        if upcoming:
            save_events(events)
        threading.Event().wait(60)


threading.Thread(target=check_reminders, daemon=True).start()

# ---------- API Routes ----------

@app.route("/")
def home():
    return "Welcome to the Event Scheduler API!"


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    required = ["title", "description", "start_time", "end_time"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    event = {
        "id": str(uuid.uuid4()),
        "title": data["title"],
        "description": data["description"],
        "start_time": data["start_time"],
        "end_time": data["end_time"],
        "recurrence": data.get("recurrence"),  # Optional: daily, weekly, monthly
        "email": data.get("email")  # Optional: for notification
    }

    events = load_events()
    events.append(event)
    save_events(events)
    return jsonify({"message": "Event created", "event": event}), 201


@app.route("/events", methods=["GET"])
def list_events():
    events = sorted(load_events(), key=lambda x: x["start_time"])
    return jsonify(events)


@app.route("/events/<event_id>", methods=["PUT"])
def update_event(event_id):
    data = request.get_json()
    events = load_events()
    for event in events:
        if event["id"] == event_id:
            event.update({
                "title": data.get("title", event["title"]),
                "description": data.get("description", event["description"]),
                "start_time": data.get("start_time", event["start_time"]),
                "end_time": data.get("end_time", event["end_time"]),
                "recurrence": data.get("recurrence", event.get("recurrence")),
                "email": data.get("email", event.get("email")),
            })
            save_events(events)
            return jsonify({"message": "Event updated", "event": event})
    return jsonify({"error": "Event not found"}), 404


@app.route("/events/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    events = load_events()
    new_events = [e for e in events if e["id"] != event_id]
    if len(new_events) == len(events):
        return jsonify({"error": "Event not found"}), 404
    save_events(new_events)
    return jsonify({"message": "Event deleted"})


@app.route("/search", methods=["GET"])
def search_events():
    query = request.args.get("q", "").lower()
    events = load_events()
    results = [
        e for e in events
        if query in e["title"].lower() or query in e["description"].lower()
    ]
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
