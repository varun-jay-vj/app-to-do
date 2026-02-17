import streamlit as st
from datetime import datetime
import sqlite3
import os

# Page config
st.set_page_config(page_title="To-Do App", page_icon="✅", layout="centered")

# Database setup
DB_PATH = "todo_app.db"

def init_db():
    """Initialize database and create table if not exists"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'Medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    # Check if database is empty and initialize with sample tasks
    c.execute('SELECT COUNT(*) FROM tasks')
    if c.fetchone()[0] == 0:
        sample_tasks = [
            ("Set up Streamlit environment and install dependencies", "High"),
            ("Design app layout and user interface components", "High"),
            ("Implement core functionality and business logic", "Medium"),
            ("Add data persistence (database or session state)", "Medium"),
            ("Create input forms and validation", "Medium"),
            ("Add filtering and sorting capabilities", "Low"),
            ("Test app functionality and edge cases", "High"),
            ("Deploy app to Streamlit Cloud or server", "Low")
        ]
        c.executemany('INSERT INTO tasks (text, priority) VALUES (?, ?)', sample_tasks)
        conn.commit()
    
    conn.close()

def get_all_tasks():
    """Retrieve all tasks from database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, text, completed, priority, created_at FROM tasks ORDER BY id DESC')
    tasks = []
    for row in c.fetchall():
        tasks.append({
            'id': row[0],
            'text': row[1],
            'completed': bool(row[2]),
            'priority': row[3],
            'created_at': row[4]
        })
    conn.close()
    return tasks

def add_task(task_text, priority="Medium"):
    """Add new task to database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO tasks (text, priority) VALUES (?, ?)', (task_text, priority))
    conn.commit()
    conn.close()

def toggle_task(task_id):
    """Toggle task completion status"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = NOT completed WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete task from database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def clear_completed_tasks():
    """Delete all completed tasks"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE completed = 1')
    conn.commit()
    conn.close()

def get_pending_count():
    """Get count of pending tasks"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM tasks WHERE completed = 0')
    count = c.fetchone()[0]
    conn.close()
    return count

# Initialize database
init_db()


# App header
st.title("✅ To-Do App")
st.markdown("---")

# Input section
col1, col2 = st.columns([3, 1])
with col1:
    new_task = st.text_input("Add a new task", placeholder="Enter task description...", label_visibility="collapsed")
with col2:
    priority = st.selectbox("Priority", ["High", "Medium", "Low"], label_visibility="collapsed")

if st.button("➕ Add Task", use_container_width=True):
    if new_task.strip():
        add_task(new_task.strip(), priority)
        st.rerun()
    else:
        st.warning("Please enter a task description")

# Get tasks from database
tasks = get_all_tasks()

# Stats
pending = get_pending_count()
total = len(tasks)
st.markdown(f"**Tasks:** {pending} pending | {total - pending} completed | {total} total")
st.markdown("---")

# Filter options
filter_option = st.radio("Filter", ["All", "Pending", "Completed"], horizontal=True)

# Display tasks
if tasks:
    filtered_tasks = tasks
    if filter_option == "Pending":
        filtered_tasks = [t for t in tasks if not t['completed']]
    elif filter_option == "Completed":
        filtered_tasks = [t for t in tasks if t['completed']]
    
    if not filtered_tasks:
        st.info(f"No {filter_option.lower()} tasks")
    else:
        for task in filtered_tasks:
            col1, col2, col3 = st.columns([0.5, 6, 1])
            
            with col1:
                checked = st.checkbox("", value=task['completed'], key=f"check_{task['id']}", 
                                     on_change=toggle_task, args=(task['id'],))
            
            with col2:
                # Priority badge color
                priority_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                priority_badge = priority_colors.get(task['priority'], "⚪")
                
                # Task text with strikethrough if completed
                task_style = "text-decoration: line-through; color: gray;" if task['completed'] else ""
                
                # Format timestamp
                created_time = datetime.strptime(task['created_at'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
                
                st.markdown(
                    f"<span style='{task_style}'>{priority_badge} {task['text']}</span><br>"
                    f"<small style='color: gray;'>Added: {created_time}</small>",
                    unsafe_allow_html=True
                )
            
            with col3:
                if st.button("🗑️", key=f"del_{task['id']}"):
                    delete_task(task['id'])
                    st.rerun()
            
            st.markdown("---")
else:
    st.info("No tasks yet. Add your first task above!")

# Clear completed tasks button
if any(t['completed'] for t in tasks):
    if st.button("🧹 Clear Completed Tasks"):
        clear_completed_tasks()
        st.rerun()