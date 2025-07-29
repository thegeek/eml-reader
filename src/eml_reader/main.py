"""Main entry point for the EML Reader application.

EML Reader is a professional email processing and analysis platform that provides
both command-line and web-based interfaces for reading, parsing, and analyzing
EML files.

Features:
- Web interface with modern dark theme and drag & drop upload
- Command-line interface for batch processing
- Comprehensive email analysis (headers, body, attachments, metadata)
- Interactive results with expandable accordion sections
- Email address management with copy functionality
- Toast notifications for user feedback
- HTTPS support with auto-generated SSL certificates
- Cross-platform compatibility
- RESTful API for programmatic access

Usage:
    python -m eml_reader  # Start CLI interface
    eml-reader server     # Start web server
    eml-reader process file.eml  # Process EML file
"""

from .cli import cli


if __name__ == "__main__":
    cli()
