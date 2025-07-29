# 📧 EML Reader

A professional email processing and analysis platform that provides both command-line and web-based interfaces for reading, parsing, and analyzing EML files.

## ✨ Features

### 🌐 Web Interface
- **Modern Dark Theme** - Beautiful, professional UI with dark mode
- **Drag & Drop Upload** - Easy file upload with visual feedback
- **Real-time Processing** - Instant EML parsing and analysis
- **Interactive Results** - Expandable accordion sections for organized data display
- **Email Address Management** - Clickable email addresses with copy functionality
- **Toast Notifications** - User-friendly feedback for actions
- **Responsive Design** - Works perfectly on desktop and mobile devices

### 📊 Comprehensive Email Analysis
- **Summary Cards** - Quick overview of key email information
- **Detailed Headers** - Complete email header analysis with copy buttons for important fields
- **Body Content** - Separate display for text and HTML content
- **Attachment Analysis** - File details, sizes, and content types
- **Message Metadata** - Technical email information and threading data
- **Raw EML Data** - Complete original email content for debugging and analysis

### 🔧 Command Line Interface
- **File Processing** - Direct EML file parsing with JSON output
- **Summary Mode** - Quick overview of email content
- **Pretty Printing** - Formatted JSON output for readability
- **Output Control** - Save results to files or display in terminal

### 🚀 Web Server
- **HTTPS Support** - Secure connections with auto-generated SSL certificates
- **Configurable** - Customizable file upload limits and server settings
- **API Endpoints** - RESTful API for programmatic access
- **Cross-platform** - Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd eml-reader

# Install dependencies
pip install -e .
```

### Web Interface

```bash
# Initialize the application (first time only)
eml-reader bootstrap init

# Start the web server
eml-reader server

# Open your browser to https://localhost:8443
```

### Command Line

```bash
# Process an EML file
eml-reader process sample.eml

# Get summary only
eml-reader process sample.eml --summary

# Save results to file
eml-reader process sample.eml --output results.json --pretty
```

## 📖 Usage Guide

### Web Interface

1. **Upload EML File**
   - Drag and drop your EML file onto the upload area
   - Or click to browse and select a file
   - File will be processed automatically

2. **View Results**
   - **Summary Cards**: Quick overview of From, To, CC, BCC, Subject, Date, Attachments, and Size
   - **Email Headers**: Complete header analysis with copy buttons for From, To, CC, and Subject
   - **Email Body**: Separate sections for text and HTML content
   - **Attachments**: File details, sizes, and content types
   - **Message Metadata**: Technical information and threading data
   - **Raw EML Data**: Complete original email content

3. **Interactive Features**
   - Click email addresses to open in your email client
   - Click copy buttons to copy email addresses to clipboard
   - Expand/collapse accordion sections for organized viewing
   - Toast notifications confirm successful actions

### Command Line Interface

#### Process EML Files
```bash
# Basic processing
eml-reader process email.eml

# Summary only
eml-reader process email.eml --summary

# Pretty print output
eml-reader process email.eml --pretty

# Save to file
eml-reader process email.eml --output results.json
```

#### Server Management
```bash
# Start server with default settings
eml-reader server

# Custom host and port
eml-reader server --host 0.0.0.0 --port 8080

# Use custom SSL certificates
eml-reader server --cert /path/to/cert.crt --key /path/to/key.key
```

#### Bootstrap Commands
```bash
# Initialize application (first time setup)
eml-reader bootstrap init

# Check application status
eml-reader bootstrap check

# Custom SSL certificate generation
eml-reader bootstrap init --days 730 --country US --state CA --organization "My Company"
```

#### Configuration
```bash
# Set file upload size limit (in MB)
eml-reader config-file-size 50
```

## 🔧 Configuration

### Application Data Directory
The application stores its data in platform-specific directories:
- **Windows**: `%APPDATA%\eml-reader\`
- **macOS**: `~/Library/Application Support/eml-reader/`
- **Linux**: `~/.local/share/eml-reader/`

### Configuration File (`config.toml`)
```toml
[server]
host = "localhost"
port = 8443
ssl_enabled = true
file_upload_size_limit = 5242880  # 5MB in bytes

