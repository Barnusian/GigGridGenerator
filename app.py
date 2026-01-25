import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from generator import generate_html_from_csv


class GigGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gig Grid HTML Generator")
        self.root.resizable(False, False)

        self.csv_path = None

        self.build_ui()

    def build_ui(self):
        padding = {"padx": 10, "pady": 8}

        # Choose CSV button
        self.choose_button = tk.Button(
            self.root,
            text="Choose CSV",
            width=20,
            command=self.choose_csv
        )
        self.choose_button.grid(row=0, column=0, **padding)

        # CSV path display (read-only)
        self.csv_var = tk.StringVar()
        self.csv_entry = tk.Entry(
            self.root,
            textvariable=self.csv_var,
            width=50,
            state="readonly"
        )
        self.csv_entry.grid(row=1, column=0, **padding)

        # Generate HTML button (disabled until CSV chosen)
        self.generate_button = tk.Button(
            self.root,
            text="Generate HTML",
            width=20,
            state="disabled",
            command=self.generate_html
        )
        self.generate_button.grid(row=2, column=0, **padding)

    def choose_csv(self):
        path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv")]
        )

        if not path:
            return

        self.csv_path = Path(path)
        self.csv_var.set(str(self.csv_path))
        self.generate_button.config(state="normal")

    def generate_html(self):
        if not self.csv_path:
            return

        try:
            html = generate_html_from_csv(str(self.csv_path))
        except ValueError as e:
            messagebox.showerror("Invalid CSV", str(e))
            return
        except Exception as e:
            messagebox.showerror(
                "Unexpected Error",
                f"Something went wrong:\n\n{e}"
            )
            return

        save_path = filedialog.asksaveasfilename(
            title="Save HTML File",
            defaultextension=".html",
            filetypes=[("HTML files", "*.html")],
            initialfile="gig_block.html"
        )

        if not save_path:
            return

        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(html)
        except Exception as e:
            messagebox.showerror(
                "File Error",
                f"Could not write file:\n\n{e}"
            )
            return

        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(html)
        self.root.update()

        messagebox.showinfo(
            "Success",
            "HTML generated, saved to file, and copied to clipboard."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = GigGridApp(root)
    root.mainloop()
