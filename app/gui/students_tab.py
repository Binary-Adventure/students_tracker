import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import queries
from utils import validators, export_csv

class StudentsTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()
        self.load_students()
    
    def create_widgets(self):
        """Create widgets for the Students tab"""
        # Left frame for student list
        left_frame = ttk.Frame(self.frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Search frame
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        ttk.Button(search_frame, text="Очистить", command=self.clear_search).pack(side=tk.LEFT, padx=5)
        
        # Students treeview
        self.tree = ttk.Treeview(left_frame, columns=("ID", "First Name", "Last Name", "Group", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("First Name", text="Имя")
        self.tree.heading("Last Name", text="Фамилия")
        self.tree.heading("Group", text="Группа")
        self.tree.heading("Email", text="Email")
        
        self.tree.column("ID", width=50)
        self.tree.column("First Name", width=100)
        self.tree.column("Last Name", width=100)
        self.tree.column("Group", width=80)
        self.tree.column("Email", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_student_select)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Right frame for student details
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5, expand=False)
        
        # Student form
        form_frame = ttk.LabelFrame(right_frame, text="Данные студента")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.first_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.first_name_var).grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Фамилия:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.last_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.last_name_var).grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Группа:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.group_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.group_var).grid(row=2, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var).grid(row=3, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="Добавить", command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Обновить", command=self.update_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.delete_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Очистить форму", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Export button
        ttk.Button(right_frame, text="Экспорт в CSV", command=self.export_to_csv).pack(fill=tk.X, padx=5, pady=5)
        
        # Set column weights
        form_frame.columnconfigure(1, weight=1)
    
    def load_students(self):
        """Load students from database and display in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get students from database
        students = queries.get_all_students()
        
        # Add students to treeview
        for student in students:
            self.tree.insert("", tk.END, values=student)
    
    def on_student_select(self, event):
        """Handle student selection in treeview"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, "values")
            
            # Update form fields
            self.first_name_var.set(values[1])
            self.last_name_var.set(values[2])
            self.group_var.set(values[3])
            self.email_var.set(values[4])
    
    def add_student(self):
        """Add a new student to the database"""
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        group = self.group_var.get().strip()
        email = self.email_var.get().strip()
        
        # Validate input
        if not self.validate_student_input(first_name, last_name, group, email):
            return
        
        # Add student to database
        student_id = queries.add_student(first_name, last_name, group, email)
        
        if student_id:
            messagebox.showinfo("Успех", "Студент успешно добавлен")
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить студента")
    
    def update_student(self):
        """Update selected student in the database"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите студента для обновления")
            return
        
        item = selected_items[0]
        student_id = self.tree.item(item, "values")[0]
        
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        group = self.group_var.get().strip()
        email = self.email_var.get().strip()
        
        # Validate input
        if not self.validate_student_input(first_name, last_name, group, email):
            return
        
        # Update student in database
        success = queries.update_student(student_id, first_name, last_name, group, email)
        
        if success:
            messagebox.showinfo("Успех", "Данные студента обновлены")
            self.load_students()
        else:
            messagebox.showerror("Ошибка", "Не удалось обновить данные студента")
    
    def delete_student(self):
        """Delete selected student from the database"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите студента для удаления")
            return
        
        item = selected_items[0]
        student_id = self.tree.item(item, "values")[0]
        student_name = f"{self.tree.item(item, 'values')[2]} {self.tree.item(item, 'values')[1]}"
        
        # Confirm deletion
        if not messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить студента {student_name}?"):
            return
        
        # Delete student from database
        success = queries.delete_student(student_id)
        
        if success:
            messagebox.showinfo("Успех", "Студент удален")
            self.clear_form()
            self.load_students()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить студента")
    
    def clear_form(self):
        """Clear form fields"""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.group_var.set("")
        self.email_var.set("")
        
        # Deselect items in treeview
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def on_search(self, event):
        """Handle search input"""
        search_term = self.search_var.get().strip()
        
        if search_term:
            # Search students in database
            students = queries.search_students(search_term)
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Add filtered students to treeview
            for student in students:
                self.tree.insert("", tk.END, values=student)
        else:
            # If search field is empty, load all students
            self.load_students()
    
    def clear_search(self):
        """Clear search field and reload all students"""
        self.search_var.set("")
        self.load_students()
    
    def export_to_csv(self):
        """Export students data to CSV file"""
        # Get all students from treeview
        students_data = []
        for item in self.tree.get_children():
            students_data.append(self.tree.item(item, "values"))
        
        if not students_data:
            messagebox.showinfo("Экспорт", "Нет данных для экспорта")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Сохранить CSV файл"
        )
        
        if not file_path:
            return  # User cancelled
        
        # Export data
        result = export_csv.export_students_to_csv(students_data, file_path)
        
        if result:
            messagebox.showinfo("Экспорт", f"Данные успешно экспортированы в {file_path}")
        else:
            messagebox.showerror("Ошибка", "Не удалось экспортировать данные")
    
    def validate_student_input(self, first_name, last_name, group, email):
        """Validate student input fields"""
        if not first_name:
            messagebox.showwarning("Предупреждение", "Введите имя студента")
            return False
        
        if not validators.validate_name(first_name):
            messagebox.showwarning("Предупреждение", "Некорректное имя студента")
            return False
        
        if not last_name:
            messagebox.showwarning("Предупреждение", "Введите фамилию студента")
            return False
        
        if not validators.validate_name(last_name):
            messagebox.showwarning("Предупреждение", "Некорректная фамилия студента")
            return False
        
        if not group:
            messagebox.showwarning("Предупреждение", "Введите группу студента")
            return False
        
        if not validators.validate_group_name(group):
            messagebox.showwarning("Предупреждение", "Некорректное название группы")
            return False
        
        if not email:
            messagebox.showwarning("Предупреждение", "Введите email студента")
            return False
        
        if not validators.validate_email(email):
            messagebox.showwarning("Предупреждение", "Некорректный email")
            return False
        
        return True