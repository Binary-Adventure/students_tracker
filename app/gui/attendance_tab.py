import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import queries
from utils import validators, export_csv

class AttendanceTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.create_widgets()
    
    def create_widgets(self):
        """Create widgets for the Attendance tab"""
        # Top frame for date and subject selection
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(top_frame, text="Дата:").pack(side=tk.LEFT, padx=5)
        self.date_var = tk.StringVar()
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(top_frame, textvariable=self.date_var, width=12).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(top_frame, text="Предмет:").pack(side=tk.LEFT, padx=5)
        self.subject_var = tk.StringVar()
        self.subject_combo = ttk.Combobox(top_frame, textvariable=self.subject_var, state="readonly", width=30)
        self.subject_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(top_frame, text="Загрузить", command=self.load_attendance_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Новый день", command=self.prepare_new_attendance).pack(side=tk.LEFT, padx=5)
        
        # Main frame for attendance list
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Attendance treeview
        self.tree = ttk.Treeview(main_frame, columns=("ID", "Student ID", "Name", "Group", "Present"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Student ID", text="Студент ID")
        self.tree.heading("Name", text="ФИО")
        self.tree.heading("Group", text="Группа")
        self.tree.heading("Present", text="Присутствие")
        
        self.tree.column("ID", width=50)
        self.tree.column("Student ID", width=80)
        self.tree.column("Name", width=200)
        self.tree.column("Group", width=100)
        self.tree.column("Present", width=100)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Bottom frame for buttons
        bottom_frame = ttk.Frame(self.frame)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(bottom_frame, text="Отметить присутствие", command=lambda: self.mark_attendance(True)).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Отметить отсутствие", command=lambda: self.mark_attendance(False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Сохранить изменения", command=self.save_attendance).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Экспорт в CSV", command=self.export_to_csv).pack(side=tk.RIGHT, padx=5)
        
        # Load subjects
        self.load_subjects()
        
        # Store attendance records for saving
        self.attendance_records = []
        self.new_attendance_mode = False
    
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
    
    def load_attendance_data(self):
        """Load attendance data for selected date and subject"""
        date = self.date_var.get().strip()
        if not date or not validators.validate_date_format(date):
            messagebox.showwarning("Предупреждение", "Введите корректную дату (ГГГГ-ММ-ДД)")
            return
        
        selected_subject = self.subject_var.get()
        subject_id = None
        if selected_subject and selected_subject in self.subject_map:
            subject_id = self.subject_map[selected_subject]
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get attendance records from database
        attendance_records = queries.get_attendance_by_date(date, subject_id)
        
        if not attendance_records:
            messagebox.showinfo("Информация", "Нет данных о посещаемости на выбранную дату")
            self.new_attendance_mode = False
            self.attendance_records = []
            return
        
        # Add attendance records to treeview
        for record in attendance_records:
            attendance_id, student_id, first_name, last_name, group, subject_name, is_present = record
            student_name = f"{last_name} {first_name}"
            present_text = "Да" if is_present else "Нет"
            
            self.tree.insert("", tk.END, values=(attendance_id, student_id, student_name, group, present_text))
        
        self.new_attendance_mode = False
        self.attendance_records = []
    
    def prepare_new_attendance(self):
        """Prepare new attendance records for all students"""
        date = self.date_var.get().strip()
        if not date or not validators.validate_date_format(date):
            messagebox.showwarning("Предупреждение", "Введите корректную дату (ГГГГ-ММ-ДД)")
            return
        
        selected_subject = self.subject_var.get()
        if not selected_subject or selected_subject not in self.subject_map:
            messagebox.showwarning("Предупреждение", "Выберите предмет")
            return
        
        subject_id = self.subject_map[selected_subject]
        
        # Check if attendance records already exist for this date and subject
        conn = queries.get_connection()
        if not conn:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных")
            return
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM attendance WHERE date = %s AND subject_id = %s",
                (date, subject_id)
            )
            count = cursor.fetchone()[0]
            
            if count > 0:
                if not messagebox.askyesno("Подтверждение", 
                                          "Данные о посещаемости на эту дату уже существуют. Хотите загрузить их?"):
                    return
                else:
                    self.load_attendance_data()
                    return
        finally:
            conn.close()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all students
        students = queries.get_all_students()
        
        if not students:
            messagebox.showinfo("Информация", "Нет студентов в базе данных")
            return
        
        # Add students to treeview with default attendance (not present)
        self.attendance_records = []
        
        for student in students:
            student_id, first_name, last_name, group, _ = student
            student_name = f"{last_name} {first_name}"
            
            self.tree.insert("", tk.END, values=("Новый", student_id, student_name, group, "Нет"))
            
            # Store attendance record for saving
            self.attendance_records.append({
                "student_id": student_id,
                "subject_id": subject_id,
                "is_present": False,
                "date": date
            })
        
        self.new_attendance_mode = True
        messagebox.showinfo("Информация", "Подготовлены новые записи о посещаемости. Отметьте присутствующих студентов и нажмите 'Сохранить изменения'.")
    
    def mark_attendance(self, is_present):
        """Mark selected students as present or absent"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Предупреждение", "Выберите студентов")
            return
        
        present_text = "Да" if is_present else "Нет"
        
        for item in selected_items:
            values = list(self.tree.item(item, "values"))
            values[4] = present_text
            self.tree.item(item, values=values)
            
            # Update attendance record if in new attendance mode
            if self.new_attendance_mode:
                student_id = values[1]
                for record in self.attendance_records:
                    if record["student_id"] == student_id:
                        record["is_present"] = is_present
    
    def save_attendance(self):
        """Save attendance records to database"""
        if not self.new_attendance_mode:
            messagebox.showinfo("Информация", "Нет новых записей для сохранения")
            return
        
        # Save all attendance records
        success_count = 0
        for record in self.attendance_records:
            attendance_id = queries.add_attendance(
                record["student_id"],
                record["subject_id"],
                record["is_present"],
                record["date"]
            )
            
            if attendance_id:
                success_count += 1
        
        if success_count == len(self.attendance_records):
            messagebox.showinfo("Успех", "Все записи о посещаемости сохранены")
            self.new_attendance_mode = False
            self.attendance_records = []
        else:
            messagebox.showwarning("Предупреждение", f"Сохранено {success_count} из {len(self.attendance_records)} записей")
    
    def export_to_csv(self):
        """Export attendance data to CSV file"""
        # Get all attendance records from treeview
        attendance_data = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            attendance_data.append(values)
        
        if not attendance_data:
            messagebox.showinfo("Экспорт", "Нет данных для экспорта")
            return
        
        # Get date for filename
        date = self.date_var.get().strip()
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Сохранить CSV файл",
            initialfile=f"attendance_{date}.csv"
        )
        
        if not file_path:
            return  # User cancelled
        
        # Export data
        result = export_csv.export_attendance_to_csv(attendance_data, date, file_path)
        
        if result:
            messagebox.showinfo("Экспорт", f"Данные успешно экспортированы в {file_path}")
        else:
            messagebox.showerror("Ошибка", "Не удалось экспортировать данные")