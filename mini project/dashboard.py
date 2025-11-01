import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import calendar
from datetime import datetime
from db_config import DATABASE_NAME

class ExpenseDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title(" Expense Tracker Dashboard")
        self.root.geometry("1100x750")
        self.root.configure(bg='#f0f0f0')
        
        # Configure styles
        self.configure_styles()
        
        # Create the UI
        self.create_widgets()
        
        # Load data
        self.load_data()
        
    def configure_styles(self):
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure button style
        self.style.configure('Custom.TButton',
                           foreground='white',
                           background='#3498db',
                           font=('Arial', 10, 'bold'),
                           padding=6)
        
        # Configure combobox style
        self.style.configure('Custom.TCombobox',
                           foreground='#2c3e50',
                           background='white',
                           fieldbackground='white')
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="💰 Expense Tracker Dashboard", 
                              font=('Arial', 22, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=15)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel for controls
        left_frame = tk.Frame(content_frame, bg='#ecf0f1', width=280, relief=tk.RAISED, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_frame.pack_propagate(False)
        
        # Controls title
        controls_title = tk.Label(left_frame, text="📊 Dashboard Controls", 
                                 font=('Arial', 16, 'bold'), bg='#3498db', fg='white', 
                                 padx=10, pady=15)
        controls_title.pack(fill=tk.X)
        
        # Controls container
        controls_container = tk.Frame(left_frame, bg='#ecf0f1')
        controls_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=20)
        
        # Month selection
        month_label = tk.Label(controls_container, text="Select Month:", 
                              font=('Arial', 11, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        month_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Get current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Month dropdown
        self.month_var = tk.StringVar(value=calendar.month_name[current_month])
        months = [calendar.month_name[i] for i in range(1, 13)]
        month_dropdown = ttk.Combobox(controls_container, textvariable=self.month_var, 
                                     values=months, state="readonly", font=('Arial', 10))
        month_dropdown.pack(fill=tk.X, pady=(0, 15))
        
        # Year entry
        year_label = tk.Label(controls_container, text="Enter Year:", 
                             font=('Arial', 11, 'bold'), bg='#ecf0f1', fg='#2c3e50')
        year_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.year_var = tk.StringVar(value=str(current_year))
        year_entry = tk.Entry(controls_container, textvariable=self.year_var, 
                             font=('Arial', 10), relief=tk.FLAT, bd=1, 
                             highlightbackground='#3498db', highlightthickness=1)
        year_entry.pack(fill=tk.X, pady=(0, 25))
        
        # Refresh button
        refresh_btn = tk.Button(controls_container, text="🔄 Refresh Data", command=self.load_data,
                               bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                               relief=tk.FLAT, padx=10, pady=8, cursor='hand2',
                               activebackground='#2980b9', activeforeground='white')
        refresh_btn.pack(fill=tk.X, pady=(0, 20))
        
        # Summary statistics frame
        stats_frame = tk.Frame(controls_container, bg='#bdc3c7', relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        # Summary title
        stats_title = tk.Label(stats_frame, text="📈 Summary", 
                              font=('Arial', 12, 'bold'), bg='#95a5a6', fg='white',
                              padx=10, pady=8)
        stats_title.pack(fill=tk.X)
        
        # Summary content
        stats_content = tk.Frame(stats_frame, bg='#bdc3c7')
        stats_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=15)
        
        self.total_expenses_label = tk.Label(stats_content, text="Total Expenses: ₹0.00", 
                                            font=('Arial', 11, 'bold'), bg='#bdc3c7', 
                                            fg='#2c3e50', wraplength=220, justify=tk.LEFT)
        self.total_expenses_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.most_expensive_label = tk.Label(stats_content, text="Most Expensive Category: None", 
                                            font=('Arial', 10), bg='#bdc3c7', fg='#2c3e50', 
                                            wraplength=220, justify=tk.LEFT)
        self.most_expensive_label.pack(anchor=tk.W)
        
        # Right panel for charts
        right_frame = tk.Frame(content_frame, bg='white', relief=tk.RAISED, bd=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Pie chart title
        chart_title = tk.Label(right_frame, text="Monthly Expense Distribution", 
                              font=('Arial', 16, 'bold'), bg='#3498db', fg='white',
                              padx=15, pady=12)
        chart_title.pack(fill=tk.X)
        
        # Create matplotlib figure with enhanced styling
        self.figure, self.ax = plt.subplots(figsize=(8, 6), dpi=100, facecolor='#f8f9fa')
        self.ax.set_facecolor('#f8f9fa')
        
        # Style the chart
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        
        self.canvas = FigureCanvasTkAgg(self.figure, right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
    def load_data(self):
        try:
            # Get selected month and year
            selected_month = list(calendar.month_name).index(self.month_var.get())
            selected_year = int(self.year_var.get())
            
            # Connect to database
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            # Query to get expenses for the selected month
            cursor.execute("""
                SELECT category, SUM(amount) as total 
                FROM expenses 
                WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                GROUP BY category
            """, (f"{selected_month:02d}", str(selected_year)))
            
            results = cursor.fetchall()
            conn.close()
            
            # Update the pie chart
            self.update_pie_chart(results)
            
            # Update summary statistics
            self.update_summary_stats(results)
            
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def update_pie_chart(self, data):
        # Clear the previous plot
        self.ax.clear()
        
        if not data:
            # Display a message if no data
            self.ax.text(0.5, 0.5, 'No data available for selected period', 
                        horizontalalignment='center', verticalalignment='center', 
                        transform=self.ax.transAxes, fontsize=14, color='#7f8c8d',
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="#ecf0f1"))
            self.ax.set_title("Monthly Expense Distribution", fontsize=14, pad=20, 
                             color='#2c3e50', fontweight='bold')
        else:
            # Extract categories and amounts
            categories = [item[0] for item in data]
            amounts = [item[1] for item in data]
            
            # Create enhanced pie chart
            colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', 
                     '#1abc9c', '#34495e', '#e67e22', '#27ae60', '#8e44ad']
            
            pie_result = self.ax.pie(amounts, labels=categories, autopct='%1.1f%%', 
                                   colors=colors[:len(categories)], startangle=90,
                                   explode=[0.05] * len(categories))
            
            # Handle different return types from pie chart
            if len(pie_result) == 3:
                wedges, texts, autotexts = pie_result
                # Improve text appearance
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(9)
            else:
                wedges, texts = pie_result
                # Improve text appearance
                for text in texts:
                    text.set_fontsize(10)
                    text.set_color('#2c3e50')
                    text.set_fontweight('bold')
            
            for text in texts:
                text.set_fontsize(10)
                text.set_color('#2c3e50')
                text.set_fontweight('bold')
            
            self.ax.set_title("Monthly Expense Distribution", fontsize=14, pad=20, 
                             color='#2c3e50', fontweight='bold')
            
        # Draw the canvas
        self.canvas.draw()
        
    def update_summary_stats(self, data):
        if not data:
            self.total_expenses_label.config(text="Total Expenses: ₹0.00")
            self.most_expensive_label.config(text="Most Expensive Category: None")
        else:
            # Calculate total expenses
            total = sum([item[1] for item in data])
            self.total_expenses_label.config(text=f"Total Expenses: ₹{total:.2f}")
            
            # Find most expensive category
            max_item = max(data, key=lambda x: x[1])
            self.most_expensive_label.config(text=f"Most Expensive Category: {max_item[0]}\n(₹{max_item[1]:.2f})")

def main():
    root = tk.Tk()
    app = ExpenseDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()