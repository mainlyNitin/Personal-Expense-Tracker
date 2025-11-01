// Simple Expense Tracker JavaScript

// DOM Elements
const expenseForm = document.getElementById('expense-form');
const refreshBtn = document.getElementById('refresh-btn');
const expensesBody = document.getElementById('expenses-body');
const messageDiv = document.getElementById('message');

// Chart instance
let expenseChart = null;

// Set today's date as default
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
    
    // Load initial data
    loadExpenses();
    loadSummary();
});

// Event Listeners
expenseForm.addEventListener('submit', addExpense);
refreshBtn.addEventListener('click', refreshData);

// Refresh all data
function refreshData() {
    loadExpenses();
    loadSummary();
    showMessage('Data refreshed successfully!', 'success');
}

// Load all expenses
function loadExpenses() {
    fetch('/api/expenses')
        .then(response => response.json())
        .then(expenses => {
            expensesBody.innerHTML = '';
            
            if (expenses.length === 0) {
                expensesBody.innerHTML = '<tr><td colspan="5">No expenses found</td></tr>';
                updateChart([]);
                return;
            }
            
            // Sort expenses by date (newest first)
            expenses.sort((a, b) => new Date(b.date) - new Date(a.date));
            
            expenses.forEach(expense => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${formatDate(expense.date)}</td>
                    <td><span class="category-badge category-${expense.category.toLowerCase()}">${expense.category}</span></td>
                    <td>₹${parseFloat(expense.amount).toFixed(2)}</td>
                    <td>${expense.notes || '-'}</td>
                    <td>
                        <button class="delete-btn" onclick="deleteExpense(${expense.id})">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </td>
                `;
                expensesBody.appendChild(row);
            });
            
            // Update chart with expense data
            updateChart(expenses);
        })
        .catch(error => {
            showMessage('Error loading expenses: ' + error.message, 'error');
        });
}

// Load summary data
function loadSummary() {
    fetch('/api/expenses')
        .then(response => response.json())
        .then(expenses => {
            // Total expenses
            const totalExpenses = expenses.reduce((sum, expense) => sum + parseFloat(expense.amount), 0);
            document.getElementById('total-expenses').textContent = `₹${totalExpenses.toFixed(2)}`;
            
            // This month expenses
            const currentDate = new Date();
            const currentMonth = currentDate.getMonth() + 1;
            const currentYear = currentDate.getFullYear();
            
            const monthlyExpenses = expenses.filter(expense => {
                const expenseDate = new Date(expense.date);
                return expenseDate.getMonth() + 1 === currentMonth && 
                       expenseDate.getFullYear() === currentYear;
            }).reduce((sum, expense) => sum + parseFloat(expense.amount), 0);
            
            document.getElementById('monthly-expenses').textContent = `₹${monthlyExpenses.toFixed(2)}`;
            
            // Total transactions
            document.getElementById('total-transactions').textContent = expenses.length;
            
            // Unique categories
            const categories = [...new Set(expenses.map(expense => expense.category))];
            document.getElementById('total-categories').textContent = categories.length;
        })
        .catch(error => {
            console.error('Error loading summary:', error);
        });
}

// Add new expense
function addExpense(e) {
    e.preventDefault();
    
    const date = document.getElementById('date').value;
    const category = document.getElementById('category').value;
    const amount = document.getElementById('amount').value;
    const notes = document.getElementById('notes').value;
    
    const expense = {
        date: date,
        category: category,
        amount: parseFloat(amount),
        notes: notes
    };
    
    fetch('/api/expenses', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(expense)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            showMessage(data.error, 'error');
        } else {
            showMessage('Expense added successfully!', 'success');
            expenseForm.reset();
            document.getElementById('date').value = new Date().toISOString().split('T')[0];
            loadExpenses();
            loadSummary();
        }
    })
    .catch(error => {
        showMessage('Error adding expense: ' + error.message, 'error');
    });
}

// Delete expense
function deleteExpense(id) {
    if (confirm('Are you sure you want to delete this expense?')) {
        fetch(`/api/expenses/${id}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showMessage(data.error, 'error');
            } else {
                showMessage('Expense deleted successfully!', 'success');
                loadExpenses();
                loadSummary();
            }
        })
        .catch(error => {
            showMessage('Error deleting expense: ' + error.message, 'error');
        });
    }
}

// Update chart with expense data
function updateChart(expenses) {
    // Group expenses by category
    const categoryTotals = {};
    
    expenses.forEach(expense => {
        if (!categoryTotals[expense.category]) {
            categoryTotals[expense.category] = 0;
        }
        categoryTotals[expense.category] += parseFloat(expense.amount);
    });
    
    // Prepare chart data
    const categories = Object.keys(categoryTotals);
    const amounts = Object.values(categoryTotals);
    
    // Destroy existing chart if it exists
    if (expenseChart) {
        expenseChart.destroy();
    }
    
    // Create new chart
    const ctx = document.getElementById('expenseChart').getContext('2d');
    expenseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categories,
            datasets: [{
                data: amounts,
                backgroundColor: [
                    '#3498db',
                    '#2ecc71',
                    '#e74c3c',
                    '#f39c12',
                    '#9b59b6',
                    '#1abc9c',
                    '#34495e',
                    '#e67e22',
                    '#27ae60',
                    '#8e44ad'
                ],
                borderWidth: 2,
                borderColor: '#fff',
                hoverBorderWidth: 3,
                hoverBorderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: 'circle',
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 14
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ₹${value.toFixed(2)} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true
            }
        }
    });
}

// Format date for display
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Show message
function showMessage(text, type) {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type} show`;
    
    // Clear message after 3 seconds
    setTimeout(() => {
        messageDiv.classList.remove('show');
    }, 3000);
}