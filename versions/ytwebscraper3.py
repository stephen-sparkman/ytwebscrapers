import customtkinter as ctk
from pytubefix import YouTube, Playlist, Channel
import os
import threading
from tkinter import filedialog, messagebox

class YouTubeDownloaderGUI:
    def __init__(self):
        # Set appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("YouTube Downloader")
        self.root.geometry("700x650")
        
        # Default download path
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Token storage
        self.po_token = ""
        self.visitor_data = ""
        
        # Create UI elements
        self.create_widgets()
        
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
        
        # Token configuration section (collapsible)
        token_frame = ctk.CTkFrame(main_frame)
        token_frame.pack(pady=10, padx=10, fill="x")
        
        token_label = ctk.CTkLabel(
            token_frame,
            text="🔑 Optional: Add tokens to bypass bot detection",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        token_label.pack(pady=5)
        
        # PO Token input
        po_label = ctk.CTkLabel(token_frame, text="po_token:", font=ctk.CTkFont(size=10))
        po_label.pack(pady=(5, 0))
        
        self.po_token_entry = ctk.CTkEntry(
            token_frame,
            placeholder_text="Paste po_token here (optional)",
            width=450,
            height=30,
            font=ctk.CTkFont(size=10)
        )
        self.po_token_entry.pack(pady=2)
        
        # Visitor Data input
        visitor_label = ctk.CTkLabel(token_frame, text="visitor_data:", font=ctk.CTkFont(size=10))
        visitor_label.pack(pady=(5, 0))
        
        self.visitor_data_entry = ctk.CTkEntry(
            token_frame,
            placeholder_text="Paste visitor_data here (optional)",
            width=450,
            height=30,
            font=ctk.CTkFont(size=10)
        )
        self.visitor_data_entry.pack(pady=2)
        
        help_button = ctk.CTkButton(
            token_frame,
            text="ℹ️ How to get tokens?",
            command=self.show_token_help,
            width=150,
            height=25,
            font=ctk.CTkFont(size=10)
        )
        help_button.pack(pady=5)
        
        # Download type selection
        type_label = ctk.CTkLabel(
            main_frame, 
            text="Select Download Type:", 
            font=ctk.CTkFont(size=14)
        )
        type_label.pack(pady=(10, 5))
        
        self.download_type = ctk.CTkOptionMenu(
            main_frame,
            values=["Single Video", "Playlist", "Channel", "Audio Only", "Thumbnail"],
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
        url_label.pack(pady=(10, 5))
        
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
        folder_frame.pack(pady=10)
        
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
        self.download_button.pack(pady=15)
        
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
            height=120,
            font=ctk.CTkFont(size=11)
        )
        self.status_text.pack(pady=5)
    
    def show_token_help(self):
        """Show instructions for getting tokens"""
        help_text = """How to get po_token and visitor_data:

1. Open YouTube in your browser
2. Press F12 to open Developer Tools
3. Go to the "Console" tab
4. Paste this code and press Enter:

console.log('po_token:', document.cookie.split(';').find(c => c.includes('PO_TOKEN'))?.split('=')[1] || 'Not found');
console.log('visitor_data:', document.cookie.split(';').find(c => c.includes('VISITOR_INFO1_LIVE'))?.split('=')[1] || 'Not found');

5. Copy the values and paste them into the fields above

Note: These tokens expire, so you may need to refresh them periodically."""
        
        messagebox.showinfo("Token Help", help_text)
    
    def get_youtube_object(self, url):
        """Create YouTube object with optional tokens"""
        po_token = self.po_token_entry.get().strip()
        visitor_data = self.visitor_data_entry.get().strip()
        
        if po_token and visitor_data:
            self.log_status("🔑 Using authentication tokens...")
            return YouTube(url, po_token=po_token, visitor_data=visitor_data)
        else:
            return YouTube(url)
    
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
    
    def download(self, url):
        """Handle download based on selected type"""
        try:
            download_type = self.download_type.get()
            
            if download_type == "Single Video":
                self.download_video(url)
            elif download_type == "Playlist":
                self.download_playlist(url)
            elif download_type == "Channel":
                self.download_channel(url)
            elif download_type == "Audio Only":
                self.download_audio(url)
            elif download_type == "Thumbnail":
                self.download_thumbnail(url)
            
            # Re-enable download button after successful download
            self.update_button("normal", "⬇ Download")
                
        except Exception as e:
            error_msg = f"An error occurred:\n{str(e)}"
            self.log_status(f"\n❌ Error: {str(e)}")
            
            # Check if it's a bot detection error
            if "bot" in str(e).lower() or "po_token" in str(e).lower():
                self.log_status("\n💡 Tip: Add po_token and visitor_data tokens above to fix this!")
                self.log_status("Click the 'ℹ️ How to get tokens?' button for instructions.")
            
            self.show_error(error_msg)
            # Re-enable download button after error
            self.update_button("normal", "⬇ Download")
            self.update_progress(0)
    
    def download_video(self, url):
        """Download single video"""
        self.log_status("🎬 Fetching video information...")
        yt = self.get_youtube_object(url)
        self.log_status(f"Title: {yt.title}")
        self.log_status(f"Duration: {yt.length}s")
        self.log_status("\n⬇ Downloading video...")
        
        self.update_progress(0.3)
        
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download(output_path=self.download_path)
        
        self.update_progress(1.0)
        self.log_status(f"✅ Download complete!\nSaved to: {self.download_path}")
        self.show_success("Video downloaded successfully!")
    
    def download_playlist(self, url):
        """Download entire playlist"""
        self.log_status("📋 Fetching playlist information...")
        pl = Playlist(url)
        
        # Get tokens if available
        po_token = self.po_token_entry.get().strip()
        visitor_data = self.visitor_data_entry.get().strip()
        
        total_videos = len(pl.video_urls)
        self.log_status(f"Found {total_videos} videos in playlist")
        self.log_status("\n⬇ Starting playlist download...\n")
        
        for index, video_url in enumerate(pl.video_urls, 1):
            try:
                # Create YouTube object with tokens for each video
                if po_token and visitor_data:
                    video = YouTube(video_url, po_token=po_token, visitor_data=visitor_data)
                else:
                    video = YouTube(video_url)
                    
                self.log_status(f"[{index}/{total_videos}] Downloading: {video.title}")
                video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=self.download_path)
                
                # Update progress
                progress = index / total_videos
                self.update_progress(progress)
                
                self.log_status(f"✅ Completed ({index}/{total_videos})\n")
            except Exception as e:
                self.log_status(f"❌ Failed to download video {index} - {str(e)}\n")
        
        self.log_status(f"\n🎉 Playlist download complete!\nSaved to: {self.download_path}")
        self.show_success(f"Downloaded {total_videos} videos successfully!")
    
    def download_channel(self, url):
        """Download all videos from a channel"""
        self.log_status("📺 Fetching channel information...")
        ch = Channel(url)
        
        # Get tokens if available
        po_token = self.po_token_entry.get().strip()
        visitor_data = self.visitor_data_entry.get().strip()
        
        self.log_status(f"Channel: {ch.channel_name}")
        total_videos = len(ch.video_urls)
        self.log_status(f"Found {total_videos} videos")
        self.log_status("\n⬇ Starting channel download...\n")
        
        for index, video_url in enumerate(ch.video_urls, 1):
            try:
                # Create YouTube object with tokens for each video
                if po_token and visitor_data:
                    video = YouTube(video_url, po_token=po_token, visitor_data=visitor_data)
                else:
                    video = YouTube(video_url)
                    
                self.log_status(f"[{index}/{total_videos}] Downloading: {video.title}")
                video.streams.first().download(output_path=self.download_path)
                
                # Update progress
                progress = index / total_videos
                self.update_progress(progress)
                
                self.log_status(f"✅ Completed ({index}/{total_videos})\n")
            except Exception as e:
                self.log_status(f"❌ Failed to download video {index} - {str(e)}\n")
        
        self.log_status(f"\n🎉 Channel download complete!\nSaved to: {self.download_path}")
        self.show_success(f"Downloaded {total_videos} videos from {ch.channel_name}!")
    
    def download_audio(self, url):
        """Download audio only"""
        self.log_status("🎵 Fetching video information...")
        yt = self.get_youtube_object(url)
        self.log_status(f"Title: {yt.title}")
        self.log_status("\n⬇ Downloading audio...")
        
        self.update_progress(0.3)
        
        audio = yt.streams.filter(only_audio=True).first()
        out_path = audio.download(output_path=self.download_path)
        
        # Convert to MP3
        self.log_status("🔄 Converting to MP3...")
        self.update_progress(0.7)
        
        new_name = os.path.splitext(out_path)
        mp3_path = new_name[0] + '.mp3'
        os.rename(out_path, mp3_path)
        
        self.update_progress(1.0)
        self.log_status(f"✅ Audio download complete!\nSaved to: {mp3_path}")
        self.show_success("Audio downloaded successfully!")
    
    def download_thumbnail(self, url):
        """Download video thumbnail"""
        self.log_status("🖼️ Fetching video information...")
        yt = self.get_youtube_object(url)
        self.log_status(f"Title: {yt.title}")
        self.log_status("\n⬇ Downloading thumbnail...")
        
        self.update_progress(0.3)
        
        video = yt.streams.filter(only_video=True).first()
        out_path = video.download(output_path=self.download_path)
        
        new_name = os.path.splitext(out_path)
        os.rename(out_path, new_name[0] + '.mp4')
        
        self.update_progress(1.0)
        self.log_status(f"✅ Thumbnail download complete!\nSaved to: {self.download_path}")
        self.show_success("Thumbnail downloaded successfully!")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = YouTubeDownloaderGUI()
    app.run()