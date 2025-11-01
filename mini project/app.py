from flask import Flask, render_template, request, jsonify
from db_connect import get_db_connection, create_tables

# Create Flask app
app = Flask(__name__)

# Initialize database when app starts
create_tables()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to add an expense
@app.route('/api/expenses', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['date', 'category', 'amount']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Connect to database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert expense
        cur.execute(
            "INSERT INTO expenses (date, category, amount, notes) VALUES (?, ?, ?, ?)",
            (data['date'], data['category'], data['amount'], data.get('notes', ''))
        )
        
        conn.commit()
        expense_id = cur.lastrowid
        cur.close()
        conn.close()
        
        return jsonify({'id': expense_id, 'message': 'Expense added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to get all expenses
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    try:
        # Connect to database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get all expenses
        cur.execute("SELECT id, date, category, amount, notes FROM expenses ORDER BY date DESC")
        rows = cur.fetchall()
        
        # Convert to list of dictionaries
        expenses = []
        for row in rows:
            expenses.append({
                'id': row[0],
                'date': row[1],
                'category': row[2],
                'amount': row[3],
                'notes': row[4] if row[4] else ''
            })
        
        cur.close()
        conn.close()
        
        return jsonify(expenses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API endpoint to delete an expense
@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        # Connect to database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Delete expense
        cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        rows_affected = cur.rowcount
        
        cur.close()
        conn.close()
        
        if rows_affected > 0:
            return jsonify({'message': 'Expense deleted successfully'}), 200
        else:
            return jsonify({'error': 'Expense not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)