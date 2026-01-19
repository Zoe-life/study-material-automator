"""Configuration Management"""
import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Manages application configuration"""
    
    def __init__(self, env_file: Optional[str] = None):
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        # API Keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        
        # Model Configuration
        self.openai_model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.openai_temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))
        
        # Directories
        self.output_dir = os.getenv('OUTPUT_DIR', 'output')
        self.temp_dir = os.getenv('TEMP_DIR', 'temp')
        
        # Create directories if they don't exist
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def validate(self) -> bool:
        """
        Validate configuration
        
        Returns:
            True if configuration is valid
        """
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not set")
            return False
        return True
    
    def get_output_path(self, filename: str) -> str:
        """Get full path for output file"""
        return os.path.join(self.output_dir, filename)
    
    def get_temp_path(self, filename: str) -> str:
        """Get full path for temporary file"""
        return os.path.join(self.temp_dir, filename)
