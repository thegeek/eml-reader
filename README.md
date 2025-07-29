# 📧 EML Reader

A professional email processing and analysis platform that provides both command-line and web-based interfaces for reading, parsing, and analyzing EML files.

## ✨ Features

### 🌐 Modern Web Interface
- **Dark Theme**: Professional dark interface with modern design
- **Drag & Drop**: Intuitive file upload with visual feedback
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Interactive Elements**: Smooth animations and hover effects
- **Real-time Processing**: Instant email analysis and display

### 📊 Comprehensive Email Analysis
- **Summary Cards** - Quick overview of key email information
- **Detailed Headers** - Complete email header analysis with copy buttons for important fields
- **Body Content** - Separate display for text and HTML content
- **Attachment Analysis** - File details, sizes, and content types
- **Message Metadata** - Technical email information and threading data
- **Raw EML Data** - Complete original email content for debugging and analysis
- **Thread Analysis** - Email conversation threading and relationship mapping

### 🧵 Email Threading Analysis
- **Automatic Thread Detection** - Identifies email conversations and relationships
- **Thread Timeline** - Chronological display of messages in conversations
- **Participant Tracking** - Lists all participants with message counts
- **Engagement Metrics** - Calculates engagement scores and activity levels
- **Response Time Analysis** - Tracks response times between messages
- **Thread Depth Calculation** - Shows how deep messages are in conversations
- **Interactive Thread Modal** - Click participant boxes to view detailed email context
- **Style Switching** - Toggle between dark and light themes for HTML content

### 🔧 Command Line Interface
- **Batch Processing** - Process multiple EML files at once
- **Thread Analysis** - Analyze email threads in directories
- **Thread Search** - Search threads by subject or participant
- **Thread Details** - View detailed thread information
- **Configuration Management** - Set file upload limits and other settings
- **JSON Output** - Export results in structured format

### 🔒 Security & Performance
- **HTTPS Support** - Secure connections with auto-generated SSL certificates
- **Content Sanitization** - Safe HTML display with CID image handling
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Configurable Limits** - Adjustable file upload size limits
- **Error Handling** - Robust error handling and user feedback

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

#### Thread Analysis
```bash
# Analyze email threads in a directory
eml-reader threads analyze /path/to/eml/files

# Search threads by subject or participant
eml-reader threads search "project update"

# Show detailed thread information
eml-reader threads show thread_abc123

# Save thread analysis to file
eml-reader threads analyze /path/to/eml/files --output threads.json --pretty
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
    "raw_size": 2048,
    "thread_analysis": {
      "thread_id": "thread_abc123",
      "thread_depth": 2,
      "is_reply": true,
      "is_forward": false,
      "thread_participants": ["sender@example.com", "recipient@example.com"],
      "engagement_indicators": {
        "engagement_score": 75,
        "content_length": 1024,
        "has_attachments": true
      }
    }
  },
  "raw_eml": "From: sender@example.com\nTo: recipient@example.com\n..."
}
```

#### GET `/api/threads`
List all analyzed email threads.

**Response:**
```json
{
  "status": "success",
  "thread_count": 5,
  "threads": [
    {
      "thread_id": "thread_abc123",
      "message_count": 3,
      "participants": ["user1@example.com", "user2@example.com"],
      "subject": "Project Update Discussion",
      "created": "2024-01-15T10:30:00Z",
      "last_activity": "2024-01-15T14:45:00Z",
      "max_depth": 2,
      "engagement_metrics": {
        "average_engagement_score": 78.5,
        "thread_activity_level": "medium"
      }
    }
  ]
}
```

#### GET `/api/threads/{thread_id}`
Get detailed information about a specific thread.

**Response:**
```json
{
  "status": "success",
  "thread_id": "thread_abc123",
  "summary": {
    "thread_id": "thread_abc123",
    "message_count": 3,
    "participants": ["user1@example.com", "user2@example.com"],
    "subject": "Project Update Discussion",
    "max_depth": 2
  },
  "timeline": [
    {
      "position": 1,
      "is_root": true,
      "is_latest": false,
      "email_data": {...},
      "thread_analysis": {...},
      "response_time": null
    },
    {
      "position": 2,
      "is_root": false,
      "is_latest": false,
      "email_data": {...},
      "thread_analysis": {...},
      "response_time": {
        "seconds": 3600,
        "formatted": "1h"
      }
    }
  ]
}
```

#### GET `/api/threads/search/{query}`
Search threads by subject or participant.

**Response:**
```json
{
  "status": "success",
  "query": "project",
  "result_count": 2,
  "results": [
    {
      "thread_id": "thread_abc123",
      "subject": "Project Update Discussion",
      "message_count": 3,
      "participants": ["user1@example.com", "user2@example.com"]
    }
  ]
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

### ✅ Completed Features
- [x] Web interface with modern dark theme
- [x] Drag & drop file upload
- [x] Comprehensive email analysis (headers, body, attachments, metadata)
- [x] Interactive accordion sections
- [x] Email address formatting with copy functionality
- [x] Toast notifications for user feedback
- [x] HTTPS support with auto-generated SSL certificates
- [x] Cross-platform compatibility
- [x] Command-line interface for batch processing
- [x] Configuration management
- [x] Raw EML data display
- [x] **Email threading analysis** - Complete implementation with thread detection, timeline generation, and conversation tracking
- [x] **Interactive thread analysis modal** - Clickable participant boxes with detailed email context
- [x] **HTML content sanitization** - Handles CID image references and security issues
- [x] **Style switching** - Dark/light theme toggle for HTML content display

### 🚀 Planned Features
- [ ] Advanced email filtering and search
- [ ] Email analytics dashboard
- [ ] Export functionality (PDF, CSV, JSON)
- [ ] Email signature detection and extraction
- [ ] Spam detection and scoring
- [ ] Email encryption analysis
- [ ] Multi-language support
- [ ] Email archiving and backup
- [ ] Real-time email monitoring
- [ ] Integration with email servers (IMAP, POP3)
- [ ] Email template analysis
- [ ] Sentiment analysis for email content
- [ ] Email workflow automation
- [ ] Advanced reporting and insights
- [ ] Email compliance checking
- [ ] Email security analysis
- [ ] Email performance metrics
- [ ] Email collaboration features
- [ ] Email data visualization
- [ ] Email API for third-party integrations
