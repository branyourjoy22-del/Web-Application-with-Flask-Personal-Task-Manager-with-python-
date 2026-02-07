"""Tkinter window with File menu (Open, Save, Exit)."""
import tkinter as tk
from tkinter import filedialog, messagebox


def open_file():
    """Open a file: dialog returns path or '' if cancelled. Read file and put content in the Text."""
    path = filedialog.askopenfilename(
        title="Open file",
        filetypes=[("All files", "*.*"), ("Text files", "*.txt")],
    )
    if not path:
        return
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        # Delete everything from start (1.0) to end, then insert file content
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, content)
        app.title(f"File menu demo - {path}")
    except OSError as e:
        messagebox.showerror("Open error", str(e))


def save_file():
    """Save: dialog to choose path. Get all text from 1.0 to END and write to file."""
    path = filedialog.asksaveasfilename(
        title="Save file",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if not path:
        return
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text_area.get("1.0", tk.END))
        app.title(f"File menu demo - {path}")
        messagebox.showinfo("Saved", f"Saved to {path}")
    except OSError as e:
        messagebox.showerror("Save error", str(e))


# Main window: tk.Tk; we adjust its title and size
app = tk.Tk()
app.title("File menu demo")
app.geometry("600x400")

# Menubar and File submenu with Open, Save, Exit
menubar = tk.Menu(app)
app.config(menu=menubar)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=app.quit)

# tk.Text is a multi-line text widget; pack it to fill both (expand=True, fill=both)
text_area = tk.Text(app, wrap=tk.WORD, padx=8, pady=8)
text_area.pack(expand=True, fill=tk.BOTH)

# mainloop() starts the Tkinter event loop (essential for the window to display and interact)
app.mainloop()
