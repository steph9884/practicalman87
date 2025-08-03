#!/usr/bin/env python3
"""
Web Server Interface for URL Obfuscation Tool
==============================================

A simple web interface for generating obfuscated URLs with live preview
and batch generation capabilities.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from url_obfuscator import URLObfuscator, URLTemplateEngine
import socket
import threading
import time


class ObfuscationHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the obfuscation web interface."""
    
    def __init__(self, *args, **kwargs):
        self.obfuscator = URLObfuscator()
        self.template_engine = URLTemplateEngine(self.obfuscator)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/index.html':
            self.serve_html()
        elif self.path == '/api/templates':
            self.serve_templates()
        elif self.path.startswith('/api/generate'):
            self.handle_generate_get()
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/api/generate':
            self.handle_generate_post()
        else:
            self.send_error(404)
    
    def serve_html(self):
        """Serve the main HTML interface."""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Obfuscation Tool</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1rem;
        }
        
        .main-content {
            padding: 40px;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-group textarea {
            height: 120px;
            resize: vertical;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #5a6268;
        }
        
        .results-section {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .results-section h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .url-result {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 10px;
            word-break: break-all;
            font-family: monospace;
            font-size: 14px;
        }
        
        .copy-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            margin-left: 10px;
        }
        
        .copy-btn:hover {
            background: #218838;
        }
        
        .templates-section {
            margin-top: 30px;
            padding: 20px;
            background: #e9ecef;
            border-radius: 8px;
        }
        
        .template-item {
            background: white;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 10px;
        }
        
        .template-name {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        
        .template-pattern {
            font-family: monospace;
            font-size: 12px;
            color: #6c757d;
            word-break: break-all;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #6c757d;
        }
        
        @media (max-width: 768px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .main-content {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔒 URL Obfuscation Tool</h1>
            <p>Generate obfuscated URLs with dynamic components for enhanced security</p>
        </div>
        
        <div class="main-content">
            <form id="obfuscationForm">
                <div class="form-grid">
                    <div>
                        <div class="form-group">
                            <label for="template">Template:</label>
                            <select id="template" name="template">
                                <option value="">Loading templates...</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="email">Email Address:</label>
                            <input type="email" id="email" name="email" value="user@example.com" required>
                        </div>
                        
                        <div class="form-group">
                            <label for="domain">Domain:</label>
                            <input type="text" id="domain" name="domain" value="mysite.com" required>
                        </div>
                    </div>
                    
                    <div>
                        <div class="form-group">
                            <label for="count">Number of URLs:</label>
                            <input type="number" id="count" name="count" value="1" min="1" max="100">
                        </div>
                        
                        <div class="form-group">
                            <label for="customTemplate">Custom Template (optional):</label>
                            <textarea id="customTemplate" name="customTemplate" 
                                     placeholder="https://{domain}/[[random_string(8)]]?id=[[base64_email]]"></textarea>
                        </div>
                    </div>
                </div>
                
                <div class="button-group">
                    <button type="submit" class="btn btn-primary">Generate URLs</button>
                    <button type="button" class="btn btn-secondary" onclick="clearResults()">Clear Results</button>
                    <button type="button" class="btn btn-secondary" onclick="showTemplates()">Show Templates</button>
                </div>
            </form>
            
            <div id="results" class="results-section" style="display: none;">
                <h3>Generated URLs:</h3>
                <div id="urlList"></div>
            </div>
            
            <div id="templates" class="templates-section" style="display: none;">
                <h3>Available Templates:</h3>
                <div id="templateList"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Load templates on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadTemplates();
        });
        
        // Load available templates
        async function loadTemplates() {
            try {
                const response = await fetch('/api/templates');
                const templates = await response.json();
                
                const select = document.getElementById('template');
                select.innerHTML = '<option value="">Select a template...</option>';
                
                for (const [name, pattern] of Object.entries(templates)) {
                    const option = document.createElement('option');
                    option.value = name;
                    option.textContent = name.replace('_', ' ').toUpperCase();
                    select.appendChild(option);
                }
            } catch (error) {
                console.error('Error loading templates:', error);
            }
        }
        
        // Handle form submission
        document.getElementById('obfuscationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            
            try {
                document.getElementById('results').style.display = 'block';
                document.getElementById('urlList').innerHTML = '<div class="loading">Generating URLs...</div>';
                
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                displayResults(result);
                
            } catch (error) {
                console.error('Error generating URLs:', error);
                document.getElementById('urlList').innerHTML = '<div class="loading">Error generating URLs</div>';
            }
        });
        
        // Display generated URLs
        function displayResults(urls) {
            const urlList = document.getElementById('urlList');
            urlList.innerHTML = '';
            
            urls.forEach((urlData, index) => {
                const urlDiv = document.createElement('div');
                urlDiv.className = 'url-result';
                urlDiv.innerHTML = `
                    <strong>URL ${index + 1}:</strong><br>
                    ${urlData.url}
                    <button class="copy-btn" onclick="copyToClipboard('${urlData.url.replace(/'/g, "\\'")}')">Copy</button>
                `;
                urlList.appendChild(urlDiv);
            });
        }
        
        // Show/hide templates
        function showTemplates() {
            const templatesDiv = document.getElementById('templates');
            if (templatesDiv.style.display === 'none') {
                loadTemplateDetails();
                templatesDiv.style.display = 'block';
            } else {
                templatesDiv.style.display = 'none';
            }
        }
        
        // Load template details
        async function loadTemplateDetails() {
            try {
                const response = await fetch('/api/templates');
                const templates = await response.json();
                
                const templateList = document.getElementById('templateList');
                templateList.innerHTML = '';
                
                for (const [name, pattern] of Object.entries(templates)) {
                    const templateDiv = document.createElement('div');
                    templateDiv.className = 'template-item';
                    templateDiv.innerHTML = `
                        <div class="template-name">${name.replace('_', ' ').toUpperCase()}</div>
                        <div class="template-pattern">${pattern}</div>
                    `;
                    templateList.appendChild(templateDiv);
                }
            } catch (error) {
                console.error('Error loading template details:', error);
            }
        }
        
        // Copy to clipboard
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                // Could add a toast notification here
                console.log('URL copied to clipboard');
            });
        }
        
        // Clear results
        function clearResults() {
            document.getElementById('results').style.display = 'none';
            document.getElementById('templates').style.display = 'none';
        }
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def serve_templates(self):
        """Serve available templates as JSON."""
        templates = self.template_engine.templates
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(templates, indent=2).encode('utf-8'))
    
    def handle_generate_get(self):
        """Handle GET request for URL generation."""
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        template = query_params.get('template', ['webmail_style'])[0]
        email = query_params.get('email', ['test@example.com'])[0]
        domain = query_params.get('domain', ['example.com'])[0]
        count = int(query_params.get('count', ['1'])[0])
        
        urls = self.generate_urls(template, email, domain, count)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(urls, indent=2).encode('utf-8'))
    
    def handle_generate_post(self):
        """Handle POST request for URL generation."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        
        template = data.get('template', 'webmail_style')
        custom_template = data.get('customTemplate', '')
        email = data.get('email', 'test@example.com')
        domain = data.get('domain', 'example.com')
        count = int(data.get('count', 1))
        
        if custom_template:
            template = custom_template
        
        urls = self.generate_urls(template, email, domain, count, custom_template != '')
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(urls, indent=2).encode('utf-8'))
    
    def generate_urls(self, template, email, domain, count, is_custom=False):
        """Generate obfuscated URLs."""
        urls = []
        
        for i in range(count):
            if is_custom:
                url = self.template_engine.process_template(template, email, domain)
            else:
                if template in self.template_engine.templates:
                    template_str = self.template_engine.templates[template]
                    url = self.template_engine.process_template(template_str, email, domain)
                else:
                    # Fallback to webmail_style
                    template_str = self.template_engine.templates['webmail_style']
                    url = self.template_engine.process_template(template_str, email, domain)
            
            urls.append({
                'url': url,
                'timestamp': time.time(),
                'template': template,
                'email': email,
                'domain': domain
            })
        
        return urls
    
    def log_message(self, format, *args):
        """Override to customize logging."""
        print(f"[{self.date_time_string()}] {format % args}")


def find_free_port(start_port=8080):
    """Find a free port starting from the given port."""
    port = start_port
    while port < start_port + 100:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1
    raise RuntimeError(f"No free port found in range {start_port}-{start_port + 100}")


def run_server(port=None):
    """Run the obfuscation web server."""
    if port is None:
        port = find_free_port()
    
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, ObfuscationHandler)
    
    print(f"🚀 URL Obfuscation Server running at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='URL Obfuscation Web Server')
    parser.add_argument('--port', '-p', type=int, help='Port to run the server on')
    args = parser.parse_args()
    
    run_server(args.port)