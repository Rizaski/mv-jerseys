#!/usr/bin/env python3
"""
Simple HTTP Server for Otomono Jerseys
Serves the static files and provides a local development environment
"""

import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    try:
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'buffer'):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass  # If encoding fix fails, continue anyway

# Configuration
PORT = 8000
HOST = 'localhost'

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve files with proper MIME types"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        # Custom log format
        print(f"[{self.log_date_time_string()}] {format % args}")

def start_server():
    """Start the HTTP server"""
    try:
        # Create server
        with socketserver.TCPServer((HOST, PORT), CustomHTTPRequestHandler) as httpd:
            print("=" * 60)
            print("🚀 Otomono Jerseys Development Server")
            print("=" * 60)
            print(f"📍 Server running at: http://{HOST}:{PORT}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print("=" * 60)
            print("🔗 Quick Links:")
            print(f"   • Main Site: http://{HOST}:{PORT}/index.html")
            print(f"   • Admin Panel: http://{HOST}:{PORT}/admin-panel.html")
            print(f"   • 🚨 FIX PERMISSIONS: http://{HOST}:{PORT}/firebase-rules-implementation.html")
            print(f"   • Firebase Setup Guide: http://{HOST}:{PORT}/firebase-setup-guide.html")
            print(f"   • Firebase Permissions Guide: http://{HOST}:{PORT}/firebase-permissions-guide.html")
            print(f"   • Order Test: http://{HOST}:{PORT}/quick-order-test.html")
            print(f"   • Full Test: http://{HOST}:{PORT}/test-order-saving.html")
            print(f"   • OrderManager Test: http://{HOST}:{PORT}/test-order-manager.html")
            print(f"   • Order Diagnostic: http://{HOST}:{PORT}/order-diagnostic.html")
            print(f"   • Firebase Test: http://{HOST}:{PORT}/firebase-test.html")
            print("=" * 60)
            print("💡 Press Ctrl+C to stop the server")
            print("=" * 60)
            
            # Try to open browser automatically
            try:
                webbrowser.open(f'http://{HOST}:{PORT}/quick-order-test.html')
                print("🌐 Browser opened automatically")
            except:
                print("⚠️  Could not open browser automatically")
            
            print("\n🔄 Server started successfully!")
            print("📝 Check the console for any errors or requests")
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Goodbye!")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: Port {PORT} is already in use")
            print(f"💡 Try a different port or stop the process using port {PORT}")
            print("🔧 Alternative: python server.py --port 8001")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

def check_files():
    """Check if required files exist"""
    required_files = [
        'index.html'
    ]
    
    optional_files = [
        'js/order-manager.js',
        'quick-order-test.html',
        'test-order-saving.html'
    ]
    
    missing_required = []
    missing_optional = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_required.append(file)
    
    for file in optional_files:
        if not os.path.exists(file):
            missing_optional.append(file)
    
    if missing_required:
        print("❌ Error: Required files are missing:")
        for file in missing_required:
            print(f"   • {file}")
        print("\n💡 Make sure you're running this from the project root directory")
        return False
    
    if missing_optional:
        print("⚠️  Note: Some optional files are missing (server will still start):")
        for file in missing_optional:
            print(f"   • {file}")
        print()
    
    return True

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--port' and len(sys.argv) > 2:
            try:
                PORT = int(sys.argv[2])
            except ValueError:
                print("❌ Error: Port must be a number")
                sys.exit(1)
        elif sys.argv[1] in ['-h', '--help']:
            print("Usage: python server.py [--port PORT]")
            print("  --port PORT    Use a specific port (default: 8000)")
            print("  -h, --help     Show this help message")
            sys.exit(0)
    
    # Check if we're in the right directory
    if not check_files():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Start the server
    start_server()
