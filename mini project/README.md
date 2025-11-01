# Personal Expense Tracker

A web application for tracking personal expenses built with Flask and SQLite.

## Features
- Add, view, and delete expenses
- Categorize expenses by type
- View all expenses in a sortable table
- Responsive design that works on mobile and desktop
- Beautiful dashboard with monthly expense visualization (using Tkinter)

## Project Structure
```
├── app.py              # Main Flask application
├── dashboard.py        # Tkinter dashboard with expense visualization
├── db_config.py        # Database configuration
├── db_connect.py       # Database connection utilities
├── setup_db.py         # Database setup script
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css   # Custom styles
│   └── js/
│       └── script.js   # Client-side JavaScript
└── expenses.db         # SQLite database (created automatically)
```

## Setup Instructions

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and go to `http://localhost:5000`

4. To view the dashboard visualization:
   ```
   python dashboard.py
   ```

## API Endpoints

- `GET /` - Serve the main page
- `POST /api/expenses` - Add a new expense
- `GET /api/expenses` - Get all expenses
- `DELETE /api/expenses/<id>` - Delete an expense by ID

## Database Schema

The application uses a simple SQLite database with one table:

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    notes TEXT
);
```