# 🗓️ Event Scheduler System

This is a simple **Flask-based REST API** application to manage your events. It allows users to **Create, Read, Update, and Delete (CRUD)** events using RESTful endpoints.

---

## 📋 Features

- ✅ Create Event (POST)
- ✅ List All Events (GET)
- ✅ Update Event by ID (PUT)
- ✅ Delete Event by ID (DELETE)
- ✅ JSON file persistence (`events.json`)
- ✅ Reminders (due within the next hour)
- ✅ Unit Tests using Pytest

---

## 🚀 Technologies Used

- Python 3.x
- Flask
- REST API
- Postman
- JSON file storage
- Pytest

---

## 📦 Setup Instructions

### 🔧 Install Dependencies

First, create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # Or use venv\Scripts\activate on Windows

Install required packages:
pip install -r requirements.txt

Run the App
python app.py


how to use postman :

Step 1: Open Postman
Download and open Postman

✅ Step 2: Import the Collection
Click on Import (top-left).

Choose File, then upload:

EventScheduler.postman_collection.json from this repo

Click Import

✅ Step 3: Test Each API
You will see 4 requests inside the collection:

Create Event (POST)

Get All Events (GET)

Update Event (PUT)

Delete Event (DELETE)
```