[ssl]
cert_file = "ssl/server.crt"
key_file = "ssl/server.key"
days_valid = 365
country = "US"
state = "CA"
locality = "San Francisco"
organization = "EML Reader"
common_name = "localhost"

[logging]
level = "INFO"
file = "eml-reader.log"
```

## 🌐 API Reference

### Endpoints

#### GET `/api/status`
Returns server status and version information.

**Response:**
```json
{
  "status": "running",
  "service": "EML Reader Server",
  "version": "0.1.0"
}
```

#### POST `/api/process`
Process EML content and return structured data.

**Request:**
- **Content-Type**: `multipart/form-data` or `application/json`
- **Body**: EML file or JSON with `eml_content` field

**Response:**
```json
{
  "status": "processed",
  "message": "EML file processed successfully",
  "filename": "email.eml",
  "summary": {
    "subject": "Email Subject",
    "from": "sender@example.com",
    "to": "recipient@example.com",
    "cc": "cc@example.com",
    "bcc": "bcc@example.com",
    "date": "Wed, 15 Jan 2024 10:30:00 +0000",
    "has_attachments": true,
    "attachment_count": 2,
    "has_html": true,
    "has_text": true,
    "size_bytes": 1024
  },
  "data": {
    "headers": {
      "common": {...},
      "all": {...},
      "count": 15
    },
    "body": {
      "text": "Plain text content",
      "html": "<html>HTML content</html>",
      "content_type": "multipart/alternative",
      "encoding": "utf-8"
    },
    "attachments": [
      {
        "filename": "document.pdf",
        "content_type": "application/pdf",
        "size": 1024,
        "content_id": "<attachment@example.com>",
        "content_disposition": "attachment; filename=\"document.pdf\""
      }
    ],
    "metadata": {
      "is_multipart": true,
      "content_type": "multipart/mixed",
      "date_parsed": "2024-01-15T10:30:00Z",
      "message_id": "<message@example.com>",
      "in_reply_to": "<reply@example.com>",
      "references": ["<ref1@example.com>", "<ref2@example.com>"]
    },
    "raw_size": 2048
  },
  "raw_eml": "From: sender@example.com\nTo: recipient@example.com\n..."
}
```

## 🛠️ Development

### Project Structure
```
eml-reader/
├── pyproject.toml          # Project configuration and dependencies
├── README.md              # This file
├── src/
│   └── eml_reader/
│       ├── __init__.py    # Package initialization
│       ├── main.py        # Main entry point
│       ├── cli.py         # Command-line interface
│       ├── server.py      # Web server implementation
│       ├── html.py        # HTML templates and pages
│       ├── eml_processor.py # EML parsing and processing
│       └── resource.py    # Resource management and SSL
```

### Key Components

#### EMLProcessor
- Parses EML files using Python's standard `email` module
- Extracts headers, body content, attachments, and metadata
- Provides summary information for quick overview
- Handles multipart messages and various email formats

#### Web Server
- Built with `aiohttp` for high-performance async operations
- Supports both HTTP and HTTPS modes
- Configurable file upload limits
- RESTful API endpoints for programmatic access

#### Resource Manager
- Cross-platform application data directory management
- SSL certificate generation and management
- Configuration file handling
- Bootstrap commands for initial setup

### Building and Testing

```bash
# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest

# Build package
python -m build
```

## 🔒 Security

- **HTTPS by Default** - Auto-generated SSL certificates for secure connections
- **File Upload Limits** - Configurable maximum file sizes
- **Input Validation** - Proper EML parsing and error handling
- **Cross-Platform Security** - Secure file permissions on all platforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues, questions, or feature requests:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

## 🎯 Roadmap

- [ ] Email threading analysis
- [ ] Advanced search and filtering
- [ ] Bulk EML processing
- [ ] Email export functionality
- [ ] Integration with email servers
- [ ] Plugin system for custom processors
- [ ] Advanced analytics and reporting
