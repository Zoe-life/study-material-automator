"""Video Processing Module"""
import os
import tempfile
from typing import Dict, Optional
import yt_dlp
from openai import OpenAI

try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False


class VideoProcessor:
    """Processes video files and URLs to extract audio and metadata"""
    
    def __init__(self, temp_dir: Optional[str] = None):
        self.temp_dir = temp_dir or tempfile.gettempdir()
    
    def download_video(self, video_url: str, output_path: Optional[str] = None) -> str:
        """
        Download video from URL
        
        Args:
            video_url: URL of the video
            output_path: Path to save the video (optional)
            
        Returns:
            Path to downloaded video file
        """
        if not output_path:
            output_path = os.path.join(self.temp_dir, 'downloaded_video.%(ext)s')
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
        
        return filename
    
    def extract_audio(self, video_path: str, audio_output: Optional[str] = None) -> str:
        """
        Extract audio from video file
        
        Args:
            video_path: Path to video file
            audio_output: Path to save audio file (optional)
            
        Returns:
            Path to extracted audio file
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if not audio_output:
            audio_output = os.path.join(self.temp_dir, 'audio.mp3')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': audio_output.replace('.mp3', ''),
            'quiet': True,
        }
        
        # If it's a local file, we need to extract using moviepy
        try:
            if not MOVIEPY_AVAILABLE:
                raise ImportError("moviepy not available")
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_output, logger=None)
            video.close()
        except Exception as e:
            print(f"Warning: Could not extract audio using moviepy: {e}")
            # Fallback: just return the video path, transcription might still work
            return video_path
        
        return audio_output
    
    def get_video_info(self, video_source: str) -> Dict:
        """
        Get video metadata
        
        Args:
            video_source: Video file path or URL
            
        Returns:
            Dictionary with video metadata
        """
        info = {
            'duration': None,
            'title': None,
            'description': None,
            'source': video_source
        }
        
        # If it's a URL, use yt-dlp to get info
        if video_source.startswith('http'):
            try:
                ydl_opts = {'quiet': True, 'no_warnings': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    video_info = ydl.extract_info(video_source, download=False)
                    info['duration'] = video_info.get('duration')
                    info['title'] = video_info.get('title')
                    info['description'] = video_info.get('description')
            except Exception as e:
                print(f"Warning: Could not extract video info: {e}")
        else:
            # Local file
            try:
                if not MOVIEPY_AVAILABLE:
                    raise ImportError("moviepy not available")
                video = VideoFileClip(video_source)
                info['duration'] = video.duration
                info['title'] = os.path.basename(video_source)
                video.close()
            except Exception as e:
                print(f"Warning: Could not get video info: {e}")
        
        return info
    
    def transcribe_audio(self, audio_path: str, api_key: str) -> str:
        """
        Transcribe audio using OpenAI Whisper API
        
        Args:
            audio_path: Path to audio file
            api_key: OpenAI API key
            
        Returns:
            Transcribed text
        """
        try:
            client = OpenAI(api_key=api_key)
            
            with open(audio_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            
            return transcript
        except Exception as e:
            raise Exception(f"Transcription failed: {e}")
