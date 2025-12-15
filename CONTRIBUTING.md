# Contributing to Study Material Automator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/study-material-automator.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with clear messages: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

## Testing

When adding new features:

1. Test with various PDF formats
2. Test with different video sources
3. Ensure error handling works properly
4. Verify output quality

## Areas for Contribution

We welcome contributions in these areas:

- **Additional Processors**: Support for more input formats (PPTX, DOCX, etc.)
- **Enhanced Diagrams**: More diagram types and visualization options
- **Interactive Features**: Web interface for the system
- **Language Support**: Multi-language content processing
- **Performance**: Optimization for large documents
- **Testing**: Unit tests and integration tests
- **Documentation**: Tutorials, guides, and examples

## Bug Reports

When reporting bugs, please include:

1. Description of the issue
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. System information (OS, Python version)
6. Error messages or logs

## Feature Requests

We're open to new ideas! When suggesting features:

1. Describe the feature and its benefits
2. Explain use cases
3. Consider implementation complexity
4. Suggest possible approaches

## Code Review Process

All submissions require review. We'll:

1. Check code quality and style
2. Verify functionality
3. Ensure documentation is updated
4. Test with various inputs
5. Provide constructive feedback

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing! 🎉
