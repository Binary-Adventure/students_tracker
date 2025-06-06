import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import queries
from utils import validators, export_csv

class GradesTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()
        self.selected_student_id = None
    
    def create_widgets(self):
        """Create widgets for the Grades tab"""
        # Top frame for student selection
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(top_frame, text="Выберите студента:").pack(side=tk.LEFT, padx=5)
        
        # Student combobox
        self.student_var = tk.StringVar()
        self.student_combo = ttk.Combobox(top_frame, textvariable=self.student_var, state="readonly", width=40)
        self.student_combo.pack(side=tk.LEFT, padx=5)
        self.student_combo.bind("<<ComboboxSelected>>", self.on_student_select)
        
        # Refresh button
        ttk.Button(top_frame, text="Обновить список", command=self.load_students).pack(side=tk.LEFT, padx=5)
        
        # Date range frame
        date_frame = ttk.LabelFrame(self.frame, text="Период")
        date_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(date_frame, text="С:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_date_var = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.start_date_var, width=12).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(date_frame, text="(ГГГГ-ММ-ДД)").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(date_frame, text="По:").grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.end_date_var = tk.StringVar()
        ttk.Entry(date_frame, textvariable=self.end_date_var, width=12).grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        ttk.Label(date_frame, text="(ГГГГ-ММ-ДД)").grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        
        ttk.Button(date_frame, text="Применить фильтр", command=self.load_grades).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(date_frame, text="Сбросить", command=self.reset_filter).grid(row=0, column=7, padx=5, pady=5)
        
        # Left frame for grades list
        left_frame = ttk.Frame(self.frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Grades treeview
        self.tree = ttk.Treeview(left_frame, columns=("ID", "Subject", "Grade", "Date"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Subject", text="Предмет")
        self.tree.heading("Grade", text="Оценка")
        self.tree.heading("Date", text="Дата")
        
        self.tree.column("ID", width=50)
        self.tree.column("Subject", width=200)
        self.tree.column("Grade", width=80)
        self.tree.column("Date", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Right frame for adding grades
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5, expand=False)
        
        # Add grade form
        form_frame = ttk.LabelFrame(right_frame, text="Добавить оценку")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Предмет:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(form_frame, textvariable=self.subject_var, state="readonly")
        self.subject_combo.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Оценка (1-5):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.grade_var = tk.StringVar()
        ttk.Spinbox(form_frame, from_=1, to=5, textvariable=self.grade_var, width=5).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Дата:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_var = tk.StringVar()
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=self.date_var).grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Add grade button
        ttk.Button(form_frame, text="Добавить оценку", command=self.add_grade).grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky=tk.E+tk.W)
        
        # Export button
        ttk.Button(right_frame, text="Экспорт в CSV", command=self.export_to_csv).pack(fill=tk.X, padx=5, pady=5)
        
        # Set column weights
        form_frame.columnconfigure(1, weight=1)
        
        # Load students and subjects
        self.load_students()
        self.load_subjects()
    
    def load_students(self):
        """Load students from database and populate combobox"""
        students = queries.get_all_students()
        
        # Format student names for combobox
        student_list = []
        self.student_map = {}  # Map display names to student IDs
        
        for student in students:
            student_id, first_name, last_name, group, _ = student
            display_name = f"{last_name} {first_name} ({group})"
            student_list.append(display_name)
            self.student_map[display_name] = student_id
        
        self.student_combo['values'] = student_list
        
        # Clear selection if no students
        if not student_list:
            self.student_var.set("")
            self.selected_student_id = None
            # Clear grades list
            for item in self.tree.get_children():
                self.tree.delete(item)
    
    def load_subjects(self):
        """Load subjects from database and populate combobox"""
        subjects = queries.get_all_subjects()
        
        # Format subject names for combobox
        subject_list = []
        self.subject_map = {}  # Map display names to subject IDs
        
        for subject in subjects:
            subject_id, subject_name, teacher_name = subject
            display_name = f"{subject_name} ({teacher_name})"
            subject_list.append(display_name)
            self.subject_map[display_name] = subject_id
        
        self.subject_combo['values'] = subject_list
    
    def on_student_select(self, event):
        """Handle student selection in combobox"""
        selected_student = self.student_var.get()
        if selected_student in self.student_map:
            self.selected_student_id = self.student_map[selected_student]
            self.load_grades()
    
    def load_grades(self):
        """Load grades for selected student and display in treeview"""
        if not self.selected_student_id:
            return
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get date range if specified
        start_date = self.start_date_var.get().strip() or None
        end_date = self.end_date_var.get().strip() or None
        
        # Validate date format if provided
        if start_date and not validators.validate_date_format(start_date):
            messagebox.showwarning("Предупреждение", "Некорректный формат начальной даты (ГГГГ-ММ-ДД)")
            return
        
        if end_date and not validators.validate_date_format(end_date):
            messagebox.showwarning("Предупреждение", "Некорректный формат конечной даты (ГГГГ-ММ-ДД)")
            return
        
        # Get grades from database
        grades = queries.get_student_grades(self.selected_student_id, start_date, end_date)
        
        # Add grades to treeview
        for grade in grades:
            self.tree.insert("", tk.END, values=grade)
    
    def reset_filter(self):
        """Reset date filter and reload grades"""
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.load_grades()
    
    def add_grade(self):
        """Add a new grade to the database"""
        if not self.selected_student_id:
            messagebox.showwarning("Предупреждение", "Выберите студента")
            return
        
        selected_subject = self.subject_var.get()
        if not selected_subject or selected_subject not in self.subject_map:
            messagebox.showwarning("Предупреждение", "Выберите предмет")
            return
        
        subject_id = self.subject_map[selected_subject]
        
        grade = self.grade_var.get().strip()
        if not grade or not validators.validate_grade(grade):
            messagebox.showwarning("Предупреждение", "Введите корректную оценку (1-5)")
            return
        
        date = self.date_var.get().strip()
        if not date or not validators.validate_date_format(date):
            messagebox.showwarning("Предупреждение", "Введите корректную дату (ГГГГ-ММ-ДД)")
            return
        
        # Add grade to database
        grade_id = queries.add_grade(self.selected_student_id, subject_id, int(grade), date)
        
        if grade_id:
            messagebox.showinfo("Успех", "Оценка успешно добавлена")
            self.load_grades()
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить оценку")
    
    def export_to_csv(self):
        """Export grades data to CSV file"""
        if not self.selected_student_id:
            messagebox.showwarning("Предупреждение", "Выберите студента")
            return
        
        # Get all grades from treeview
        grades_data = []
        for item in self.tree.get_children():
            grades_data.append(self.tree.item(item, "values"))
        
        if not grades_data:
            messagebox.showinfo("Экспорт", "Нет данных для экспорта")
            return
        
        # Get student name for filename
        student_name = self.student_var.get().split(" (")[0]
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Сохранить CSV файл",
            initialfile=f"grades_{student_name}.csv"
        )
        
        if not file_path:
            return  # User cancelled
        
        # Export data
        result = export_csv.export_grades_to_csv(grades_data, student_name, file_path)
        
        if result:
            messagebox.showinfo("Экспорт", f"Данные успешно экспортированы в {file_path}")
        else:
            messagebox.showerror("Ошибка", "Не удалось экспортировать данные")