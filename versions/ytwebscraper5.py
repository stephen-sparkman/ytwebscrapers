import customtkinter as ctk
import os
import threading
import subprocess
import json
from tkinter import filedialog, messagebox

class YouTubeDownloaderGUI:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("YouTube Downloader")
        self.root.geometry("700x600")
        
        # Default download path
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Create UI elements
        self.create_widgets()
        
        # Check if yt-dlp is installed
        self.check_ytdlp()
        
    def check_ytdlp(self):
        """Check if yt-dlp is installed"""
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            version = result.stdout.strip()
            self.log_status(f"✅ yt-dlp version {version} detected")
            
            # Also check ffmpeg
            if self.check_ffmpeg():
                self.log_status("✅ ffmpeg detected (MP3 conversion available)")
            else:
                self.log_status("⚠️ ffmpeg not found (audio will save in original format)")
                self.log_status("   To enable MP3 conversion: brew install ffmpeg")
                
        except FileNotFoundError:
            self.log_status("⚠️ yt-dlp not found. Installing...")
            self.install_ytdlp()
        except Exception as e:
            self.log_status(f"⚠️ Could not verify yt-dlp: {e}")
    
    def install_ytdlp(self):
        """Install yt-dlp using pip"""
        try:
            self.log_status("Installing yt-dlp via pip...")
            subprocess.run(['pip', 'install', '-U', 'yt-dlp'], 
                         check=True, capture_output=True)
            self.log_status("✅ yt-dlp installed successfully!")
        except Exception as e:
            error_msg = f"Failed to install yt-dlp: {e}\n\nPlease install manually:\npip install -U yt-dlp"
            self.log_status(f"❌ {error_msg}")
            messagebox.showerror("Installation Error", error_msg)
        
    def create_widgets(self):
        # Title
        title_label = ctk.CTkLabel(
            self.root, 
            text="🎥 YouTube Downloader", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(pady=10, padx=40, fill="both", expand=True)
        
        # Info label
        info_label = ctk.CTkLabel(
            main_frame,
            text="Using yt-dlp (no tokens needed!)",
            font=ctk.CTkFont(size=11),
            text_color="green"
        )
        info_label.pack(pady=5)
        
        # Download type selection
        type_label = ctk.CTkLabel(
            main_frame, 
            text="Select Download Type:", 
            font=ctk.CTkFont(size=14)
        )
        type_label.pack(pady=(20, 5))
        
        self.download_type = ctk.CTkOptionMenu(
            main_frame,
            values=["Single Video", "Playlist", "Channel", "Audio Only", "Best Quality"],
            font=ctk.CTkFont(size=13),
            width=300
        )
        self.download_type.pack(pady=5)
        self.download_type.set("Single Video")
        
        # URL input
        url_label = ctk.CTkLabel(
            main_frame, 
            text="Enter URL:", 
            font=ctk.CTkFont(size=14)
        )
        url_label.pack(pady=(20, 5))
        
        self.url_entry = ctk.CTkEntry(
            main_frame, 
            placeholder_text="https://www.youtube.com/watch?v=...",
            width=500,
            height=40,
            font=ctk.CTkFont(size=13)
        )
        self.url_entry.pack(pady=5)
        
        # Output folder selection
        folder_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        folder_frame.pack(pady=15)
        
        self.folder_label = ctk.CTkLabel(
            folder_frame, 
            text=f"Save to: {self.download_path}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.folder_label.pack(side="left", padx=5)
        
        folder_button = ctk.CTkButton(
            folder_frame,
            text="Change Folder",
            command=self.select_folder,
            width=120,
            height=28,
            font=ctk.CTkFont(size=11)
        )
        folder_button.pack(side="left", padx=5)
        
        # Download button
        self.download_button = ctk.CTkButton(
            main_frame,
            text="⬇ Download",
            command=self.start_download,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            width=250,
            corner_radius=10
        )
        self.download_button.pack(pady=20)
        
        # Test button
        test_button = ctk.CTkButton(
            main_frame,
            text="🔍 Test yt-dlp",
            command=self.test_ytdlp,
            font=ctk.CTkFont(size=12),
            height=30,
            width=150,
            fg_color="gray40",
            hover_color="gray30"
        )
        test_button.pack(pady=5)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=500)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        # Status text box
        status_label = ctk.CTkLabel(
            main_frame, 
            text="Status:", 
            font=ctk.CTkFont(size=12)
        )
        status_label.pack(pady=(10, 5))
        
        self.status_text = ctk.CTkTextbox(
            main_frame, 
            width=500, 
            height=150,
            font=ctk.CTkFont(size=11)
        )
        self.status_text.pack(pady=5)
        
    def select_folder(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.download_path = folder
            self.folder_label.configure(text=f"Save to: {self.download_path}")
            self.log_status(f"Output folder changed to: {self.download_path}")
    
    def log_status(self, message):
        """Add message to status text box (thread-safe)"""
        self.root.after(0, self._log_status_ui, message)
    
    def _log_status_ui(self, message):
        """Internal method to update UI from main thread"""
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
    
    def clear_status(self):
        """Clear status text box"""
        self.status_text.delete("1.0", "end")
    
    def update_progress(self, value):
        """Update progress bar (thread-safe)"""
        self.root.after(0, self.progress_bar.set, value)
    
    def update_button(self, state, text):
        """Update download button (thread-safe)"""
        self.root.after(0, lambda: self.download_button.configure(state=state, text=text))
    
    def show_success(self, message):
        """Show success message (thread-safe)"""
        self.root.after(0, lambda: messagebox.showinfo("Success", message))
    
    def show_error(self, message):
        """Show error message (thread-safe)"""
        self.root.after(0, lambda: messagebox.showerror("Download Error", message))
    
    def test_ytdlp(self):
        """Test yt-dlp with a simple command"""
        self.clear_status()
        self.log_status("🔍 Testing yt-dlp installation...\n")
        
        # Test version
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            self.log_status(f"✅ yt-dlp version: {result.stdout.strip()}\n")
        except Exception as e:
            self.log_status(f"❌ yt-dlp not found: {e}\n")
            return
        
        # Test with a simple URL
        url = self.url_entry.get().strip() or "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.log_status(f"Testing with URL: {url}\n")
        
        try:
            cmd = ['yt-dlp', '--dump-json', '--no-playlist', url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_status("✅ yt-dlp can access YouTube successfully!")
                self.log_status("\nVideo info retrieved successfully!")
                # Parse and show some info
                try:
                    import json
                    info = json.loads(result.stdout)
                    self.log_status(f"Title: {info.get('title', 'N/A')}")
                    self.log_status(f"Duration: {info.get('duration', 0)}s")
                    self.log_status(f"Upload date: {info.get('upload_date', 'N/A')}")
                except:
                    pass
            else:
                self.log_status(f"❌ Error testing yt-dlp:\n{result.stderr}")
                self.log_status("\nTrying to update yt-dlp...")
                self.install_ytdlp()
                
        except Exception as e:
            self.log_status(f"❌ Test failed: {e}")
    
    def check_ffmpeg(self):
        """Check if ffmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, timeout=5)
            return True
        except:
            return False
    
    def start_download(self):
        """Start download in separate thread"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showwarning("Invalid Input", "Please enter a URL!")
            return
        
        # Disable download button during download
        self.download_button.configure(state="disabled", text="Downloading...")
        self.progress_bar.set(0)
        self.clear_status()
        
        # Start download in separate thread to prevent UI freezing
        download_thread = threading.Thread(target=self.download, args=(url,), daemon=True)
        download_thread.start()
    
    def run_ytdlp_command(self, url, options):
        """Run yt-dlp command and capture output"""
        cmd = ['yt-dlp'] + options + [url]
        
        self.log_status(f"Command: yt-dlp {' '.join(options)}\n")
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output line by line
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    self.log_status(line)
                    
                    # Update progress based on yt-dlp output
                    if '[download]' in line and '%' in line:
                        try:
                            # Extract percentage
                            percent_str = line.split('%')[0].split()[-1]
                            percent = float(percent_str) / 100
                            self.update_progress(percent)
                        except:
                            pass
            
            # Get any error output
            stderr = process.stderr.read()
            if stderr:
                self.log_status(f"\n⚠️ Errors/Warnings:\n{stderr}")
            
            returncode = process.wait()
            
            if returncode == 0:
                self.update_progress(1.0)
                return True
            else:
                self.log_status(f"\n❌ yt-dlp exited with code {returncode}")
                return False
                
        except FileNotFoundError:
            self.log_status("❌ yt-dlp not found! Installing now...")
            self.install_ytdlp()
            return False
        except Exception as e:
            self.log_status(f"❌ Error running yt-dlp: {e}")
            import traceback
            self.log_status(traceback.format_exc())
            return False
    
    def download(self, url):
        """Handle download based on selected type"""
        try:
            download_type = self.download_type.get()
            
            # Common options
            base_options = [
                '-o', f'{self.download_path}/%(title)s.%(ext)s',  # Output template
                '--no-mtime',  # Don't use Last-modified header
                '--no-playlist' if download_type != "Playlist" else '--yes-playlist',
                '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                '--extractor-args', 'youtube:player_client=android',  # Use Android client to bypass restrictions
                '--no-check-certificate',
            ]
            
            if download_type == "Single Video":
                options = base_options + [
                    '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                ]
                self.log_status("🎬 Downloading single video...")
                
            elif download_type == "Playlist":
                options = base_options + [
                    '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    '--yes-playlist',
                ]
                self.log_status("📋 Downloading playlist...")
                
            elif download_type == "Channel":
                options = base_options + [
                    '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                ]
                self.log_status("📺 Downloading channel videos...")
                
            elif download_type == "Audio Only":
                # Check if ffmpeg is available
                has_ffmpeg = self.check_ffmpeg()
                
                if has_ffmpeg:
                    options = base_options + [
                        '-x',  # Extract audio
                        '--audio-format', 'mp3',  # Convert to mp3
                        '--audio-quality', '0',  # Best quality
                    ]
                    self.log_status("🎵 Downloading audio (will convert to MP3)...")
                else:
                    options = base_options + [
                        '-f', 'bestaudio',  # Just download best audio (no conversion)
                    ]
                    self.log_status("🎵 Downloading audio (no ffmpeg - saving as original format)...")
                    self.log_status("💡 Install ffmpeg to get MP3 conversion: brew install ffmpeg")
                
            elif download_type == "Best Quality":
                options = base_options + [
                    '-f', 'bestvideo+bestaudio/best',  # Best video + best audio
                    '--merge-output-format', 'mp4',  # Merge into mp4
                ]
                self.log_status("💎 Downloading best quality...")
            
            # Run download
            success = self.run_ytdlp_command(url, options)
            
            if success:
                self.log_status(f"\n✅ Download complete!\nSaved to: {self.download_path}")
                self.show_success("Download completed successfully!")
            else:
                self.log_status("\n❌ Download failed!")
                
                # Check for common errors and provide solutions
                status_content = self.status_text.get("1.0", "end")
                
                if "This video is not available" in status_content:
                    error_msg = ("Video is not available. This could mean:\n\n"
                                "1. Video is region-restricted\n"
                                "2. Video is age-restricted or requires sign-in\n"
                                "3. Video is private or deleted\n\n"
                                "Try updating yt-dlp:\n"
                                "pip install -U yt-dlp")
                elif "Sign in to confirm" in status_content or "age" in status_content.lower():
                    error_msg = ("Video requires authentication.\n\n"
                                "To download age-restricted videos:\n"
                                "1. Export cookies from your browser\n"
                                "2. Use --cookies option in yt-dlp")
                elif "No video formats" in status_content:
                    error_msg = "No suitable video format found. Try a different quality option."
                else:
                    error_msg = "Download failed. Check the status log for details."
                
                self.show_error(error_msg)
            
            # Re-enable download button
            self.update_button("normal", "⬇ Download")
                
        except Exception as e:
            error_msg = f"An error occurred:\n{str(e)}"
            self.log_status(f"\n❌ Error: {str(e)}")
            self.show_error(error_msg)
            self.update_button("normal", "⬇ Download")
            self.update_progress(0)
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = YouTubeDownloaderGUI()
    app.run()