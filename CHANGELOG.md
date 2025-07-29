# Changelog

All notable changes to the EML Reader project will be documented in this file.

## [0.2.1] - 2025-07-29

### 🎨 Improved - Thread Timeline Layout
- **Vertical Timeline Design**: New agenda-style timeline with alternating left/right message positioning
- **Timeline Axis**: Central gradient line with visual markers for message positions
- **Month Markers**: White circular markers showing month/year at timeline boundaries
- **Visual Pointers**: Triangular arrows connecting messages to the timeline axis
- **Enhanced Hover Effects**: Improved hover animations and visual feedback
- **Professional Styling**: Better typography, spacing, and visual hierarchy
- **Responsive Design**: Timeline adapts gracefully to different screen sizes

## [0.2.0] - 2025-07-29

### 🧵 Added - Email Threading Analysis
- **Complete Thread Analysis Engine**: New `thread_analyzer.py` module with comprehensive email threading capabilities
- **Thread Detection**: Automatic identification of email conversations using Message-ID, In-Reply-To, and References headers
- **Thread Timeline**: Chronological display of messages in conversations with response time analysis
- **Participant Tracking**: Lists all participants with message counts and engagement metrics
- **Engagement Scoring**: Calculates engagement scores based on content length, recipients, and attachments
- **Thread Depth Calculation**: Shows how deep messages are in conversations (capped at 15 levels)
- **Subject Analysis**: Detects Re:, Fw:, Fwd: prefixes and thread continuation patterns

### 🎨 Added - Interactive Thread Analysis Modal
- **Clickable Participant Boxes**: Click "1 message" boxes to view detailed email context
- **Email Context Modal**: Beautiful modal dialog with comprehensive email information
- **Style Switching**: Toggle between dark and light themes for HTML content display
- **Responsive Layout**: Professional layout with proper spacing for email addresses
- **Enhanced Metadata Display**: Organized metadata sections with better visual hierarchy

### 🔧 Added - CLI Thread Analysis Commands
- **`eml-reader threads analyze <directory>`**: Analyze email threads in directories
- **`eml-reader threads search <query>`**: Search threads by subject or participant
- **`eml-reader threads show <thread_id>`**: Show detailed thread information
- **Batch Processing**: Process multiple EML files for thread analysis
- **JSON Output**: Export thread analysis results in structured format

### 🌐 Added - Thread Analysis API Endpoints
- **`GET /api/threads`**: List all analyzed threads with summaries
- **`GET /api/threads/{thread_id}`**: Get detailed thread information and timeline
- **`GET /api/threads/search/{query}`**: Search threads by subject or participant
- **Thread Timeline**: Chronological message timeline with response times
- **Engagement Metrics**: Thread-level engagement analysis

### 🔒 Added - Security & Content Sanitization
- **HTML Content Sanitization**: Safe HTML display with CID image reference handling
- **Security Enhancements**: Removes potentially dangerous script tags and links
- **CID Image Handling**: Replaces embedded images with professional placeholders
- **Error Prevention**: Eliminates console errors from problematic email content

### 🎯 Improved - Web Interface
- **Thread Analysis Section**: New accordion section for thread information
- **Better Layout**: Improved modal layout with proper spacing and alignment
- **Copy Button Positioning**: Fixed alignment issues with email address copy buttons
- **Toast Notifications**: Enhanced user feedback for all interactions
- **Responsive Design**: Better mobile and tablet experience

### 📊 Improved - Email Analysis
- **Thread Integration**: Every processed email now includes thread analysis
- **Enhanced Metadata**: Thread ID, depth, position, and engagement indicators
- **Better Data Structure**: Improved organization of email analysis results
- **Raw EML Display**: Complete original email content for debugging

### 🛠️ Technical Improvements
- **Thread Manager**: Comprehensive thread collection and relationship management
- **Thread Analyzer**: Sophisticated email threading analysis engine
- **Performance Optimization**: Efficient thread detection and analysis
- **Error Handling**: Robust error handling for thread analysis operations
- **Code Organization**: Better separation of concerns and modular design

## [0.1.0] - 2025-07-29

### 🎉 Initial Release
- **Web Interface**: Modern dark theme with drag & drop file upload
- **Email Processing**: Comprehensive EML file parsing and analysis
- **Interactive Results**: Expandable accordion sections for organized data display
- **Email Address Management**: Clickable email addresses with copy functionality
- **Toast Notifications**: User-friendly feedback for actions
- **HTTPS Support**: Secure connections with auto-generated SSL certificates
- **Command Line Interface**: Direct EML file processing with JSON output
- **Cross-platform Compatibility**: Works on Windows, macOS, and Linux
- **Configuration Management**: Customizable file upload limits and server settings
- **API Endpoints**: RESTful API for programmatic access
- **Raw EML Data**: Complete original email content display
- **Attachment Analysis**: File details, sizes, and content types
- **Message Metadata**: Technical email information extraction