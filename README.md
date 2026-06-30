# Personal Assistant

A command-line personal assistant built in Python for managing tasks, schedules, and projects, with real-time weather and news integrations via external APIs.

## Features

**Task Management**
- Add, edit, view, and delete tasks
- Set due dates and receive deadline reminders
- Search and filter by keyword

**Project Management**
- Add, view, and remove projects
- Filter by month
- Search functionality

**Schedule Management**
- Add, view, and delete scheduled events
- Search by specific date
- Deadline reminders for upcoming events

**Live Data**
- Current weather for any city (via weather API)
- Latest news headlines by country and category
- Direct links to full articles

**Storage**
- All data persisted locally in JSON files (`tasks.json`, `projects.json`, `schedules.json`)

## Project Structure
├── support.py       # Main application logic
├── tasks.json       # Task data
├── projects.json    # Project data
└── schedules.json   # Schedule data

## Concepts Demonstrated

- Object-oriented programming (dedicated classes for Schedule and Project)
- REST API consumption with `requests`
- JSON file I/O for persistent storage
- Date handling with `datetime`
- Input validation with `re`

## How to Run

```bash
python support.py
```

Requires a `requests` library (`pip install requests`) and valid API keys for weather and news services.
