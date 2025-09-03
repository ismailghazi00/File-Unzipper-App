import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import threading

def unzip_files_gui():
    """
    This is the main function to create and run the GUI for the unzipping application.
    """
    root = tk.Tk()
    root.title("File Unzipper - Created by Ismail Ghazi")
    root.geometry("600x650")
    root.resizable(False, False)

    # Use a clean, modern font and dark theme
    root.option_add('*Font', 'Inter 10')
    root.configure(bg="#1a1a1a")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TFrame", background="#2a2a2a")
    style.configure("TLabel", background="#2a2a2a", foreground="#f0f0f0")
    style.configure("TButton", background="#4a4a4a", foreground="#f0f0f0", borderwidth=1, focusthickness=3, focuscolor="none")
    style.map("TButton", background=[('active', '#5a5a5a')])
    style.configure("TCheckbutton", background="#2a2a2a", foreground="#f0f0f0")
    style.configure("TEntry", fieldbackground="#3a3a3a", foreground="#f0f0f0", insertcolor="#f0f0f0")
    style.configure("TNotebook", background="#1a1a1a", borderwidth=0)
    style.configure("TNotebook.Tab", background="#4a4a4a", foreground="#f0f0f0", padding=[10, 5])
    style.map("TNotebook.Tab", background=[('selected', '#2a2a2a')], foreground=[('selected', '#ffffff')])
    style.configure("TProgressbar", thickness=15, troughcolor="#4a4a4a", background="#2563eb")

    # Define a frame for the main content with padding and a background color
    main_frame = ttk.Frame(root, padding=(20, 20, 20, 10))
    main_frame.pack(fill="both", expand=True)

    # Title label
    title_label = ttk.Label(main_frame, text="File Unzipper", font=("Inter", 18, "bold"), foreground="#ffffff")
    title_label.pack(pady=(0, 5))
    
    # Author label
    author_label = ttk.Label(main_frame, text="Created by Ismail Ghazi", font=("Inter", 10), foreground="#cccccc")
    author_label.pack(pady=(0, 20))

    # Path variables
    source_path = tk.StringVar()
    destination_path = tk.StringVar()
    
    # --- Source Folder Selection ---
    source_frame = ttk.Frame(main_frame)
    source_frame.pack(fill="x", pady=5)
    
    source_label = ttk.Label(source_frame, text="Source Folder (contains zip files):")
    source_label.pack(side="left", padx=(0, 5))
    
    source_entry = ttk.Entry(source_frame, textvariable=source_path, state='readonly')
    source_entry.pack(side="left", fill="x", expand=True)
    
    def browse_source():
        path = filedialog.askdirectory()
        if path:
            source_path.set(path)
    
    source_button = ttk.Button(source_frame, text="Select Folder", command=browse_source)
    source_button.pack(side="right", padx=(5, 0))

    # --- Destination Folder Selection ---
    dest_frame = ttk.Frame(main_frame)
    dest_frame.pack(fill="x", pady=5)
    
    dest_label = ttk.Label(dest_frame, text="Destination Folder (where to unzip):")
    dest_label.pack(side="left", padx=(0, 5))
    
    dest_entry = ttk.Entry(dest_frame, textvariable=destination_path, state='readonly')
    dest_entry.pack(side="left", fill="x", expand=True)
    
    def browse_destination():
        path = filedialog.askdirectory()
        if path:
            destination_path.set(path)
    
    dest_button = ttk.Button(dest_frame, text="Select Folder", command=browse_destination)
    dest_button.pack(side="right", padx=(5, 0))
    
    # --- Options Checkboxes ---
    options_frame = ttk.Frame(main_frame)
    options_frame.pack(fill="x", pady=10)
    
    delete_var = tk.IntVar()
    delete_checkbox = ttk.Checkbutton(options_frame, text="Delete original zip files after unzipping", variable=delete_var)
    delete_checkbox.pack(anchor="w")
    
    overwrite_var = tk.IntVar()
    overwrite_checkbox = ttk.Checkbutton(options_frame, text="Overwrite existing folders", variable=overwrite_var)
    overwrite_checkbox.pack(anchor="w")
    
    # --- Log Area ---
    log_label = ttk.Label(main_frame, text="Log:", font=("Inter", 10, "bold"))
    log_label.pack(anchor="w", pady=(10, 5))
    
    log_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15, bg="#3a3a3a", fg="#f0f0f0", insertbackground="#f0f0f0", relief="flat")
    log_text.pack(fill="both", expand=True)
    
    def add_log(message):
        log_text.insert(tk.END, message + "\n")
        log_text.see(tk.END)

    # --- Progress Bar ---
    progress_bar = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
    progress_bar.pack(fill="x", pady=(10, 0))

    # --- Unzip Button and Logic ---
    def start_unzip_thread():
        # Disable the button to prevent multiple clicks
        unzip_button.state(['disabled'])
        
        # Start the unzipping process in a separate thread
        thread = threading.Thread(target=unzip_logic)
        thread.start()

    def unzip_logic():
        source = source_path.get()
        destination = destination_path.get()
        delete_after = delete_var.get()
        overwrite_existing = overwrite_var.get()

        log_text.delete('1.0', tk.END)
        
        if not source or not destination:
            messagebox.showerror("Error", "Please select both a source and destination folder.")
            unzip_button.state(['!disabled'])
            return

        if not os.path.isdir(source):
            messagebox.showerror("Error", f"Source directory does not exist: {source}")
            unzip_button.state(['!disabled'])
            return
            
        if not os.path.isdir(destination):
            add_log(f"Destination folder does not exist. Creating: {destination}")
            try:
                os.makedirs(destination)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create destination folder: {e}")
                unzip_button.state(['!disabled'])
                return

        add_log("--- Starting Unzip Process ---")
        add_log(f"Source: {source}")
        add_log(f"Destination: {destination}")
        add_log(f"Delete after unzip: {'Yes' if delete_after else 'No'}")
        add_log(f"Overwrite existing: {'Yes' if overwrite_existing else 'No'}")
        add_log("")

        zip_files = [f for f in os.listdir(source) if f.endswith(".zip")]
        total_files = len(zip_files)
        progress_bar['maximum'] = total_files

        if total_files == 0:
            add_log("No .zip files found in the source directory.")
        else:
            for i, filename in enumerate(zip_files):
                zip_filepath = os.path.join(source, filename)
                folder_name = os.path.splitext(filename)[0]
                destination_folder_path = os.path.join(destination, folder_name)

                # Update the progress bar
                progress_bar['value'] = i + 1
                root.update_idletasks()

                if os.path.exists(destination_folder_path) and not overwrite_existing:
                    add_log(f"Warning: Folder '{folder_name}' already exists. Skipping due to overwrite setting.")
                    continue

                try:
                    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                        add_log(f"Unzipping '{filename}'...")
                        zip_ref.extractall(destination_folder_path)
                    add_log("Extraction complete.")
                    
                    if delete_after:
                        os.remove(zip_filepath)
                        add_log(f"Deleted original file: '{filename}'")

                except zipfile.BadZipFile:
                    add_log(f"Error: '{filename}' is not a valid zip file. Skipping.")
                except Exception as e:
                    add_log(f"An unexpected error occurred with '{filename}': {e}")
                finally:
                    add_log("")
        
        add_log(f"Successfully processed {total_files} zip files.")
        add_log("--- Process Complete ---")
        progress_bar['value'] = 0  # Reset progress bar
        unzip_button.state(['!disabled'])

    unzip_button = ttk.Button(main_frame, text="Unzip All Folders", command=start_unzip_thread)
    unzip_button.pack(fill="x", pady=(10, 0))

    root.mainloop()

if __name__ == "__main__":
    unzip_files_gui()
