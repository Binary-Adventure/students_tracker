import csv
import os
from datetime import datetime

def export_students_to_csv(students_data, output_path=None):
    """
    Export students data to CSV file
    
    Args:
        students_data: List of tuples containing student information
        output_path: Path to save the CSV file (optional)
    
    Returns:
        Path to the saved CSV file
    """
    if output_path is None:
        # Create a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"students_export_{timestamp}.csv"
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['ID', 'First Name', 'Last Name', 'Group', 'Email'])
            # Write data
            for student in students_data:
                writer.writerow(student)
        
        return output_path
    except Exception as e:
        print(f"Error exporting students to CSV: {e}")
        return None

def export_grades_to_csv(grades_data, student_name=None, output_path=None):
    """
    Export grades data to CSV file
    
    Args:
        grades_data: List of tuples containing grade information
        student_name: Name of the student (optional)
        output_path: Path to save the CSV file (optional)
    
    Returns:
        Path to the saved CSV file
    """
    if output_path is None:
        # Create a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"grades_export_{timestamp}.csv"
        if student_name:
            filename = f"grades_{student_name.replace(' ', '_')}_{timestamp}.csv"
        output_path = filename
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['ID', 'Subject', 'Grade', 'Date'])
            # Write data
            for grade in grades_data:
                writer.writerow(grade)
        
        return output_path
    except Exception as e:
        print(f"Error exporting grades to CSV: {e}")
        return None

def export_attendance_to_csv(attendance_data, date=None, output_path=None):
    """
    Export attendance data to CSV file
    
    Args:
        attendance_data: List of tuples containing attendance information
        date: Date of attendance (optional)
        output_path: Path to save the CSV file (optional)
    
    Returns:
        Path to the saved CSV file
    """
    if output_path is None:
        # Create a filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"attendance_export_{timestamp}.csv"
        if date:
            filename = f"attendance_{date}_{timestamp}.csv"
        output_path = filename
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['ID', 'Student Name', 'Group', 'Subject', 'Present', 'Date'])
            # Write data
            for record in attendance_data:
                writer.writerow(record)
        
        return output_path
    except Exception as e:
        print(f"Error exporting attendance to CSV: {e}")
        return None