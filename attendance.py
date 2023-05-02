import sqlite3
import tkinter as tk
from   tkinter import messagebox
from   datetime import date


# Create a database connection
conn = sqlite3.connect('attendance.db')

# Create a table to store user information
conn.execute('''CREATE TABLE IF NOT EXISTS users
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             USERNAME TEXT NOT NULL,
             PASSWORD TEXT NOT NULL);''')

# Create a table to store attendance information
conn.execute('''CREATE TABLE IF NOT EXISTS attendance
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             USER_ID INTEGER NOT NULL,
             ATTENDANCE_DATE TEXT NOT NULL,
             FOREIGN KEY (USER_ID) REFERENCES users(ID));''')

# Create a GUI window
root = tk.Tk()
root.geometry('400x300')
root.title('Attendance System')

# Create a label for the username field
username_label = tk.Label(root, text='Username:')
username_label.pack()

# Create a username entry field
username_entry = tk.Entry(root)
username_entry.pack()

# Create a label for the password field
password_label = tk.Label(root, text='Password:')
password_label.pack()

# Create a password entry field
password_entry = tk.Entry(root, show='*')
password_entry.pack()

# Create a login button
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the user exists in the database
    cursor = conn.execute("SELECT * FROM users WHERE USERNAME = ? AND PASSWORD = ?", (username, password))
    row = cursor.fetchone()

    if row:
        messagebox.showinfo('Success', 'Login successful')
        mark_attendance(row[0])
    else:
        messagebox.showerror('Error', 'Invalid login credentials')

login_button = tk.Button(root, text='Login', command=login)
login_button.pack()
login_button.config(bg='#4CAF50', fg='white')

# Create a register button
def register():
    register_window = tk.Toplevel()
    register_window.geometry('400x300')
    register_window.title('Register')

    # Create a label for the username field
    username_label = tk.Label(register_window, text='Username:')
    username_label.pack()

    # Create a username entry field
    username_entry = tk.Entry(register_window)
    username_entry.pack()

    # Create a label for the password field
    password_label = tk.Label(register_window, text='Password:')
    password_label.pack()

    # Create a password entry field
    password_entry = tk.Entry(register_window, show='*')
    password_entry.pack()

    # Create a register button
    def register_user():
        username = username_entry.get()
        password = password_entry.get()

        # Check if the user already exists in the database
        cursor = conn.execute("SELECT * FROM users WHERE USERNAME = ?", (username,))
        row = cursor.fetchone()

        if row:
            messagebox.showerror('Error', 'User already exists')
        else:
            conn.execute("INSERT INTO users (USERNAME, PASSWORD) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo('Success', 'User registered successfully')
            register_window.destroy()

    register_button = tk.Button(register_window, text='Register', command=register_user)
    register_button.pack()
    register_button.config(bg='#4CAF50', fg='white')

    

register_button = tk.Button(root, text='Register', command=register)
register_button.pack()
register_button.config(bg='#4CAF50', fg='white')


# Create a function to mark attendance
def mark_attendance(user_id):
    attendance_window = tk.Toplevel()
    attendance_window.geometry('400x300')
    attendance_window_title = 'Mark Attendance - ' + date.today().strftime('%Y-%m-%d')
    attendance_window.title(attendance_window_title)

    # Create a mark attendance button
    def mark_attendance_date():
        attendance_date = date.today().strftime('%Y-%m-%d')
        #attendance_date_label.config(font=('Arial', 14))
        # Check if attendance for the user and date already exists
        cursor = conn.execute("SELECT * FROM attendance WHERE USER_ID = ? AND ATTENDANCE_DATE = ?", (user_id, attendance_date))
        row = cursor.fetchone()

        if row:
            messagebox.showerror('Error', 'Attendance already marked for this user and date')
        else:
            conn.execute("INSERT INTO attendance (USER_ID, ATTENDANCE_DATE) VALUES (?, ?)", (user_id, attendance_date))
            conn.commit()
            messagebox.showinfo('Success', 'Attendance marked successfully')
            attendance_window.destroy()

    mark_attendance_button = tk.Button(attendance_window, text='Mark Attendance', command=mark_attendance_date)
    mark_attendance_button.pack(padx=20, pady=20)
    mark_attendance_button.config(font=('Arial', 14)) 


username_label.config(font=('Arial', 14))
password_label.config(font=('Arial', 14))
login_button.config(font=('Arial', 14))
register_button.config(font=('Arial', 14))




username_label.pack(pady=10)
username_entry.pack(pady=5)
password_label.pack(pady=10)
password_entry.pack(pady=5)
login_button.pack(pady=20)
register_button.pack(pady=10)

root.configure(bg='blue')

root.mainloop()



