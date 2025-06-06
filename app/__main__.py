import tkinter as tk
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.gui.main_window import MainWindow
from app.database.db_connect import get_connection
from app.database.db_init import create_tables

def main():
    """Main entry point for the application"""
    # Check database connection
    conn = get_connection()
    if not conn:
        print("Error: Could not connect to the database.")
        print("Please check your database settings and try again.")
        sys.exit(1)
    conn.close()
    
    # Create tables if they don't exist
    create_tables()
    
    # Start the GUI
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()