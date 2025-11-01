import unittest
import sys
import os
import json
from app import app

class ExpenseTrackerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        """Test that the index page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Simple Expense Tracker', response.data)

    def test_add_expense(self):
        """Test adding a new expense"""
        expense_data = {
            'date': '2023-06-15',
            'category': 'Food',
            'amount': 25.50,
            'notes': 'Lunch at restaurant'
        }
        
        response = self.app.post('/api/expenses',
                               data=json.dumps(expense_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertIn('message', data)

    def test_get_expenses(self):
        """Test retrieving all expenses"""
        response = self.app.get('/api/expenses')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_delete_expense(self):
        """Test deleting an expense"""
        # First add an expense
        expense_data = {
            'date': '2023-06-15',
            'category': 'Transport',
            'amount': 10.00,
            'notes': 'Bus fare'
        }
        
        response = self.app.post('/api/expenses',
                               data=json.dumps(expense_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        expense_id = data['id']
        
        # Then delete it
        response = self.app.delete(f'/api/expenses/{expense_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()