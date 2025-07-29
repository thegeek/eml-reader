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
    
    .thread-info {
        display: flex;
        flex-direction: column;
        gap: 2rem;
    }
    
    .thread-summary {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .thread-summary-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #333;
    }
    
    .thread-subject {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
        flex: 1;
    }
    
    .thread-stats {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .thread-stat {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: #252525;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #e0e0e0;
    }
    
    .thread-timeline {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        position: relative;
    }
    
    .timeline-container {
        position: relative;
        padding: 2rem 0;
    }
    
    .timeline-axis {
        position: absolute;
        left: 50%;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 2px;
        transform: translateX(-50%);
    }
    
    .timeline-item {
        position: relative;
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
        width: 100%;
    }
    
    .timeline-item:nth-child(odd) {
        justify-content: flex-start;
    }
    
    .timeline-item:nth-child(even) {
        justify-content: flex-end;
    }
    
    .timeline-marker {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 2rem;
        height: 2rem;
        background: #667eea;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.9rem;
        z-index: 2;
        border: 3px solid #1a1a1a;
    }
    
    .timeline-item.root .timeline-marker {
        background: #00b894;
    }
    
    .timeline-item.latest .timeline-marker {
        background: #f39c12;
    }
    
    .timeline-content {
        width: 45%;
        background: #252525;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .timeline-item:nth-child(odd) .timeline-content {
        margin-right: 50%;
    }
    
    .timeline-item:nth-child(even) .timeline-content {
        margin-left: 50%;
    }
    
    .timeline-content:hover {
        border-color: #667eea;
        background: #2a2a2a;
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
    }
    
    .timeline-pointer {
        position: absolute;
        top: 50%;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        transform: translateY(-50%);
    }
    
    .timeline-item:nth-child(odd) .timeline-pointer {
        right: -16px;
        border-left-color: #252525;
    }
    
    .timeline-item:nth-child(even) .timeline-pointer {
        left: -16px;
        border-right-color: #252525;
    }
    
    .timeline-item:nth-child(odd) .timeline-content:hover .timeline-pointer {
        border-left-color: #2a2a2a;
    }
    
    .timeline-item:nth-child(even) .timeline-content:hover .timeline-pointer {
        border-right-color: #2a2a2a;
    }
    
    .message-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #333;
    }
    
    .sender {
        font-weight: 600;
        color: #ffffff;
        font-size: 1rem;
    }
    
    .message-date {
        color: #a0a0a0;
        font-size: 0.85rem;
    }
    
    .message-subject {
        color: #e0e0e0;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    .thread-indicators {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .reply-badge, .forward-badge, .depth-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .reply-badge {
        background: #00b894;
        color: white;
    }
    
    .forward-badge {
        background: #f39c12;
        color: white;
    }
    
    .depth-badge {
        background: #667eea;
        color: white;
    }
    
    .timeline-month-marker {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        background: white;
        color: #333;
        border-radius: 50%;
        width: 3rem;
        height: 3rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.8rem;
        z-index: 3;
        border: 3px solid #1a1a1a;
    }
    
    .timeline-month-marker .month {
        font-size: 0.7rem;
        line-height: 1;
    }
    
    .timeline-month-marker .year {
        font-size: 0.6rem;
        line-height: 1;
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
    
    .timeline-month-marker .year {
        font-size: 0.6rem;
        line-height: 1;
    }
    
    .thread-participants {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .participants-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .participant-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: #252525;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .participant-item:hover {
        background: #2a2a2a;
        border-color: #667eea;
    }
    
    .participant-email {
        color: #e0e0e0;
        font-weight: 500;
    }
    
    .message-count {
        background: #667eea;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .message-count:hover {
        background: #5a6fd8;
        transform: scale(1.05);
    }
    
    .message-count:active {
        transform: scale(0.95);
    }
    
    /* Modal styles */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
    }
    
    .modal-overlay.show {
        opacity: 1;
        visibility: visible;
    }
    
    .modal-content {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 16px;
        max-width: 90vw;
        max-height: 90vh;
        width: 800px;
        overflow: hidden;
        transform: scale(0.9);
        transition: all 0.3s ease;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    }
    
    .modal-overlay.show .modal-content {
        transform: scale(1);
    }
    
    .modal-header {
        background: #252525;
        padding: 1.5rem;
        border-bottom: 1px solid #333;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .modal-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    .modal-close {
        background: none;
        border: none;
        color: #a0a0a0;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .modal-close:hover {
        color: #ffffff;
        background: #333;
    }
    
    .modal-body {
        padding: 1.5rem;
        max-height: 70vh;
        overflow-y: auto;
    }
    
    .email-context {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .context-header {
        background: #252525;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .context-subject {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #333;
    }
    
    .context-meta {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .context-meta-row {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .context-meta-label {
        font-size: 0.8rem;
        color: #a0a0a0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .context-meta-value {
        color: #e0e0e0;
        font-weight: 500;
        word-wrap: break-word;
        overflow-wrap: break-word;
        line-height: 1.5;
        padding: 0.75rem;
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        min-height: 2.5rem;
    }
    
    .context-meta-value .copy-btn {
        display: inline-block;
        margin-left: 0.5rem;
        vertical-align: middle;
        flex-shrink: 0;
    }
    
    .context-meta-value:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    .context-meta-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .context-meta-grid .context-meta-row {
        margin-bottom: 0;
    }
    
    .context-body {
        background: #252525;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .context-body-title {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .context-body-title-left {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .style-switch {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        color: #a0a0a0;
    }
    
    .style-switch-btn {
        background: #333;
        border: 1px solid #555;
        color: #e0e0e0;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.3s ease;
    }
    
    .style-switch-btn:hover {
        background: #444;
        border-color: #666;
    }
    
    .style-switch-btn.active {
        background: #667eea;
        border-color: #667eea;
        color: white;
    }
    
    .context-body-content {
        background: #1a1a1a;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1rem;
        max-height: 300px;
        overflow-y: auto;
        font-family: 'JetBrains Mono', 'Fira Code', monospace;
        font-size: 0.9rem;
        line-height: 1.5;
        color: #e0e0e0;
    }
    
    .context-body-content.html {
        background: #1a1a1a;
        color: #e0e0e0;
    }
    
    .context-body-content.html.light {
        background: #ffffff;
        color: #333333;
        border-color: #ddd;
    }
    
    .context-body-content.text {
        white-space: pre-wrap;
        word-wrap: break-word;
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
                
                <!-- Thread Analysis Section -->
                <div class="accordion-item">
                    <div class="accordion-header" data-accordion="thread">
                        <div class="accordion-title">🧵 Thread Analysis</div>
                        <div class="accordion-icon">▼</div>
                    </div>
                    <div class="accordion-content" id="threadContent">
                        <div class="content-box">
                            <div class="content-box-title">🧵 Thread Information</div>
                            <div class="thread-info" id="threadInfo">
                                <div class="thread-summary" id="threadSummary"></div>
                                <div class="thread-timeline" id="threadTimeline"></div>
                                <div class="thread-participants" id="threadParticipants"></div>
                            </div>
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
    
    <!-- Email Context Modal -->
    <div class="modal-overlay" id="emailContextModal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title">📧 Email Context</div>
                <button class="modal-close" onclick="closeEmailContext()">×</button>
            </div>
            <div class="modal-body">
                <div class="email-context" id="emailContextContent">
                    <!-- Email context content will be populated here -->
                </div>
            </div>
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
                htmlContent.innerHTML = sanitizeHtml(data.body.html);
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
            
            // Display thread analysis
            displayThreadAnalysis(data);
        }}
        
        function displayThreadAnalysis(data) {{
            const threadSummary = document.getElementById('threadSummary');
            const threadTimeline = document.getElementById('threadTimeline');
            const threadParticipants = document.getElementById('threadParticipants');
            
            const threadAnalysis = data.thread_analysis;
            if (!threadAnalysis) {{
                threadSummary.innerHTML = '<div class="data-value empty">No thread analysis available</div>';
                threadTimeline.innerHTML = '<div class="data-value empty">No timeline available</div>';
                threadParticipants.innerHTML = '<div class="data-value empty">No participants available</div>';
                return;
            }}
            
            // Display thread summary
            const summary = threadAnalysis.subject_thread || {{}};
            const engagement = threadAnalysis.engagement_indicators || {{}};
            const headers = data.headers?.common || {{}};
            
            // Get meaningful subject
            const subject = summary.normalized || summary.original || headers.subject || 'No Subject';
            
            threadSummary.innerHTML = `
                <div class="thread-summary-header">
                    <div class="thread-subject">${{subject}}</div>
                    <div class="thread-stats">
                        <div class="thread-stat">
                            <span>📧</span>
                            <span>Depth: ${{threadAnalysis.thread_depth || 0}}</span>
                        </div>
                        <div class="thread-stat">
                            <span>👥</span>
                            <span>${{(threadAnalysis.thread_participants || []).length}} participants</span>
                        </div>
                        <div class="thread-stat">
                            <span>⭐</span>
                            <span>Engagement: ${{engagement.engagement_score || 0}}</span>
                        </div>
                    </div>
                </div>
                <div class="data-grid">
                    <div class="data-item">
                        <div class="data-label">Thread ID</div>
                        <div class="data-value">${{threadAnalysis.thread_id || 'Unknown'}}</div>
                    </div>
                    <div class="data-item">
                        <div class="data-label">Message Position</div>
                        <div class="data-value">${{threadAnalysis.thread_position || 1}}</div>
                    </div>
                    <div class="data-item">
                        <div class="data-label">Thread Type</div>
                        <div class="data-value">
                            ${{threadAnalysis.is_root ? '🌱 Root Message' : ''}}
                            ${{threadAnalysis.is_reply ? '↩️ Reply' : ''}}
                            ${{threadAnalysis.is_forward ? '↪️ Forward' : ''}}
                            ${{!threadAnalysis.is_root && !threadAnalysis.is_reply && !threadAnalysis.is_forward ? '📧 New Message' : ''}}
                        </div>
                    </div>
                    <div class="data-item">
                        <div class="data-label">Subject Analysis</div>
                        <div class="data-value">
                            ${{summary.has_re_prefix ? 'Re: ' : ''}}
                            ${{summary.has_fw_prefix ? 'Fw: ' : ''}}
                            ${{summary.has_aw_prefix ? 'Aw: ' : ''}}
                            ${{summary.prefix_count > 0 ? `(${{summary.prefix_count}} prefixes)` : ''}}
                            ${{!summary.has_re_prefix && !summary.has_fw_prefix && !summary.has_aw_prefix ? 'No prefixes' : ''}}
                        </div>
                    </div>
                </div>
            `;
            
            // Display thread timeline (simplified for single email)
            const timelineData = {{
                position: threadAnalysis.thread_position || 1,
                is_root: threadAnalysis.is_root || false,
                is_latest: true,
                email_data: data,
                thread_analysis: threadAnalysis
            }};
            
            threadTimeline.innerHTML = `
                <div class="timeline-container">
                    <div class="timeline-axis"></div>
                    
                    <!-- Month markers -->
                    <div class="timeline-month-marker" style="top: -1rem;">
                        <div class="month">JAN</div>
                        <div class="year">2024</div>
                    </div>
                    
                    <div class="timeline-item ${{timelineData.is_root ? 'root' : ''}} ${{timelineData.is_latest ? 'latest' : ''}}">
                        <div class="timeline-marker">${{timelineData.position}}</div>
                        <div class="timeline-content">
                            <div class="timeline-pointer"></div>
                            <div class="message-header">
                                <span class="sender">${{headers.from || 'Unknown Sender'}}</span>
                                <span class="message-date">${{headers.date || 'Unknown Date'}}</span>
                            </div>
                            <div class="message-subject">${{headers.subject || 'No Subject'}}</div>
                            <div class="thread-indicators">
                                ${{threadAnalysis.is_reply ? '<span class="reply-badge">↩️ Reply</span>' : ''}}
                                ${{threadAnalysis.is_forward ? '<span class="forward-badge">↪️ Forward</span>' : ''}}
                                <span class="depth-badge">Depth: ${{threadAnalysis.thread_depth || 0}}</span>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Additional month marker if needed -->
                    ${{threadAnalysis.thread_depth > 2 ? `
                    <div class="timeline-month-marker" style="bottom: -1rem;">
                        <div class="month">FEB</div>
                        <div class="year">2024</div>
                    </div>
                    ` : ''}}
                </div>
            `;
            
            // Display participants
            const participants = threadAnalysis.thread_participants || [];
            if (participants && participants.length > 0) {{
                threadParticipants.innerHTML = `
                    <div class="participants-list">
                        ${{participants.map((participant, index) => `
                            <div class="participant-item">
                                <div class="participant-email">${{formatEmailAddresses(participant)}}</div>
                                <div class="message-count" onclick="showEmailContext('${{participant}}', ${{index}})">1 message</div>
                            </div>
                        `).join('')}}
                    </div>
                `;
                
                // Store email data globally for modal access
                window.currentEmailData = data;
            }} else {{
                threadParticipants.innerHTML = '<div class="data-value empty">No participants found</div>';
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
            
            // For multiple emails, create a cleaner layout
            return emailList.map(email => `
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #333; margin-bottom: 0.5rem;">
                    <div style="flex: 1; min-width: 0;">
                        ${{formatSingleEmail(email)}}
                    </div>
                </div>
            `).join('');
        }}
        
        function formatSingleEmail(email) {{
            // Handle email formats like "John Doe <john@example.com>" or just "john@example.com"
            const emailRegex = /^(.+?)\s*<(.+?)>$/;
            const match = email.match(emailRegex);
            
            if (match) {{
                // Format: "Full Name <email@domain.com>"
                const name = match[1].trim();
                const emailAddress = match[2].trim();
                return `${{name}} <a href="mailto:${{emailAddress}}" style="color: #667eea; text-decoration: none;">${{emailAddress}}</a> <button onclick="copyToClipboard('${{emailAddress}}', event)" class="copy-btn" title="Copy email address">📋</button>`;
            }} else {{
                // Format: "email@domain.com" -> "email@domain.com"
                const emailAddress = email.trim();
                return `<a href="mailto:${{emailAddress}}" style="color: #667eea; text-decoration: none;">${{emailAddress}}</a> <button onclick="copyToClipboard('${{emailAddress}}', event)" class="copy-btn" title="Copy email address">📋</button>`;
            }}
        }}
        
        function copyToClipboard(text, event) {{
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
        
        function closeEmailContext() {{
            const modal = document.getElementById('emailContextModal');
            modal.classList.remove('show');
        }}
        
        function switchHtmlStyle(style) {{
            const htmlContent = document.getElementById('htmlContentArea');
            const darkBtn = document.querySelector('.style-switch-btn[onclick*="dark"]');
            const lightBtn = document.querySelector('.style-switch-btn[onclick*="light"]');
            
            if (!htmlContent) return;
            
            // Update button states
            if (style === 'dark') {{
                darkBtn.classList.add('active');
                lightBtn.classList.remove('active');
                htmlContent.classList.remove('light');
            }} else {{
                lightBtn.classList.add('active');
                darkBtn.classList.remove('active');
                htmlContent.classList.add('light');
            }}
        }}
        
        function showEmailContext(participantEmail, participantIndex) {{
            const modal = document.getElementById('emailContextModal');
            const content = document.getElementById('emailContextContent');
            
            // Get the current email data
            const emailData = window.currentEmailData;
            if (!emailData) {{
                console.error('No email data available');
                return;
            }}
            
            // Extract email address from participant (handle "Name <email>" format)
            const emailMatch = participantEmail.match(/<(.+?)>/);
            const emailAddress = emailMatch ? emailMatch[1] : participantEmail;
            
            // Create context content
            const headers = emailData.headers?.common || {{}};
            const body = emailData.body || {{}};
            const threadAnalysis = emailData.thread_analysis || {{}};
            
            content.innerHTML = `
                <div class="context-header">
                    <div class="context-subject">${{headers.subject || 'No Subject'}}</div>
                    <div class="context-meta">
                        <div class="context-meta-row">
                            <div class="context-meta-label">From</div>
                            <div class="context-meta-value">${{formatEmailAddresses(headers.from || 'Unknown')}}</div>
                        </div>
                        <div class="context-meta-row">
                            <div class="context-meta-label">To</div>
                            <div class="context-meta-value">${{formatEmailAddresses(headers.to || 'Unknown')}}</div>
                        </div>
                        <div class="context-meta-grid">
                            <div class="context-meta-row">
                                <div class="context-meta-label">Date</div>
                                <div class="context-meta-value">${{headers.date || 'Unknown'}}</div>
                            </div>
                            <div class="context-meta-row">
                                <div class="context-meta-label">Thread ID</div>
                                <div class="context-meta-value">${{threadAnalysis.thread_id || 'Unknown'}}</div>
                            </div>
                        </div>
                        <div class="context-meta-grid">
                            <div class="context-meta-row">
                                <div class="context-meta-label">Thread Depth</div>
                                <div class="context-meta-value">${{threadAnalysis.thread_depth || 0}}</div>
                            </div>
                            <div class="context-meta-row">
                                <div class="context-meta-label">Engagement Score</div>
                                <div class="context-meta-value">${{threadAnalysis.engagement_indicators?.engagement_score || 0}}</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                ${{body.html ? `
                <div class="context-body">
                    <div class="context-body-title">
                        <div class="context-body-title-left">
                            <span>📄</span>
                            <span>HTML Content</span>
                        </div>
                        <div class="style-switch">
                            <span>Style:</span>
                            <button class="style-switch-btn" onclick="switchHtmlStyle('dark')">Dark</button>
                            <button class="style-switch-btn active" onclick="switchHtmlStyle('light')">Light</button>
                        </div>
                    </div>
                    <div class="context-body-content html light" id="htmlContentArea">${{sanitizeHtml(body.html)}}</div>
                </div>
                ` : ''}}
                
                ${{body.text ? `
                <div class="context-body">
                    <div class="context-body-title">
                        <div class="context-body-title-left">
                            <span>📝</span>
                            <span>Text Content</span>
                        </div>
                    </div>
                    <div class="context-body-content text">${{escapeHtml(body.text)}}</div>
                </div>
                ` : ''}}
                
                ${{emailData.attachments && emailData.attachments.length > 0 ? `
                <div class="context-body">
                    <div class="context-body-title">
                        <div class="context-body-title-left">
                            <span>📎</span>
                            <span>Attachments (${{emailData.attachments.length}})</span>
                        </div>
                    </div>
                    <div class="context-body-content">
                        ${{emailData.attachments.map(attachment => `
                            <div style="margin-bottom: 0.5rem; padding: 0.5rem; background: #1a1a1a; border-radius: 4px;">
                                <strong>${{attachment.filename || 'Unnamed'}}</strong><br>
                                <small>${{attachment.content_type}} • ${{formatFileSize(attachment.size)}}</small>
                            </div>
                        `).join('')}}
                    </div>
                </div>
                ` : ''}}
            `;
            
            // Show modal
            modal.classList.add('show');
            
            // Close modal when clicking outside
            modal.addEventListener('click', function(e) {{
                if (e.target === modal) {{
                    closeEmailContext();
                }}
            }});
            
            // Close modal with Escape key
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'Escape') {{
                    closeEmailContext();
                }}
            }});
        }}
        
        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}
        
        function sanitizeHtml(html) {{
            if (!html) return '';
            
            // Create a temporary div to parse and sanitize HTML
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            
            // Handle CID image references
            const images = tempDiv.querySelectorAll('img');
            images.forEach(img => {{
                const src = img.getAttribute('src');
                if (src && src.startsWith('cid:')) {{
                    // Replace CID images with a placeholder
                    img.setAttribute('src', 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMzMzIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iI2FhYSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlPC90ZXh0Pjwvc3ZnPg==');
                    img.setAttribute('alt', 'Embedded image (CID: ' + src.substring(4) + ')');
                    img.style.border = '1px solid #333';
                    img.style.padding = '10px';
                    img.style.backgroundColor = '#1a1a1a';
                }}
            }});
            
            // Handle other potentially problematic elements
            const scripts = tempDiv.querySelectorAll('script');
            scripts.forEach(script => script.remove());
            
            const styles = tempDiv.querySelectorAll('style');
            styles.forEach(style => {{
                // Keep styles but sanitize them
                style.textContent = style.textContent.replace(/url\(/gi, 'url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjMzMzIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iI2FhYSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlPC90ZXh0Pjwvc3ZnPg==)');
            }});
            
            // Handle external links to prevent security issues
            const links = tempDiv.querySelectorAll('a');
            links.forEach(link => {{
                const href = link.getAttribute('href');
                if (href && (href.startsWith('javascript:') || href.startsWith('data:'))) {{
                    link.removeAttribute('href');
                    link.style.color = '#666';
                    link.style.textDecoration = 'line-through';
                }}
            }});
            
            return tempDiv.innerHTML;
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
