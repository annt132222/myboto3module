import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from myyboto3module import uploader

class FileUploadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Upload GUI")
        self.root.geometry("700x500")
        
        self.file_paths = []
        self.active_uploads = 0
        self.uploader = None

        self.label = tk.Label(root, text="Select files to upload:")
        self.label.pack(pady=10)
        
        self.file_listbox = tk.Listbox(root, width=60, height=5)
        self.file_listbox.pack(pady=5)
        
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_files)
        self.browse_button.pack(pady=5)
        
        self.upload_button = tk.Button(root, text="Upload", command=self.start_upload)
        self.upload_button.pack(pady=5)

        self.progress_bars = {}
        self.status_labels = {}  

        self.retry_button = tk.Button(root, text="Retry", command=self.start_upload)
        self.retry_button.pack(pady=5)
        self.retry_button.pack_forget()
        
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)
    
    def browse_files(self):
        files = filedialog.askopenfilenames()
        if files:
            self.file_paths = files
            self.file_listbox.delete(0, tk.END)
            self.progress_bars.clear()
            self.status_labels.clear()
            for file in files:
                self.file_listbox.insert(tk.END, file)
                progress_bar = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=300, mode='determinate')
                progress_bar.pack(pady=2)
                self.progress_bars[file] = progress_bar

                status_label = tk.Label(self.root, text="0% completed")
                status_label.pack(pady=2)
                self.status_labels[file] = status_label

    def update_progress(self, file_path, progress_value):
        def _update():
            if file_path in self.status_labels:
                status_text = f"Uploading {file_path}: {progress_value:.2f}% completed"
                self.status_labels[file_path].config(text=status_text)
            if file_path in self.progress_bars:
                self.progress_bars[file_path]['value'] = progress_value
        self.root.after(0, _update)

    def start_upload(self):
        if not self.file_paths:
            messagebox.showwarning("Warning", "Please select files first!")
            return
        
        self.upload_button.config(state=tk.DISABLED)
        self.retry_button.pack_forget()
        self.active_uploads = len(self.file_paths)
        
        uploaders = uploader.UpLoader(self.file_paths, self.update_progress, self.upload_complete)
        uploaders.upload_files()

    def upload_complete(self, file_path):
        self.active_uploads -= 1
        if self.active_uploads == 0:
            self.upload_button.config(state=tk.NORMAL)
            messagebox.showinfo(title="Progress",message="All file have been uploaded!")
if __name__ == "__main__":
    root = tk.Tk()
    app = FileUploadApp(root)
    root.mainloop()
