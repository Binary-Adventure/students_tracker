import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import queries

class SubjectsTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()
        self.load_subjects()
    
    def create_widgets(self):
        """Create widgets for the Subjects tab"""
        # Left frame for subject list
        left_frame = ttk.Frame(self.frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Subjects treeview
        self.tree = ttk.Treeview(left_frame, columns=("ID", "Subject Name", "Teacher Name"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Subject Name", text="Название предмета")
        self.tree.heading("Teacher Name", text="Преподаватель")
        
        self.tree.column("ID", width=50)
        self.tree.column("Subject Name", width=200)
        self.tree.column("Teacher Name", width=200)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_subject_select)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Right frame for subject details
        right_frame = ttk.Frame(self.frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5, expand=False)
        
        # Subject form
        form_frame = ttk.LabelFrame(right_frame, text="Данные предмета")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Название предмета:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.subject_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.subject_name_var).grid(row=0, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Преподаватель:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.teacher_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.teacher_name_var).grid(row=1, column=1, sticky=tk.W+tk.E, padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="Добавить", command=self.add_subject).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Обновить", command=self.update_subject).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.delete_subject).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Очистить форму", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Set column weights
        form_frame.columnconfigure(1, weight=1)
    
    def load_subjects(self):
        """Load subjects from database and display in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get subjects from database
        subjects = queries.get_all_subjects()
        
        # Add subjects to treeview
        for subject in subjects:
            self.tree.insert("", tk.END, values=subject)
    
    def on_subject_select(self, event):
        """Handle subject selection in treeview"""
        selected_items = self.tree.selection()
        if selected_items:
            item = selected_items[0]
            values = self.tree.item(item, "values")
            
            # Update form fields
            self.subject_name_var.set(values[1])
            self.teacher_name_var.set(values[2])
    
    def add_subject(self):
        """Add a new subject to the database"""
        subject_name = self.subject_name_var.get().strip()
        teacher_name = self.teacher_name_var.get().strip()
        
        # Validate input
        if not self.validate_subject_input(subject_name, teacher_name):
            return
        
        # Add subject to database
        subject_id = queries.add_subject(subject_name, teacher_name)
        
        if subject_id:
            messagebox.showinfo("Успех", "Предмет успешно добавлен")
            self.clear_form()
            self.load_subjects()
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить предмет")
    
    def update_subject(self):
        """Update selected subject in the database"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите предмет для обновления")
            return
        
        item = selected_items[0]
        subject_id = self.tree.item(item, "values")[0]
        
        subject_name = self.subject_name_var.get().strip()
        teacher_name = self.teacher_name_var.get().strip()
        
        # Validate input
        if not self.validate_subject_input(subject_name, teacher_name):
            return
        
        # Update subject in database (we need to implement this function in queries.py)
        conn = queries.get_connection()
        if not conn:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных")
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE subjects SET subject_name = %s, teacher_name = %s WHERE subject_id = %s",
                (subject_name, teacher_name, subject_id)
            )
            conn.commit()
            messagebox.showinfo("Успех", "Данные предмета обновлены")
            self.load_subjects()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Ошибка", f"Не удалось обновить данные предмета: {e}")
        finally:
            conn.close()
    
    def delete_subject(self):
        """Delete selected subject from the database"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите предмет для удаления")
            return
        
        item = selected_items[0]
        subject_id = self.tree.item(item, "values")[0]
        subject_name = self.tree.item(item, "values")[1]
        
        # Confirm deletion
        if not messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить предмет '{subject_name}'?"):
            return
        
        # Delete subject from database
        success = queries.delete_subject(subject_id)
        
        if success:
            messagebox.showinfo("Успех", "Предмет удален")
            self.clear_form()
            self.load_subjects()
        else:
            messagebox.showerror("Ошибка", "Не удалось удалить предмет")
    
    def clear_form(self):
        """Clear form fields"""
        self.subject_name_var.set("")
        self.teacher_name_var.set("")
        
        # Deselect items in treeview
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def validate_subject_input(self, subject_name, teacher_name):
        """Validate subject input fields"""
        if not subject_name:
            messagebox.showwarning("Предупреждение", "Введите название предмета")
            return False
        
        if len(subject_name) < 2:
            messagebox.showwarning("Предупреждение", "Название предмета должно содержать не менее 2 символов")
            return False
        
        if not teacher_name:
            messagebox.showwarning("Предупреждение", "Введите имя преподавателя")
            return False
        
        if len(teacher_name) < 2:
            messagebox.showwarning("Предупреждение", "Имя преподавателя должно содержать не менее 2 символов")
            return False
        
        return True