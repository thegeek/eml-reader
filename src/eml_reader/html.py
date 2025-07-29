"""HTML templates and pages for the EML Reader application.

This module contains all HTML templates and pages for the EML Reader web interface,
including the welcome page, upload interface, and results display.

Features:
- Modern dark theme with professional design
- Responsive layout for desktop and mobile devices
- Drag & drop file upload with visual feedback
- Interactive accordion sections for organized data display
- Email address management with clickable links and copy functionality
- Toast notifications for user feedback
- Custom scrollbars and smooth animations
- Comprehensive results display including:
  - Summary cards for key email information
  - Detailed header analysis with copy buttons
  - Body content display (text and HTML)
  - Attachment analysis and details
  - Message metadata and threading information
  - Raw EML data for debugging and analysis

The module provides a complete web interface that combines modern design with
powerful functionality for email analysis and processing.
"""

# CSS styles shared across pages
COMMON_STYLES = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #0a0a0a;
        color: #ffffff;
        line-height: 1.6;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    .main-container {
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .hero-section {
        text-align: center;
        margin-bottom: 4rem;
        padding: 3rem 0;
    }
    
    .hero-logo {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #a0a0a0;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    .status-section {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 8px 32px rgba(0, 184, 148, 0.3);
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: white;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    .action-button {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        border: none;
        cursor: pointer;
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    .upload-section {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        max-width: 600px;
        margin: 0 auto;
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        color: #667eea;
    }
    
    .upload-title {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .upload-description {
        color: #a0a0a0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .file-upload-area {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 3rem 2rem;
        margin: 2rem 0;
        background: #252525;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .file-upload-area:hover {
        border-color: #764ba2;
        background: #2a2a2a;
    }
    
    .file-upload-area.dragover {
        border-color: #00b894;
        background: #1a2a1a;
    }
    
    .upload-icon-large {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: #667eea;
    }
    
    .upload-text {
        color: #e0e0e0;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .upload-hint {
        color: #a0a0a0;
        font-size: 0.9rem;
    }
    
    .file-input {
        display: none;
    }
    
    .upload-button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        margin-top: 1rem;
    }
    
    .upload-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    .upload-button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }
    
    .file-info {
        background: #252525;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        display: none;
    }
    
    .file-info.show {
        display: block;
    }
    
    .file-name {
        color: #e0e0e0;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .file-size {
        color: #a0a0a0;
        font-size: 0.9rem;
    }
    
    .results-section {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        display: none;
    }
    
    .results-section.show {
        display: block;
    }
    
    .results-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #2a2a2a;
    }
    
    .results-icon {
        font-size: 2rem;
        color: #00b894;
    }
    
    .results-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .summary-grid {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .summary-card {
        background: #252525;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
    }
    
    .summary-card:hover {
        transform: translateY(-2px);
        border-color: #667eea;
        background: #2a2a2a;
    }
    
    .summary-icon {
        font-size: 2rem;
        color: #667eea;
        flex-shrink: 0;
    }
    
    .summary-info {
        flex: 1;
    }
    
    .summary-label {
        color: #a0a0a0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .summary-value {
        color: #ffffff;
        font-weight: 600;
        font-size: 1.1rem;
        word-break: break-word;
    }
    
    .accordion-content {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }
    
    .accordion-content.active {
        max-height: 600px;
        padding: 1.5rem;
        overflow-y: auto;
    }
    
    /* Custom Scrollbar Styles */
    .accordion-content::-webkit-scrollbar {
        width: 8px;
    }
    
    .accordion-content::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 4px;
    }
    
    .accordion-content::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .accordion-content::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    .accordion-content::-webkit-scrollbar-corner {
        background: #1a1a1a;
    }
    
    /* Firefox scrollbar */
    .accordion-content {
        scrollbar-width: thin;
        scrollbar-color: #667eea #1a1a1a;
    }
    
    /* Content boxes scrollbar */
    .content-text::-webkit-scrollbar,
    .content-html::-webkit-scrollbar,
    .body-content::-webkit-scrollbar {
        width: 8px;
    }
    
    .content-text::-webkit-scrollbar-track,
    .content-html::-webkit-scrollbar-track,
    .body-content::-webkit-scrollbar-track {
        background: #0d1117;
        border-radius: 4px;
    }
    
    .content-text::-webkit-scrollbar-thumb,
    .content-html::-webkit-scrollbar-thumb,
    .body-content::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    .content-text::-webkit-scrollbar-thumb:hover,
    .content-html::-webkit-scrollbar-thumb:hover,
    .body-content::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
    
    .content-text::-webkit-scrollbar-corner,
    .content-html::-webkit-scrollbar-corner,
    .body-content::-webkit-scrollbar-corner {
        background: #0d1117;
    }
    
    .content-text,
    .content-html,
    .body-content {
        scrollbar-width: thin;
        scrollbar-color: #667eea #0d1117;
    }
    
    .data-section {
        margin-bottom: 1.5rem;
    }
    
    .data-section:last-child {
        margin-bottom: 0;
    }
    
    .data-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .data-grid {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .data-item {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .data-item:hover {
        border-color: #667eea;
        background: #252525;
    }
    
    .data-label {
        color: #a0a0a0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .data-value {
        color: #e0e0e0;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.9rem;
        word-break: break-word;
        line-height: 1.5;
    }
    
    .data-value.empty {
        color: #666;
        font-style: italic;
    }
    
    .accordion-item {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        margin-bottom: 1rem;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .accordion-item:hover {
        border-color: #667eea;
    }
    
    .accordion-header {
        background: #252525;
        padding: 1rem 1.5rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
        border-bottom: 1px solid #333;
    }
    
    .accordion-header:hover {
        background: #2a2a2a;
    }
    
    .accordion-header.active {
        background: #667eea;
        color: white;
    }
    
    .accordion-title {
        font-weight: 600;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .accordion-icon {
        font-size: 1.2rem;
        transition: transform 0.3s ease;
    }
    
    .accordion-header.active .accordion-icon {
        transform: rotate(180deg);
    }
    
    .content-box {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .content-box:last-child {
        margin-bottom: 0;
    }
    
    .content-box-title {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .content-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #e0e0e0;
        white-space: pre-wrap;
        word-break: break-word;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .content-html {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #e0e0e0;
        background: #1a1a1a;
        border: 1px solid #667eea;
        border-radius: 8px;
        padding: 1.5rem;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .content-html * {
        max-width: 100%;
    }
    
    .attachments-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .attachment-item {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
    }
    
    .attachment-item:hover {
        border-color: #667eea;
        background: #252525;
    }
    
    .attachment-icon {
        font-size: 1.5rem;
        color: #667eea;
    }
    
    .attachment-info {
        flex: 1;
    }
    
    .attachment-name {
        color: #e0e0e0;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    
    .attachment-details {
        color: #a0a0a0;
        font-size: 0.85rem;
    }
    
    .body-content {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1.5rem;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        max-height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-break: break-word;
    }
    
    .body-content.html {
        background: #1a1a1a;
        border-color: #667eea;
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid #ffffff;
        border-radius: 50%;
        border-top-color: transparent;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .content-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 3rem;
        margin-bottom: 4rem;
    }
    
    .api-section {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .endpoint-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .endpoint-item {
        background: #252525;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .endpoint-item:hover {
        transform: translateY(-2px);
        border-color: #764ba2;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
    }
    
    .endpoint-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .method-badge {
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .method-get {
        background: #667eea;
        color: white;
    }
    
    .method-post {
        background: #e17055;
        color: white;
    }
    
    .endpoint-path {
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 1rem;
        color: #e0e0e0;
        font-weight: 500;
    }
    
    .endpoint-description {
        color: #a0a0a0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    .examples-section {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .code-examples {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .code-block {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1.5rem;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.85rem;
        line-height: 1.6;
        overflow-x: auto;
    }
    
    .code-comment {
        color: #7d8590;
    }
    
    .code-string {
        color: #a5d6ff;
    }
    
    .code-keyword {
        color: #ff7b72;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        border-top: 1px solid #2a2a2a;
        margin-top: 3rem;
    }
    
    .version-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #252525;
        color: #a0a0a0;
        padding: 0.75rem 1.5rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #333;
    }
    
    .error-container {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 16px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .error-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .error-title {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    
    .error-message {
        background: #2d1b1b;
        border: 1px solid #4a2c2c;
        border-radius: 8px;
        padding: 1rem;
        color: #ff6b6b;
        margin: 1.5rem 0;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
    }
    
    .back-link {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .back-link:hover {
        color: #764ba2;
    }
    
    .copy-btn {
        background: none;
        border: none;
        color: #a0a0a0;
        cursor: pointer;
        font-size: 1rem;
        padding: 0.25rem;
        margin-left: 0.5rem;
        border-radius: 4px;
        transition: all 0.3s ease;
        opacity: 0.7;
    }
    
    .copy-btn:hover {
        color: #667eea;
        opacity: 1;
        background: rgba(102, 126, 234, 0.1);
    }
    
    .copy-btn:active {
        transform: scale(0.95);
    }
    
    .toast {
        position: fixed;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        z-index: 10000;
        pointer-events: none;
        opacity: 0;
        transform: translateY(10px);
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    
    .toast.show {
        opacity: 1;
        transform: translateY(0);
    }
    
    .toast::before {
        content: '✅';
        margin-right: 0.5rem;
    }
    
    @media (max-width: 768px) {
        body {
            padding: 10px;
        }
        
        .content-grid {
            grid-template-columns: 1fr;
            gap: 2rem;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .api-section,
        .examples-section {
            padding: 1.5rem;
        }
        
        .status-section {
            flex-direction: column;
            gap: 1rem;
        }
        
        .upload-section {
            padding: 2rem;
        }
        
        .summary-grid {
            grid-template-columns: 1fr;
        }
        
        .data-grid {
            grid-template-columns: 1fr;
        }
        
        .tabs-header {
            flex-wrap: wrap;
        }
    }
</style>
"""

# Welcome page HTML
WELCOME_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EML Reader - Professional Email Processing</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    {COMMON_STYLES}
</head>
<body>
    <div class="main-container">
        <div class="hero-section">
            <div class="hero-logo">📧</div>
            <h1 class="hero-title">EML Reader Server</h1>
            <p class="hero-subtitle">Professional Email Processing & Analysis Platform</p>
            <div class="status-section">
                <div class="status-indicator">
                    <div class="status-dot"></div>
                    Server Running
                </div>
                <a href="/upload" class="action-button">
                    <span>📤</span>
                    Upload EML File
                </a>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="api-section">
                <h2 class="section-title">🚀 API Endpoints</h2>
                <div class="endpoint-list">
                    <div class="endpoint-item">
                        <div class="endpoint-header">
                            <span class="method-badge method-get">GET</span>
                            <span class="endpoint-path">/api/status</span>
                        </div>
                        <div class="endpoint-description">
                            Retrieve server status and version information
                        </div>
                    </div>
                    
                    <div class="endpoint-item">
                        <div class="endpoint-header">
                            <span class="method-badge method-post">POST</span>
                            <span class="endpoint-path">/api/process</span>
                        </div>
                        <div class="endpoint-description">
                            Process EML content and extract email data
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="examples-section">
                <h2 class="section-title">📖 Quick Start</h2>
                <div class="code-examples">
                    <div class="code-block">
<span class="code-comment"># Check server status</span>
curl https://localhost:8443/api/status
                    </div>
                    
                    <div class="code-block">
<span class="code-comment"># Process an EML file</span>
curl -X POST https://localhost:8443/api/process \\
  -H <span class="code-string">"Content-Type: application/json"</span> \\
  -d <span class="code-string">'{{"eml_content": "your eml content here"}}'</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <div class="version-badge">
                <span>⚡</span>
                EML Reader Server v0.1.0
            </div>
        </div>
    </div>
</body>
</html>
"""

# Upload page HTML
UPLOAD_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EML Reader - Upload File</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    {COMMON_STYLES}
</head>
<body>
    <div class="main-container">
        <div class="upload-section">
            <div class="upload-icon">📤</div>
            <h1 class="upload-title">Upload EML File</h1>
            <p class="upload-description">Select an EML file to process and analyze</p>
            
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="file-upload-area" id="uploadArea">
                    <div class="upload-icon-large">📁</div>
                    <div class="upload-text">Drop your EML file here</div>
                    <div class="upload-hint">or click to browse</div>
                    <input type="file" id="fileInput" class="file-input" accept=".eml" />
                </div>
                
                <div class="file-info" id="fileInfo">
                    <div class="file-name" id="fileName"></div>
                    <div class="file-size" id="fileSize"></div>
                </div>
                
                <button type="submit" class="upload-button" id="uploadButton" disabled>
                    Process EML File
                </button>
            </form>
        </div>
        
        <!-- Results Section -->
        <div class="results-section" id="resultsSection">
            <div class="results-header">
                <div class="results-icon">✅</div>
                <div class="results-title">Processing Results</div>
            </div>
            
            <!-- Summary Cards -->
            <div class="summary-grid" id="summaryGrid">
                <div class="summary-card">
                    <div class="summary-icon">📧</div>
                    <div class="summary-info">
                        <div class="summary-label">Subject</div>
                        <div class="summary-value" id="summarySubject">-</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">👤</div>
                    <div class="summary-info">
                        <div class="summary-label">From</div>
                        <div class="summary-value" id="summaryFrom">-</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">📬</div>
                    <div class="summary-info">
                        <div class="summary-label">To</div>
                        <div class="summary-value" id="summaryTo">-</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">📋</div>
                    <div class="summary-info">
                        <div class="summary-label">CC</div>
                        <div class="summary-value" id="summaryCc">-</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">👁️</div>
                    <div class="summary-info">
                        <div class="summary-label">BCC</div>
                        <div class="summary-value" id="summaryBcc">-</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">📅</div>
                    <div class="summary-info">
                        <div class="summary-label">Date</div>
                        <div class="summary-value" id="summaryDate">-</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">📎</div>
                    <div class="summary-info">
                        <div class="summary-label">Attachments</div>
                        <div class="summary-value" id="summaryAttachments">-</div>
                    </div>
                </div>
                <div class="summary-card">
                    <div class="summary-icon">📊</div>
                    <div class="summary-info">
                        <div class="summary-label">Size</div>
                        <div class="summary-value" id="summarySize">-</div>
                    </div>
                </div>
            </div>
            
            <!-- Content Sections -->
            <div class="tabs-container">
                <!-- Headers Section -->
                <div class="accordion-item">
                    <div class="accordion-header" data-accordion="headers">
                        <div class="accordion-title">📋 Email Headers</div>
                        <div class="accordion-icon">▼</div>
                    </div>
                    <div class="accordion-content" id="headersContent">
                        <div class="data-grid" id="commonHeadersGrid"></div>
                    </div>
                </div>
                
                <!-- Body Section -->
                <div class="accordion-item">
                    <div class="accordion-header" data-accordion="body">
                        <div class="accordion-title">📝 Email Body</div>
                        <div class="accordion-icon">▼</div>
                    </div>
                    <div class="accordion-content" id="bodyContent">
                        <div class="content-box">
                            <div class="content-box-title">📝 Text Content</div>
                            <div class="content-text" id="textContent">No text content available</div>
                        </div>
                        <div class="content-box">
                            <div class="content-box-title">🌐 HTML Content</div>
                            <div class="content-html" id="htmlContent">No HTML content available</div>
                        </div>
                    </div>
                </div>
                
                <!-- Attachments Section -->
                <div class="accordion-item">
                    <div class="accordion-header" data-accordion="attachments">
                        <div class="accordion-title">📎 Attachments</div>
                        <div class="accordion-icon">▼</div>
                    </div>
                    <div class="accordion-content" id="attachmentsContent">
                        <div class="attachments-list" id="attachmentsList">
                            <div class="data-value empty">No attachments found</div>
                        </div>
                    </div>
                </div>
                
                <!-- Metadata Section -->
                <div class="accordion-item">
                    <div class="accordion-header" data-accordion="metadata">
                        <div class="accordion-title">🔍 Message Metadata</div>
                        <div class="accordion-icon">▼</div>
                    </div>
                    <div class="accordion-content" id="metadataContent">
                        <div class="data-grid" id="metadataGrid"></div>
                    </div>
                </div>
                
                <!-- Raw EML Data Section -->
                <div class="accordion-item">
                    <div class="accordion-header" data-accordion="raw">
                        <div class="accordion-title">📄 Raw EML Data</div>
                        <div class="accordion-icon">▼</div>
                    </div>
                    <div class="accordion-content" id="rawContent">
                        <div class="content-box">
                            <div class="content-box-title">📄 Raw Email Content</div>
                            <div class="body-content" id="rawEmlData">No raw data available</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <a href="/" class="back-link">
                <span>←</span>
                Back to Home
            </a>
        </div>
    </div>
    
    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const uploadButton = document.getElementById('uploadButton');
        const uploadForm = document.getElementById('uploadForm');
        const resultsSection = document.getElementById('resultsSection');
        
        // Accordion functionality
        const accordionHeaders = document.querySelectorAll('.accordion-header');
        
        accordionHeaders.forEach(header => {{
            header.addEventListener('click', () => {{
                const accordionItem = header.closest('.accordion-item');
                const content = accordionItem.querySelector('.accordion-content');
                const icon = header.querySelector('.accordion-icon');
                
                // Toggle active state
                const isActive = header.classList.contains('active');
                
                // Close all accordions
                accordionHeaders.forEach(h => {{
                    h.classList.remove('active');
                    h.closest('.accordion-item').querySelector('.accordion-content').classList.remove('active');
                }});
                
                // Open clicked accordion if it wasn't active
                if (!isActive) {{
                    header.classList.add('active');
                    content.classList.add('active');
                }}
            }});
        }});
        
        // Auto-open first accordion (Headers) by default
        setTimeout(() => {{
            const firstAccordion = document.querySelector('.accordion-header');
            if (firstAccordion) {{
                firstAccordion.click();
            }}
        }}, 100);
        
        // Handle file selection
        fileInput.addEventListener('change', function(e) {{
            const file = e.target.files[0];
            if (file) {{
                fileName.textContent = file.name;
                fileSize.textContent = formatFileSize(file.size);
                fileInfo.classList.add('show');
                uploadButton.disabled = false;
                
                // Hide previous results when new file is selected
                resultsSection.classList.remove('show');
            }}
        }});
        
        // Handle drag and drop
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {{
            e.preventDefault();
            uploadArea.classList.add('dragover');
        }});
        
        uploadArea.addEventListener('dragleave', () => {{
            uploadArea.classList.remove('dragover');
        }});
        
        uploadArea.addEventListener('drop', (e) => {{
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {{
                fileInput.files = files;
                const file = files[0];
                fileName.textContent = file.name;
                fileSize.textContent = formatFileSize(file.size);
                fileInfo.classList.add('show');
                uploadButton.disabled = false;
                
                // Hide previous results when new file is dropped
                resultsSection.classList.remove('show');
            }}
        }});
        
        // Handle form submission
        uploadForm.addEventListener('submit', async (e) => {{
            e.preventDefault();
            const file = fileInput.files[0];
            if (!file) return;
            
            uploadButton.disabled = true;
            uploadButton.innerHTML = '<span class="loading-spinner"></span> Processing...';
            
            try {{
                const formData = new FormData();
                formData.append('file', file);
                
                const response = await fetch('/api/process', {{
                    method: 'POST',
                    body: formData
                }});
                
                const result = await response.json();
                
                if (response.ok) {{
                    displayResults(result.data, result.summary, result.raw_eml);
                    resultsSection.classList.add('show');
                    resultsSection.scrollIntoView({{ behavior: 'smooth' }});
                }} else {{
                    alert('Error processing file: ' + result.error);
                }}
            }} catch (error) {{
                alert('Error uploading file: ' + error.message);
            }} finally {{
                uploadButton.disabled = false;
                uploadButton.textContent = 'Process EML File';
            }}
        }});
        
        function displayResults(data, summary, rawEml) {{
            // Update summary cards
            document.getElementById('summarySubject').textContent = summary.subject || 'No Subject';
            document.getElementById('summaryFrom').innerHTML = formatEmailAddresses(summary.from || 'Unknown');
            document.getElementById('summaryTo').innerHTML = formatEmailAddresses(summary.to || 'Unknown');
            document.getElementById('summaryCc').innerHTML = formatEmailAddresses(summary.cc || 'N/A');
            document.getElementById('summaryBcc').innerHTML = formatEmailAddresses(summary.bcc || 'N/A');
            document.getElementById('summaryDate').textContent = summary.date || 'Unknown';
            document.getElementById('summaryAttachments').textContent = summary.attachment_count || '0';
            document.getElementById('summarySize').textContent = formatFileSize(summary.size_bytes || 0);
            
            // Display headers
            const commonHeaders = data.headers?.common || {{}};
            const commonHeadersGrid = document.getElementById('commonHeadersGrid');
            commonHeadersGrid.innerHTML = '';
            
            Object.entries(commonHeaders).forEach(([key, value]) => {{
                const item = document.createElement('div');
                item.className = 'data-item';
                
                // Only show copy buttons for specific fields
                const shouldShowCopyButton = ['from', 'to', 'cc', 'subject'].includes(key.toLowerCase());
                
                if (shouldShowCopyButton) {{
                    item.innerHTML = `
                        <div class="data-label">${{key}}</div>
                        <div class="data-value">${{formatEmailAddresses(value)}}</div>
                    `;
                }} else {{
                    item.innerHTML = `
                        <div class="data-label">${{key}}</div>
                        <div class="data-value">${{value}}</div>
                    `;
                }}
                
                commonHeadersGrid.appendChild(item);
            }});
            
            // Display body content
            const textContent = document.getElementById('textContent');
            const htmlContent = document.getElementById('htmlContent');
            
            if (data.body?.text) {{
                textContent.textContent = data.body.text;
            }} else {{
                textContent.textContent = 'No text content available';
            }}
            
            if (data.body?.html) {{
                htmlContent.innerHTML = data.body.html;
            }} else {{
                htmlContent.textContent = 'No HTML content available';
            }}
            
            // Display attachments
            const attachmentsList = document.getElementById('attachmentsList');
            const attachments = data.attachments || [];
            
            if (attachments.length > 0) {{
                attachmentsList.innerHTML = '';
                attachments.forEach(attachment => {{
                    const item = document.createElement('div');
                    item.className = 'attachment-item';
                    item.innerHTML = `
                        <div class="attachment-icon">📎</div>
                        <div class="attachment-info">
                            <div class="attachment-name">${{attachment.filename || 'Unnamed'}}</div>
                            <div class="attachment-details">${{attachment.content_type}} • ${{formatFileSize(attachment.size)}}</div>
                        </div>
                    `;
                    attachmentsList.appendChild(item);
                }});
            }} else {{
                attachmentsList.innerHTML = '<div class="data-value empty">No attachments found</div>';
            }}
            
            // Display metadata
            const metadata = data.metadata || {{}};
            const metadataGrid = document.getElementById('metadataGrid');
            metadataGrid.innerHTML = '';
            
            Object.entries(metadata).forEach(([key, value]) => {{
                const item = document.createElement('div');
                item.className = 'data-item';
                const displayValue = value === null || value === undefined ? '-' : String(value);
                item.innerHTML = `
                    <div class="data-label">${{key}}</div>
                    <div class="data-value">${{displayValue}}</div>
                `;
                metadataGrid.appendChild(item);
            }});
            
            // Display raw EML data
            const rawEmlData = document.getElementById('rawEmlData');
            if (rawEml) {{
                rawEmlData.textContent = rawEml;
            }} else {{
                rawEmlData.textContent = 'No raw data available';
            }}
        }}
        
        function formatEmailAddresses(addresses) {{
            if (!addresses || addresses === 'N/A' || addresses === 'Unknown') {{
                return addresses;
            }}
            
            // Split by common email separators and clean up
            const emailList = addresses
                .split(/[,;]/)
                .map(email => email.trim())
                .filter(email => email.length > 0);
            
            if (emailList.length === 1) {{
                return formatSingleEmail(emailList[0]);
            }}
            
            // Return each email on its own line
            return emailList.map(email => `<div>${{formatSingleEmail(email)}}</div>`).join('');
        }}
        
        function formatSingleEmail(email) {{
            // Handle email formats like "John Doe <john@example.com>" or just "john@example.com"
            const emailRegex = /^(.+?)\s*<(.+?)>$/;
            const match = email.match(emailRegex);
            
            if (match) {{
                // Format: "Full Name <email@domain.com>"
                const name = match[1].trim();
                const emailAddress = match[2].trim();
                return `${{name}} <a href="mailto:${{emailAddress}}" style="color: #667eea; text-decoration: none;">${{emailAddress}}</a> <button onclick="copyToClipboard('${{emailAddress}}')" class="copy-btn" title="Copy email address">📋</button>`;
            }} else {{
                // Format: "email@domain.com" -> "email@domain.com"
                const emailAddress = email.trim();
                return `<a href="mailto:${{emailAddress}}" style="color: #667eea; text-decoration: none;">${{emailAddress}}</a> <button onclick="copyToClipboard('${{emailAddress}}')" class="copy-btn" title="Copy email address">📋</button>`;
            }}
        }}
        
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast('Copied to clipboard', event);
            }}).catch(err => {{
                console.error('Failed to copy: ', err);
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                showToast('Copied to clipboard', event);
            }});
        }}
        
        function showToast(message, event) {{
            // Remove any existing toast
            const existingToast = document.querySelector('.toast');
            if (existingToast) {{
                existingToast.remove();
            }}
            
            // Create new toast
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.textContent = message;
            document.body.appendChild(toast);
            
            // Position toast near mouse cursor
            const mouseX = event.clientX;
            const mouseY = event.clientY;
            const toastRect = toast.getBoundingClientRect();
            const windowWidth = window.innerWidth;
            const windowHeight = window.innerHeight;
            
            // Calculate position to keep toast within viewport
            let left = mouseX + 10;
            let top = mouseY - 10;
            
            // Adjust if toast would go off screen
            if (left + toastRect.width > windowWidth - 20) {{
                left = mouseX - toastRect.width - 10;
            }}
            
            if (top < 20) {{
                top = mouseY + 30;
            }}
            
            if (top + toastRect.height > windowHeight - 20) {{
                top = windowHeight - toastRect.height - 20;
            }}
            
            toast.style.left = left + 'px';
            toast.style.top = top + 'px';
            
            // Show toast with animation
            setTimeout(() => {{
                toast.classList.add('show');
            }}, 10);
            
            // Hide toast after 2 seconds
            setTimeout(() => {{
                toast.classList.remove('show');
                setTimeout(() => {{
                    if (toast.parentNode) {{
                        toast.remove();
                    }}
                }}, 300);
            }}, 2000);
        }}
        
        function formatFileSize(bytes) {{
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }}
    </script>
</body>
</html>
"""

# Error page template
ERROR_PAGE_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EML Reader - Error</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    {COMMON_STYLES}
</head>
<body>
    <div class="main-container">
        <div class="error-container">
            <div class="error-icon">❌</div>
            <h1 class="error-title">Error Occurred</h1>
            <div class="error-message">{{error_message}}</div>
            <a href="/" class="back-link">
                <span>←</span>
                Back to Home
            </a>
        </div>
    </div>
</body>
</html>
"""

# Not found page
NOT_FOUND_PAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EML Reader - Page Not Found</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    {COMMON_STYLES}
</head>
<body>
    <div class="main-container">
        <div class="error-container">
            <div class="error-icon">🔍</div>
            <h1 class="error-title">Page Not Found</h1>
            <div class="error-message">404: The requested page could not be found</div>
            <a href="/" class="back-link">
                <span>←</span>
                Back to Home
            </a>
        </div>
    </div>
</body>
</html>
"""
