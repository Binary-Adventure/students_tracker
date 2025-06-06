from .db_connect import get_connection

# Student queries
def add_student(first_name, last_name, group_name, email):
    """Add a new student to the database"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (first_name, last_name, group_name, email) VALUES (%s, %s, %s, %s) RETURNING student_id",
            (first_name, last_name, group_name, email)
        )
        student_id = cursor.fetchone()[0]
        conn.commit()
        return student_id
    except Exception as e:
        conn.rollback()
        print(f"Error adding student: {e}")
        return None
    finally:
        conn.close()

def get_all_students():
    """Get all students from the database"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, first_name, last_name, group_name, email FROM students ORDER BY last_name, first_name")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting students: {e}")
        return []
    finally:
        conn.close()

def update_student(student_id, first_name, last_name, group_name, email):
    """Update student information"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET first_name = %s, last_name = %s, group_name = %s, email = %s WHERE student_id = %s",
            (first_name, last_name, group_name, email, student_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Error updating student: {e}")
        return False
    finally:
        conn.close()

def delete_student(student_id):
    """Delete a student from the database"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Error deleting student: {e}")
        return False
    finally:
        conn.close()

def search_students(search_term):
    """Search for students by name or group"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        search_pattern = f"%{search_term}%"
        cursor.execute(
            """SELECT student_id, first_name, last_name, group_name, email 
               FROM students 
               WHERE first_name ILIKE %s OR last_name ILIKE %s OR group_name ILIKE %s
               ORDER BY last_name, first_name""",
            (search_pattern, search_pattern, search_pattern)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error searching students: {e}")
        return []
    finally:
        conn.close()

# Subject queries
def add_subject(subject_name, teacher_name):
    """Add a new subject to the database"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO subjects (subject_name, teacher_name) VALUES (%s, %s) RETURNING subject_id",
            (subject_name, teacher_name)
        )
        subject_id = cursor.fetchone()[0]
        conn.commit()
        return subject_id
    except Exception as e:
        conn.rollback()
        print(f"Error adding subject: {e}")
        return None
    finally:
        conn.close()

def get_all_subjects():
    """Get all subjects from the database"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT subject_id, subject_name, teacher_name FROM subjects ORDER BY subject_name")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting subjects: {e}")
        return []
    finally:
        conn.close()

def delete_subject(subject_id):
    """Delete a subject from the database"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM subjects WHERE subject_id = %s", (subject_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Error deleting subject: {e}")
        return False
    finally:
        conn.close()

# Grade queries
def add_grade(student_id, subject_id, grade, date):
    """Add a new grade to the database"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO grades (student_id, subject_id, grade, date) VALUES (%s, %s, %s, %s) RETURNING grade_id",
            (student_id, subject_id, grade, date)
        )
        grade_id = cursor.fetchone()[0]
        conn.commit()
        return grade_id
    except Exception as e:
        conn.rollback()
        print(f"Error adding grade: {e}")
        return None
    finally:
        conn.close()

def get_student_grades(student_id, start_date=None, end_date=None):
    """Get grades for a specific student with optional date range"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        query = """
            SELECT g.grade_id, s.subject_name, g.grade, g.date
            FROM grades g
            JOIN subjects s ON g.subject_id = s.subject_id
            WHERE g.student_id = %s
        """
        params = [student_id]
        
        if start_date:
            query += " AND g.date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND g.date <= %s"
            params.append(end_date)
            
        query += " ORDER BY g.date DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting student grades: {e}")
        return []
    finally:
        conn.close()

# Attendance queries
def add_attendance(student_id, subject_id, is_present, date):
    """Add attendance record to the database"""
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO attendance (student_id, subject_id, is_present, date) VALUES (%s, %s, %s, %s) RETURNING attendance_id",
            (student_id, subject_id, is_present, date)
        )
        attendance_id = cursor.fetchone()[0]
        conn.commit()
        return attendance_id
    except Exception as e:
        conn.rollback()
        print(f"Error adding attendance: {e}")
        return None
    finally:
        conn.close()

def get_attendance_by_date(date, subject_id=None):
    """Get attendance records for a specific date and optional subject"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        query = """
            SELECT a.attendance_id, s.student_id, s.first_name, s.last_name, 
                   s.group_name, sub.subject_name, a.is_present
            FROM attendance a
            JOIN students s ON a.student_id = s.student_id
            JOIN subjects sub ON a.subject_id = sub.subject_id
            WHERE a.date = %s
        """
        params = [date]
        
        if subject_id:
            query += " AND a.subject_id = %s"
            params.append(subject_id)
            
        query += " ORDER BY s.group_name, s.last_name, s.first_name"
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting attendance: {e}")
        return []
    finally:
        conn.close()

def get_student_attendance(student_id, start_date=None, end_date=None):
    """Get attendance records for a specific student with optional date range"""
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        query = """
            SELECT a.attendance_id, s.subject_name, a.date, a.is_present
            FROM attendance a
            JOIN subjects s ON a.subject_id = s.subject_id
            WHERE a.student_id = %s
        """
        params = [student_id]
        
        if start_date:
            query += " AND a.date >= %s"
            params.append(start_date)
        
        if end_date:
            query += " AND a.date <= %s"
            params.append(end_date)
            
        query += " ORDER BY a.date DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error getting student attendance: {e}")
        return []
    finally:
        conn.close()