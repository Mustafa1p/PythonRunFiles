import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os

class PythonRunner:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Script Runner")
        self.selected_files = []
        self.run_count = 0
        self.running = False

        self.file_label = tk.Label(root, text="Selected Files: None")
        self.file_label.pack()

        self.select_button = tk.Button(root, text="Select Python Files", command=self.select_files)
        self.select_button.pack()

        self.run_button = tk.Button(root, text="Run", command=self.run_scripts)
        self.run_button.pack()

        self.stats_label = tk.Label(root, text="Run Count: 0")
        self.stats_label.pack()

    def select_files(self):
        self.selected_files = filedialog.askopenfilenames(filetypes=[("Python files", "*.py")])
        if self.selected_files:
            self.file_label.config(text=f"Selected Files: {', '.join(self.selected_files)}")

    def run_scripts(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected!")
            return

        if self.running:
            messagebox.showerror("Error", "Scripts are already running!")
            return

        self.run_count += len(self.selected_files)
        self.stats_label.config(text=f"Run Count: {self.run_count}")

        for file in self.selected_files:
            threading.Thread(target=self.run_script_in_thread, args=(file,)).start()

    def run_script_in_thread(self, file):
        try:
            subprocess.run(['python', file], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error running {os.path.basename(file)}: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Exception while running {os.path.basename(file)}: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonRunner(root)
    root.mainloop()
