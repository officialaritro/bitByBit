import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
from typing import Optional, Dict, List, Any
import json
import re

# You'll need to install yt-dlp with: pip install yt-dlp
import yt_dlp

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("bitByBit - YouTube Downloader")
        self.root.geometry("650x500")
        self.root.configure(bg="#FFF7D1")
        icon_path = os.path.join(os.path.dirname(__file__), "bitbybit.png")

        try:
            icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, icon)
        except Exception as e:
            print(f"Could not set icon: {e}")


        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure("TButton", background="#6A42C2", foreground="#ffffff")
        style.map("TButton", background=[('active', '#8B5DFF')])

        self.main_frame = tk.Frame(root, bg="#FFF7D1", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            self.main_frame,
            text="bitByBit - YouTube Downloader",
            font=("Helvetica", 25, "bold"),
            bg="#FFF7D1",
            fg="#6A42C2"
        )
        title_label.pack(pady=(0, 20))

        url_frame = tk.Frame(self.main_frame, bg="#FFF7D1")
        url_frame.pack(fill=tk.X, pady=10)

        url_label = tk.Label(
            url_frame,
            text="Enter YouTube URL:",
            font=("Helvetica", 10),
            bg="#FFF7D1",
            fg="#563A9C"
        )
        url_label.pack(anchor="w", pady=(20, 5))

        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=70)
        url_entry.pack(fill=tk.X, pady=5)

        buttons_frame = tk.Frame(self.main_frame, bg="#FFF7D1")
        buttons_frame.pack(fill=tk.X, pady=10)

        self.fetch_button = ttk.Button(
            buttons_frame,
            text="Fetch Video Info",
            command=self.fetch_video_info
        )
        self.fetch_button.pack(side=tk.LEFT, padx=5)

        self.info_frame = tk.Frame(self.main_frame, bg="#FFF7D1")
        self.info_frame.pack(fill=tk.BOTH, expand=True)
        self.info_frame.pack_forget()

        self.title_var = tk.StringVar()
        title_display = tk.Label(
            self.info_frame,
            textvariable=self.title_var,
            font=("Helvetica", 10, "bold"),
            bg="#FFF7D1",
            fg="#6A42C2",
            wraplength=600,
            justify="left"
        )
        title_display.pack(anchor="w", pady=5)

        self.details_var = tk.StringVar()
        details_display = tk.Label(
            self.info_frame,
            textvariable=self.details_var,
            font=("Helvetica", 9),
            bg="#FFF7D1",
            fg="#000000",
            wraplength=600,
            justify="left"
        )
        details_display.pack(anchor="w", pady=5)

        formats_frame = tk.Frame(self.info_frame, bg="#FFF7D1")
        formats_frame.pack(fill=tk.X, pady=10)

        formats_label = tk.Label(
            formats_frame,
            text="Select Format:",
            font=("Helvetica", 10),
            bg="#FFF7D1",
            fg="#563A9C"
        )
        formats_label.pack(anchor="w")

        columns = ("format_id", "extension", "resolution", "filesize", "note")
        self.formats_tree = ttk.Treeview(
            formats_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.formats_tree.heading("format_id", text="Format ID")
        self.formats_tree.heading("extension", text="Format")
        self.formats_tree.heading("resolution", text="Resolution")
        self.formats_tree.heading("filesize", text="File Size")
        self.formats_tree.heading("note", text="Notes")

        self.formats_tree.column("format_id", width=70)
        self.formats_tree.column("extension", width=70)
        self.formats_tree.column("resolution", width=100)
        self.formats_tree.column("filesize", width=100)
        self.formats_tree.column("note", width=250)

        tree_scroll = ttk.Scrollbar(formats_frame, orient="vertical", command=self.formats_tree.yview)
        self.formats_tree.configure(yscrollcommand=tree_scroll.set)

        self.formats_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.formats_tree.bind("<<TreeviewSelect>>", self.on_format_select)

        output_frame = tk.Frame(self.info_frame, bg="#FFF7D1")
        output_frame.pack(fill=tk.X, pady=10)

        output_label = tk.Label(
            output_frame,
            text="Save to:",
            font=("Helvetica", 10),
            bg="#FFF7D1",
            fg="#563A9C"
        )
        output_label.pack(side=tk.LEFT)

        self.output_var = tk.StringVar()
        self.output_var.set(os.path.join(os.path.expanduser("~"), "Downloads"))

        output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=50)
        output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        browse_button = ttk.Button(
            output_frame,
            text="Browse",
            command=self.browse_directory
        )
        browse_button.pack(side=tk.LEFT)

        progress_frame = tk.Frame(self.info_frame, bg="#FFF7D1")
        progress_frame.pack(fill=tk.X, pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            length=100,
            mode="determinate"
        )
        self.progress_bar.pack(fill=tk.X)

        self.status_var = tk.StringVar()
        self.status_var.set("Ready")

        status_label = tk.Label(
            progress_frame,
            textvariable=self.status_var,
            bg="#FFF7D1",
            fg="#6A42C2"
        )
        status_label.pack(anchor="w", pady=5)

        self.download_button = ttk.Button(
            self.info_frame,
            text="Download",
            command=self.start_download,
            state="disabled"
        )
        self.download_button.pack(pady=10)
        self.video_info = None
        self.selected_format_id = None

        self.log_frame = tk.Frame(self.main_frame, bg="#FFF7D1")
        self.log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_frame.pack_forget()

        log_label = tk.Label(
            self.log_frame,
            text="Download Log:",
            font=("Helvetica", 10),
            bg="#FFF7D1",
            fg="#563A9C"
        )
        log_label.pack(anchor="w")
        
        # Log text widget
        self.log_text = tk.Text(self.log_frame, height=8, width=70, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        log_scroll = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def browse_directory(self):
        """Open directory browser dialog"""
        directory = filedialog.askdirectory(initialdir=self.output_var.get())
        if directory:
            self.output_var.set(directory)
            
    def fetch_video_info(self):
        """Fetch video information from the URL"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
            
        self.status_var.set("Fetching video information...")
        self.fetch_button.config(state="disabled")
        
        self.formats_tree.delete(*self.formats_tree.get_children())
        self.log_text.delete(1.0, tk.END)
        
        # Start a thread for fetching info
        threading.Thread(
            target=self._fetch_info_thread,
            args=(url,),
            daemon=True
        ).start()
            
    def _fetch_info_thread(self, url):
        """Background thread for fetching video info"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'no_color': True,
                'extract_flat': True,
                'skip_download': True,
                'force_generic_extractor': False
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.video_info = ydl.extract_info(url, download=False)
            self.root.after(0, self._update_ui_with_info)
                
        except Exception as e:
            error_message = str(e)
            self.root.after(0, lambda: self._show_error(error_message))
            self.root.after(0, lambda: self.fetch_button.config(state="normal"))
    
    def _format_filesize(self, size_bytes):
        """Format file size from bytes to human-readable form"""
        if size_bytes is None:
            return "Unknown"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0 or unit == 'GB':
                break
            size_bytes /= 1024.0
                
        return f"{size_bytes:.2f} {unit}"
            
    def _update_ui_with_info(self):
        """Update UI with fetched video information"""
        if not self.video_info:
            self._show_error("Failed to extract video information")
            self.fetch_button.config(state="normal")
            return
            
      
        self.title_var.set(f"Title: {self.video_info.get('title', 'Unknown')}")
        
        channel = self.video_info.get('uploader', 'Unknown')
        duration = self._format_duration(self.video_info.get('duration', 0))
        details = f"Channel: {channel} | Duration: {duration}"
        self.details_var.set(details)
        
        
        formats = self.video_info.get('formats', [])
        if not formats:
            self._show_error("No download formats available")
            self.fetch_button.config(state="normal")
            return
            
        try:
            
            sorted_formats = self._prepare_formats(formats)
                
            
            for fmt in sorted_formats:
                format_id = fmt.get('format_id', 'N/A')
                extension = fmt.get('ext', 'N/A')
                
                resolution = 'audio only'
                if fmt.get('height'):
                    resolution = f"{fmt.get('height', 'N/A')}p"
                    if fmt.get('fps'):
                        resolution += f" {fmt.get('fps')}fps"
                        
                filesize = self._format_filesize(fmt.get('filesize'))
                
                notes = []
                if fmt.get('vcodec') == 'none':
                    notes.append('audio only')
                if fmt.get('acodec') == 'none':
                    notes.append('video only')
                if 'DASH' in fmt.get('format', ''):
                    notes.append('DASH')
                    
                note_text = ", ".join(notes) if notes else "Normal"
                    
                self.formats_tree.insert("", tk.END, values=(
                    format_id, extension, resolution, filesize, note_text
                ))
                
            
            self.info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
            self.log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
                
            
            self.fetch_button.config(state="normal")
            self.status_var.set("Ready to download. Select a format.")
        except Exception as e:
            self._show_error(f"Error processing video formats: {str(e)}")
            self.fetch_button.config(state="normal")
    
    def _prepare_formats(self, formats):
        """Filter and sort formats for better display"""
        
        useful_formats = []
        
        for fmt in formats:
            if not fmt.get('format_id'):
                continue
            useful_formats.append(fmt)
            
        
        def sort_key(fmt):
            
            score = 0
            
            
            if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                score += 10000
                
            
            height = fmt.get('height')
            if height is not None and isinstance(height, (int, float)):
                score += int(height)
            
            
            fps = fmt.get('fps')
            if fps is not None and isinstance(fps, (int, float)):
                score += fps / 100
                
            
            abr = fmt.get('abr')
            if abr is not None and isinstance(abr, (int, float)):
                score += abr / 1000
                
            return score
                
        return sorted(useful_formats, key=sort_key, reverse=True)
        
    def _format_duration(self, seconds):
        """Format duration in seconds to HH:MM:SS"""
        if not seconds:
            return "Unknown"
            
        mins, secs = divmod(int(seconds), 60)
        hours, mins = divmod(mins, 60)
            
        if hours > 0:
            return f"{hours}:{mins:02d}:{secs:02d}"
        else:
            return f"{mins}:{secs:02d}"
        
    def on_format_select(self, event):
        """Handle format selection from treeview"""
        selected_items = self.formats_tree.selection()
        if not selected_items:
            self.selected_format_id = None
            self.download_button.config(state="disabled")
            return
            
        # Get the format_id from the selected item
        item = selected_items[0]  
        values = self.formats_tree.item(item, "values")
        if values:
            self.selected_format_id = values[0]  
            self.download_button.config(state="normal")
        
    def _show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        self.status_var.set("Error occurred")
        
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, f"ERROR: {message}\n")
            self.log_text.see(tk.END)  
        
    def start_download(self):
        """Start the download process"""
        if not self.video_info or not self.selected_format_id:
            messagebox.showerror("Error", "Please select a format to download")
            return
            
        output_dir = self.output_var.get()
        if not os.path.isdir(output_dir):
            messagebox.showerror("Error", "Invalid download directory")
            return
            
        self.download_button.config(state="disabled")
        self.fetch_button.config(state="disabled")        
        self.status_var.set("Starting download...")
        self.progress_var.set(0)
        
        threading.Thread(
            target=self._download_thread,
            args=(self.video_info, self.selected_format_id, output_dir),
            daemon=True
        ).start()
        
    def _download_thread(self, video_info, format_id, output_dir):
        """Background thread for downloading"""
        try:

            ydl_opts = {
                'format': format_id,
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'quiet': False,
                'no_warnings': False,
                'verbose': True,
                'logger': MyLogger(self),  
                'nocheckcertificate': True,  
                'ignoreerrors': False 
            }
            
            self.root.after(0, lambda: self._append_to_log(
                f"Starting download of format {format_id} to {output_dir}..."
            ))
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_info['webpage_url']])
                
            self.root.after(0, self._download_complete)
                
        except Exception as e:
            error_message = str(e)
            self.root.after(0, lambda: self._show_error(error_message))
            self.root.after(0, self._reset_ui_after_download)
    
    def _append_to_log(self, message):
        """Append message to log text widget"""
        if hasattr(self, 'log_text'):
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)  
    
    def _progress_hook(self, d):
        """Handle download progress updates"""
        if d['status'] == 'downloading':
            # Update progress bar and status
            p = d.get('_percent_str', '0%').strip()
            eta = d.get('_eta_str', 'unknown').strip()
            speed = d.get('_speed_str', 'unknown').strip()
            
            try:
                p_float = float(p.replace('%', ''))
                self.root.after(0, lambda: self.progress_var.set(p_float))
            except:
                pass
                
            status = f"Downloading: {p} | Speed: {speed} | ETA: {eta}"
            self.root.after(0, lambda: self.status_var.set(status))
            
        elif d['status'] == 'finished':
            self.root.after(0, lambda: self.status_var.set("Download finished, processing file..."))
            self.root.after(0, lambda: self.progress_var.set(100))
    
    def _download_complete(self):
        """Handle download completion"""
        messagebox.showinfo("Success", "Download completed successfully!")
        self._reset_ui_after_download()
        
    def _reset_ui_after_download(self):
        """Reset UI after download completes or fails"""
        self.download_button.config(state="normal")
        self.fetch_button.config(state="normal")
        self.status_var.set("Ready")
        
class MyLogger:
    """Custom logger for yt-dlp that updates the UI"""
    def __init__(self, app):
        self.app = app
        
    def debug(self, msg):
        self._log_message(msg)
        
    def info(self, msg):
        self._log_message(msg)
        
    def warning(self, msg):
        self._log_message(f"WARNING: {msg}")
        
    def error(self, msg):
        self._log_message(f"ERROR: {msg}")
        
    def _log_message(self, msg):
        # Update the log in the main thread
        if msg and isinstance(msg, str):
            self.app.root.after(0, lambda: self._append_to_log(msg))
            
    def _append_to_log(self, message):
        """Append message to log text widget"""
        self.app.log_text.insert(tk.END, message + "\n")
        self.app.log_text.see(tk.END)  

if __name__ == "__main__":
    
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')
        
    # Create app
    app = YouTubeDownloader(root)
    root.mainloop()