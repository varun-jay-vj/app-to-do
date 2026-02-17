# ✅ Streamlit To-Do App

A simple, elegant task management application built with Streamlit and SQLite3.

<img width="1141" height="888" alt="image" src="https://github.com/user-attachments/assets/a4d70a94-7bc4-4fa6-aed3-1bd9cbe223a4" />


## Features

- **Persistent Storage** – Tasks are saved to a SQLite database and persist across sessions
- **Priority Levels** – Organize tasks by High, Medium, or Low priority
- **Task Filtering** – View All, Pending, or Completed tasks
- **Task Management** – Add, complete, and delete tasks with a clean interface
- **Pre-loaded Examples** – Initialized with sample tasks for building a Streamlit app
- **Real-time Stats** – Track pending, completed, and total task counts

## Installation

1. **Clone or download** this repository

2. **Install dependencies**:
```bash
pip install streamlit
```

SQLite3 is included with Python by default.

## Usage

Run the application:
```bash
streamlit run todo_app.py
```

The app will open in your browser at `http://localhost:8501`

## How It Works

### Database Structure
- Tasks are stored in `todo_app.db` (created automatically on first run)
- Schema includes: `id`, `text`, `completed`, `priority`, `created_at`

### Initial Sample Tasks
On first run, the app initializes with 8 sample tasks covering the Streamlit development workflow:
1. Set up Streamlit environment and install dependencies
2. Design app layout and user interface components
3. Implement core functionality and business logic
4. Add data persistence (database or session state)
5. Create input forms and validation
6. Add filtering and sorting capabilities
7. Test app functionality and edge cases
8. Deploy app to Streamlit Cloud or server

### User Interface
- **Add Task** – Enter task description and select priority level
- **Complete Task** – Click checkbox to mark as done (strikethrough styling applied)
- **Delete Task** – Click 🗑️ button to remove individual tasks
- **Filter View** – Toggle between All/Pending/Completed tasks
- **Clear Completed** – Bulk delete all completed tasks

## File Structure

```
.
├── todo_app.py       # Main application file
├── todo_app.db       # SQLite database (created on first run)
└── README.md         # This file
```

## Technology Stack

- **Streamlit** – Web framework for the UI
- **SQLite3** – Lightweight database for task persistence
- **Python 3.7+** – Core programming language

## Customization

You can modify the sample tasks by editing the `sample_tasks` list in the `init_db()` function:

```python
sample_tasks = [
    ("Your custom task", "Priority"),
    # Add more tasks here
]
```

## License

Free to use and modify as needed.

## Contributing


Feel free to submit issues or pull requests for improvements.
