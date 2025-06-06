import tkinter as tk
from tkinter import ttk, messagebox
from .students_tab import StudentsTab
from .subjects_tab import SubjectsTab
from .grades_tab import GradesTab
from .attendance_tab import AttendanceTab

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет студентов в колледже")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)
        
        # Create notebook (tabs container)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.students_tab = StudentsTab(self.notebook)
        self.subjects_tab = SubjectsTab(self.notebook)
        self.grades_tab = GradesTab(self.notebook)
        self.attendance_tab = AttendanceTab(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.students_tab.frame, text="Студенты")
        self.notebook.add(self.subjects_tab.frame, text="Предметы")
        self.notebook.add(self.grades_tab.frame, text="Оценки")
        self.notebook.add(self.attendance_tab.frame, text="Посещаемость")
        
        # Create status bar
        self.status_bar = tk.Label(self.root, text="Готово", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create menu
        self.create_menu()
        
        # Set up protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_menu(self):
        """Create application menu"""
        menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Экспорт данных", command=self.export_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_close)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menu_bar.add_cascade(label="Справка", menu=help_menu)
        
        self.root.config(menu=menu_bar)
    
    def export_data(self):
        """Export data based on current tab"""
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab == 0:  # Students tab
            self.students_tab.export_to_csv()
        elif current_tab == 2:  # Grades tab
            self.grades_tab.export_to_csv()
        elif current_tab == 3:  # Attendance tab
            self.attendance_tab.export_to_csv()
        else:
            messagebox.showinfo("Экспорт", "Экспорт недоступен для этой вкладки")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "О программе",
            "Учет студентов в колледже\n\n"
            "Версия: 1.0\n"
            "Программа для учета студентов, их успеваемости и посещаемости"
        )
    
    def on_close(self):
        """Handle window close event"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()

def run_app():
    """Run the application"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()