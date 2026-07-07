#!/usr/bin/env python3
"""
Simple H5P Viewer Server

Usage:
    python serve.py path/to/file.h5p [port]

Opens browser automatically after extracting and serving the H5P content.
"""

import http.server
import socketserver
import zipfile
import shutil
import sys
import os
import webbrowser
from pathlib import Path
import threading
import time

DEFAULT_PORT = 8080

def extract_h5p(h5p_path: Path, extract_to: Path):
    """Extract H5P file to target directory"""
    # Clean existing content
    if extract_to.exists():
        shutil.rmtree(extract_to)
    extract_to.mkdir(parents=True, exist_ok=True)

    # Extract ZIP
    with zipfile.ZipFile(h5p_path, 'r') as zf:
        zf.extractall(extract_to)

    print(f"Extracted to: {extract_to}")

def serve_directory(directory: Path, port: int):
    """Start HTTP server in directory"""
    os.chdir(directory)

    handler = http.server.SimpleHTTPRequestHandler
    handler.extensions_map.update({
        '.json': 'application/json',
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.svg': 'image/svg+xml',
    })

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at http://localhost:{port}")
        print(f"View H5P at: http://localhost:{port}/index.html")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()

def main():
    if len(sys.argv) < 2:
        print("Usage: python serve.py <path/to/file.h5p> [port]")
        print("\nExample:")
        print("  python serve.py ../test-output/4k-beispiele/02-scrum-rollen-v10.h5p")
        sys.exit(1)

    h5p_path = Path(sys.argv[1]).resolve()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT

    if not h5p_path.exists():
        print(f"Error: File not found: {h5p_path}")
        sys.exit(1)

    # Setup directories
    viewer_dir = Path(__file__).parent.resolve()
    content_dir = viewer_dir / "content"

    print(f"H5P File: {h5p_path}")
    print(f"Viewer Dir: {viewer_dir}")

    # Extract H5P content
    extract_h5p(h5p_path, content_dir)

    # Create a simple wrapper HTML that loads the content
    wrapper_html = f'''<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>H5P Preview: {h5p_path.stem}</title>
    <script src="https://cdn.jsdelivr.net/npm/h5p-standalone@3.6.0/dist/main.bundle.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            padding: 20px;
        }}
        .header {{
            max-width: 900px;
            margin: 0 auto 20px;
        }}
        h1 {{
            color: #1a1a1a;
            font-size: 22px;
            font-weight: 600;
        }}
        .subtitle {{
            color: #666;
            font-size: 14px;
            margin-top: 4px;
        }}
        #h5p-container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            padding: 24px;
            max-width: 900px;
            margin: 0 auto;
        }}
        .h5p-iframe-wrapper {{
            min-height: 500px;
        }}
        .status {{
            max-width: 900px;
            margin: 16px auto 0;
            padding: 12px 16px;
            background: #e8f5e9;
            border-radius: 8px;
            font-size: 13px;
            color: #2e7d32;
        }}
        .status.error {{
            background: #ffebee;
            color: #c62828;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{h5p_path.stem}</h1>
        <div class="subtitle">H5P Preview - {h5p_path.name}</div>
    </div>
    <div id="h5p-container"></div>
    <div class="status" id="status">Initializing...</div>

    <script>
        const el = document.getElementById('h5p-container');
        const status = document.getElementById('status');

        const options = {{
            h5pJsonPath: 'content',
            frameJs: 'https://cdn.jsdelivr.net/npm/h5p-standalone@3.6.0/dist/frame.bundle.js',
            frameCss: 'https://cdn.jsdelivr.net/npm/h5p-standalone@3.6.0/dist/styles/h5p.css',
        }};

        status.textContent = 'Loading H5P content...';

        new H5PStandalone.H5P(el, options)
            .then(() => {{
                status.textContent = 'Content loaded successfully';
            }})
            .catch(err => {{
                status.textContent = 'Error: ' + err.message;
                status.classList.add('error');
                console.error(err);
            }});
    </script>
</body>
</html>'''

    (viewer_dir / "preview.html").write_text(wrapper_html, encoding='utf-8')

    # Open browser after short delay
    url = f"http://localhost:{port}/preview.html"
    def open_browser():
        time.sleep(1)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    # Start server
    serve_directory(viewer_dir, port)

if __name__ == "__main__":
    main()
