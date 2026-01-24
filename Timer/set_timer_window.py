import tkinter as tk
from tkinter import messagebox
import requests

def set_time():
    """Send the time to the timer API"""
    try:
        time_input = entry_time.get().strip()
        
        # Parse MM:SS format
        if ':' in time_input:
            parts = time_input.split(':')
            if len(parts) == 2:
                minutes = int(parts[0])
                seconds = int(parts[1])
            else:
                messagebox.showerror("Error", "Invalid format! Use MM:SS\nExample: 02:30")
                return
        else:
            # If no colon, treat as seconds
            minutes = 0
            seconds = int(time_input)
        
        total_seconds = minutes * 60 + seconds
        
        if total_seconds <= 0:
            messagebox.showerror("Error", "Time must be greater than 0")
            return
        
        # Send to API
        response = requests.post(
            'http://localhost:5000/api/set',
            json={'seconds': total_seconds},
            timeout=2
        )
        
        if response.status_code == 200:
            messagebox.showinfo("Success", f"Timer set to {minutes:02d}:{seconds:02d}")
            window.destroy()
        else:
            messagebox.showerror("Error", "Failed to set timer")
    except ValueError:
        messagebox.showerror("Error", "Invalid format! Use MM:SS\nExample: 02:30")
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Cannot connect to timer server.\nMake sure it's running!")

def quick_set(seconds):
    """Quick set buttons"""
    try:
        response = requests.post(
            'http://localhost:5000/api/set',
            json={'seconds': seconds},
            timeout=2
        )
        if response.status_code == 200:
            mins = seconds // 60
            secs = seconds % 60
            messagebox.showinfo("Success", f"Timer set to {mins:02d}:{secs:02d}")
            window.destroy()
    except:
        messagebox.showerror("Error", "Cannot connect to timer server")

# Create window
window = tk.Tk()
window.title("Set Timer")
window.geometry("300x250")
window.resizable(False, False)

# Center window
window.update_idletasks()
x = (window.winfo_screenwidth() // 2) - (300 // 2)
y = (window.winfo_screenheight() // 2) - (250 // 2)
window.geometry(f"+{x}+{y}")

# Title
title_label = tk.Label(window, text="⏱ Set Timer", font=("Segoe UI", 16, "bold"))
title_label.pack(pady=15)

# Instruction
instruction_label = tk.Label(window, text="Enter time (MM:SS):", font=("Segoe UI", 10))
instruction_label.pack(pady=5)

# Single input field
entry_time = tk.Entry(window, width=10, font=("Segoe UI", 18, "bold"), justify="center")
entry_time.pack(pady=10)
entry_time.insert(0, "02:00")
entry_time.select_range(0, tk.END)
entry_time.focus()

# Set button
set_button = tk.Button(window, text="Set Timer", command=set_time, 
                       font=("Segoe UI", 11), bg="#4CAF50", fg="white",
                       width=15, height=1, cursor="hand2")
set_button.pack(pady=10)

# Quick set buttons
quick_frame = tk.Frame(window)
quick_frame.pack(pady=10)

tk.Label(quick_frame, text="Quick Set:", font=("Segoe UI", 9)).pack()

buttons_frame = tk.Frame(quick_frame)
buttons_frame.pack(pady=5)

tk.Button(buttons_frame, text="1 Min", command=lambda: quick_set(60),
          width=8, bg="#2196F3", fg="white", cursor="hand2").grid(row=0, column=0, padx=3)
tk.Button(buttons_frame, text="2 Min", command=lambda: quick_set(120),
          width=8, bg="#2196F3", fg="white", cursor="hand2").grid(row=0, column=1, padx=3)
tk.Button(buttons_frame, text="5 Min", command=lambda: quick_set(300),
          width=8, bg="#2196F3", fg="white", cursor="hand2").grid(row=0, column=2, padx=3)

# Bind Enter key
window.bind('<Return>', lambda e: set_time())

# Keep window on top and bring to front
window.attributes('-topmost', True)
window.lift()
window.focus_force()

# Make sure window appears
window.after(100, lambda: window.focus_force())

window.mainloop()
