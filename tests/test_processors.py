"""Tests for processor modules"""
import unittest
import os
import tempfile
from src.processors import PDFProcessor


class TestPDFProcessor(unittest.TestCase):
    """Test PDF processing functionality"""
    
    def setUp(self):
        self.processor = PDFProcessor()
    
    def test_initialization(self):
        """Test processor initializes correctly"""
        self.assertIsNotNone(self.processor)
        self.assertIsInstance(self.processor.content, dict)
    
    def test_chunk_content(self):
        """Test content chunking"""
        text = "This is a test sentence. " * 100
        chunks = self.processor.chunk_content(text, chunk_size=100)
        
        self.assertIsInstance(chunks, list)
        self.assertGreater(len(chunks), 0)
        
        # Check that chunks are roughly the right size
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 150)  # Allow some overflow
    
    def test_extract_headings(self):
        """Test heading extraction"""
        text = """Introduction
        
This is some text about the introduction.

Main Concepts

More text here.

Conclusion.
"""
        headings = self.processor.extract_headings(text)
        
        self.assertIsInstance(headings, list)
        # Should find some potential headings
        self.assertGreater(len(headings), 0)


class TestVideoProcessor(unittest.TestCase):
    """Test video processing functionality"""
    
    def test_initialization(self):
        """Test processor initializes correctly"""
        from src.processors import VideoProcessor
        processor = VideoProcessor()
        self.assertIsNotNone(processor)
        self.assertIsNotNone(processor.temp_dir)


if __name__ == '__main__':
    unittest.main()
