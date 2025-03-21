import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

root = tk.Tk()
root.title("LSDJ Wavetable Import GUI")

# Define the missing variables after initializing tkinter
source_File = tk.StringVar()
wavetable_entry = tk.StringVar()
output_entry = tk.StringVar()

def select_source_file():
    source_file = filedialog.askopenfilename(title="Select source .lsdsng file", filetypes=[("LSDSNG files", "*.lsdsng")])
    if not source_file.lower().endswith('.lsdsng'):
        messagebox.showerror("Error", "Invalid file type. Please select a .lsdsng file.")
        return
    source_File.set(source_file)  # Set the value of source_File to the selected file path
    source_label.config(text=os.path.join(os.path.basename(os.path.dirname(source_file)), os.path.basename(source_file)))

def select_wavetable_file():
    wavetable_file = filedialog.askopenfilename(title="Select wavetable .snt file", filetypes=[("SNT files", "*.snt")])
    if not wavetable_file.lower().endswith('.snt'):
        messagebox.showerror("Error", "Invalid file type. Please select a .snt file.")
        return
    wavetable_entry.set(wavetable_file)  # Set the value of wavetable_entry to the selected file path
    wavetable_label.config(text=os.path.join(os.path.basename(os.path.dirname(wavetable_file)), os.path.basename(wavetable_file)))

def select_output_file():
    output_file = filedialog.asksaveasfilename(title="Select output .lsdsng file", defaultextension=".lsdsng", filetypes=[("LSDSNG files", "*.lsdsng")])
    if not output_file.lower().endswith('.lsdsng'):
        messagebox.showerror("Error", "Invalid file type. Please select a .lsdsng file.")
        return
    output_entry.set(output_file)  # Set the value of output_entry to the selected file path
    output_label.config(text=os.path.join(os.path.basename(os.path.dirname(output_file)), os.path.basename(output_file)))

def update_values(*args):
    option = option_var.get()
    if option == "-s":
        value_combo["values"] = [f"{i:X}" for i in range(16)]
    else:
        value_combo["values"] = [f"{i:02X}" for i in range(256)]
    value_combo.current(0)

def import_wavetable():
    source_file = source_File.get()
    wavetable_file = wavetable_entry.get()
    output_file = output_entry.get()

    option = option_var.get()
    value = value_combo.get()
    verbose = verbose_var.get()
    zero = zero_var.get()
    force = force_var.get()
    decimal = decimal_var.get()

    command = ["lsdj-wavetable-import", source_file, wavetable_file, "-o", output_file]

    if verbose:
        command.append("-v")
    if zero:
        command.append("-0")
    if force:
        command.append("-f")
    if decimal:
        command.append("-d")
    if option and value:
        command.extend([option, value])

    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "Wavetable imported successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "An error occurred while importing the wavetable.")

verbose_var = tk.BooleanVar()
zero_var = tk.BooleanVar()
force_var = tk.BooleanVar()
decimal_var = tk.BooleanVar()
option_var = tk.StringVar()

root.grid_columnconfigure(1, weight=1)

value_label = tk.Label(root, text="Patch to synth 0-F / Wavetable index")
value_label.grid(row=2, column=0, sticky="w", columnspan=100)
value_combo = ttk.Combobox(root)
value_combo.grid(row=3, column=0, sticky="w", columnspan=4)

option_radio1 = tk.Radiobutton(root, text="Synth", variable=option_var, value="-s")
option_radio1.grid(row=1, column=0, sticky="w")
option_radio2 = tk.Radiobutton(root, text="Index", variable=option_var, value="-i")
option_radio2.grid(row=1, column=1, sticky="w")

verbose_check = tk.Checkbutton(root, text="Verbose output during import", variable=verbose_var)
verbose_check.grid(row=4, column=0, columnspan=4, sticky="w")
zero_check = tk.Checkbutton(root, text="Pad the synth with empty wavetables if the .snt file < 256 bytes",
                            variable=zero_var)
zero_check.grid(row=5, column=0, columnspan=4, sticky="w")
force_check = tk.Checkbutton(root, text="Force writing the wavetables, even though non-default data may be in them",
                             variable=force_var)
force_check.grid(row=6, column=0, columnspan=4, sticky="w")
decimal_check = tk.Checkbutton(root, text="Is the number for --index or --synth a decimal (instead of hex)?",
                               variable=decimal_var)
decimal_check.grid(row=7, column=0, columnspan=4, sticky="w")

source_button = tk.Button(root, text="Load .lsdsng file", command=select_source_file, width=20)
source_button.grid(row=0, column=0, sticky="w")
source_label = tk.Label(root)
source_label.grid(row=10, column=1, sticky="w", columnspan=100)

wavetable_button = tk.Button(root, text="Load .snt file", command=select_wavetable_file, width=20)
wavetable_button.grid(row=0, column=2, sticky="w")
wavetable_label = tk.Label(root)
wavetable_label.grid(row=11, column=1, sticky="w", columnspan=100)

output_button = tk.Button(root, text="Save to .lsdsng file", command=select_output_file, width=20)
output_button.grid(row=0, column=1, sticky="w")
output_label = tk.Label(root)
output_label.grid(row=12, column=1, sticky="w", columnspan=100)

# Add labels to display the selected file paths
Source_File_Label = tk.Label(root, text="Loaded .lsdsng:")
Source_File_Label.grid(row=10, column=0, sticky="w")

wavetable_output_label = tk.Label(root, text="Loaded Wavetable:")
wavetable_output_label.grid(row=12, column=0, sticky="w")

output_output_label = tk.Label(root, text="Patched .lsdsng:")
output_output_label.grid(row=11, column=0, sticky="w")

import_button = tk.Button(root, text="Import Wavetable", command=import_wavetable, width=15)
import_button.grid(row=9, column=0, sticky="w")

option_var.trace("w", update_values)
option_var.set("-s")

root.mainloop()
