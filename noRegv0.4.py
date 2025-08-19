import tkinter as tk
from tkinter import scrolledtext, messagebox

class StringManipulatorApp:
    """
    A simple desktop application for manipulating strings based on user-defined rules.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("String Manipulator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Configure grid to be responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        """
        Creates and places all the GUI widgets in the application window.
        """
        # --- Header ---
        header_frame = tk.Frame(self.root, bg="#3498db")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        header_label = tk.Label(
            header_frame,
            text="String Manipulator",
            font=("Helvetica", 20, "bold"),
            fg="white",
            bg="#3498db",
            pady=10
        )
        header_label.pack()

        # --- Input and Rules Section ---
        input_frame = tk.Frame(self.root, bg="#ffffff", padx=15, pady=15)
        input_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_rowconfigure(1, weight=1)
        input_frame.grid_rowconfigure(3, weight=1)

        input_label = tk.Label(input_frame, text="Input String", font=("Helvetica", 12, "bold"), bg="white")
        input_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10, font=("Courier", 10), bd=1, relief="solid")
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.input_text.insert(tk.END, "Admin\nUser\nViewer_1")

        rules_label = tk.Label(input_frame, text="Rules", font=("Helvetica", 12, "bold"), bg="white")
        rules_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.rules_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=15, font=("Courier", 10), bd=1, relief="solid")
        self.rules_text.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        default_rules = (
            "// Write your rules here, one per line.\n"
            "// Available rules:\n"
            "// remove:chars (e.g., remove:o,r,d)\n"
            "// replace:old,new (e.g., replace:Hello,Goodbye)\n"
            "// add-prefix:text (e.g., add-prefix:START_)\n"
            "// add-suffix:text (e.g., add-suffix:_END)\n"
            "// to-upper\n"
            "// to-lower\n\n"
            "add-prefix:slack_\n"
            "add-suffix:_grp\n"
            "remove:_\n"
        )
        self.rules_text.insert(tk.END, default_rules)

        # --- Buttons ---
        button_frame = tk.Frame(input_frame, bg="#ffffff")
        button_frame.grid(row=4, column=0, sticky="e", pady=(5, 0))
        
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_all, bg="#e74c3c", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
        clear_button.pack(side=tk.LEFT, padx=5)

        apply_button = tk.Button(button_frame, text="Apply Rules", command=self.apply_rules, bg="#2ecc71", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
        apply_button.pack(side=tk.LEFT, padx=5)


        # --- Output Section ---
        output_frame = tk.Frame(self.root, bg="#ffffff", padx=15, pady=15)
        output_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)
        
        output_label = tk.Label(output_frame, text="Output", font=("Helvetica", 12, "bold"), bg="white")
        output_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10, font=("Courier", 10), bd=1, relief="solid", state=tk.DISABLED)
        self.output_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        # --- Copy Button ---
        copy_button = tk.Button(output_frame, text="Copy Output", command=self.copy_output, bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
        copy_button.grid(row=2, column=0, sticky="e", pady=(5, 0))


    def apply_rules(self):
        """
        Reads the input string and rules, applies the transformations, and updates the output text area.
        """
        input_string = self.input_text.get("1.0", tk.END).strip()
        rules_string = self.rules_text.get("1.0", tk.END).strip()
        
        # Split the input string into individual lines
        input_lines = input_string.split('\n')
        output_lines = []
        
        # Clear previous output
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        for current_string in input_lines:
            # Re-read rules for each line to ensure they are all applied
            for line in rules_string.split('\n'):
                if not line.strip() or line.strip().startswith('//'):
                    continue

                try:
                    colon_index = line.find(':')
                    if colon_index != -1:
                        command = line[:colon_index].strip().lower()
                        args = line[colon_index + 1:]

                        if command == 'remove':
                            for char_to_remove in args.split(','):
                                current_string = current_string.replace(char_to_remove.strip(), '')
                        elif command == 'replace':
                            old, new = args.split(',', 1)
                            current_string = current_string.replace(old, new)
                        elif command == 'add-prefix':
                            current_string = args + current_string
                        elif command == 'add-suffix':
                            current_string += args
                        else:
                            messagebox.showwarning("Unknown Rule", f"The rule '{command}' is not recognized.")
                    else:
                        command = line.strip().lower()
                        if command == 'to-upper':
                            current_string = current_string.upper()
                        elif command == 'to-lower':
                            current_string = current_string.lower()
                        else:
                            messagebox.showwarning("Unknown Rule", f"The rule '{command}' is not recognized.")
                except Exception as e:
                    messagebox.showerror("Rule Error", f"An error occurred while processing rule '{line}': {e}")
            
            output_lines.append(current_string)
                
        self.output_text.insert(tk.END, '\n'.join(output_lines))
        self.output_text.config(state=tk.DISABLED)

    def clear_all(self):
        """
        Clears all three text areas.
        """
        self.input_text.delete("1.0", tk.END)
        self.rules_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

    def copy_output(self):
        """
        Copies the content of the output text area to the clipboard.
        """
        try:
            output_content = self.output_text.get("1.0", tk.END).strip()
            if output_content:
                self.root.clipboard_clear()
                self.root.clipboard_append(output_content)
                messagebox.showinfo("Copied!", "Output copied to clipboard.")
            else:
                messagebox.showwarning("Copy Failed", "Output area is empty.")
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to copy to clipboard: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StringManipulatorApp(root)
    root.mainloop()
