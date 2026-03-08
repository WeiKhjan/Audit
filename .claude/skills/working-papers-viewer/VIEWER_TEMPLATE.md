# Viewer Templates

This file contains the complete templates for all 4 viewer files. When generating a viewer for a client engagement, copy these templates and replace the placeholders.

**Placeholders to replace:**
- `[CLIENT_NAME]` — e.g., "ACME SDN. BHD."
- `[COMPANY_NUMBER]` — e.g., "202401012345 (1550123-A)"
- `[FYE_DATE]` — e.g., "31 December 2025"
- `[FYE_YEAR]` — e.g., "2025"
- `[REPORTING_FRAMEWORK]` — e.g., "MPERS" or "MFRS"
- `[AUDITOR_FIRM]` — e.g., "ABC & Associates"

---

## 1. server.py

```python
"""
Audit Working Papers Viewer - Local Server
Serves static files, handles PUT requests to save .md file edits,
and proxies AI chat requests to the Anthropic API.
Usage: python server.py
"""

import http.server
import json
import os
import re
import urllib.request
import urllib.error
import glob as globmod
from datetime import datetime


class AuditViewerHandler(http.server.SimpleHTTPRequestHandler):

    def do_PUT(self):
        if self.path == '/api/master':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))

                master_path = os.path.join(os.getcwd(), 'master_data.json')

                if '_meta' in data:
                    data['_meta']['lastModified'] = datetime.now().isoformat()

                with open(master_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                self._send_json(200, {'status': 'ok'})

            except json.JSONDecodeError:
                self._send_json(400, {'error': 'Invalid JSON'})
            except Exception as e:
                self._send_json(500, {'error': str(e)})

        elif self.path == '/api/save':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))

                folder = data.get('folder', '')
                filename = data.get('file', '')
                content = data.get('content', '')

                # Validate folder name pattern (e.g. A_Planning, C_Assets)
                if not re.match(r'^[A-Z]_[A-Za-z_]+$', folder):
                    self._send_json(400, {'error': 'Invalid folder name'})
                    return

                # Validate filename pattern (e.g. A1_Planning_Memo.md)
                if not re.match(r'^[A-Za-z0-9_]+\.md$', filename):
                    self._send_json(400, {'error': 'Invalid filename'})
                    return

                filepath = os.path.join(os.getcwd(), folder, filename)

                # Only allow overwriting existing files
                if not os.path.exists(filepath):
                    self._send_json(404, {'error': 'File not found'})
                    return

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                self._send_json(200, {'status': 'ok'})

            except json.JSONDecodeError:
                self._send_json(400, {'error': 'Invalid JSON'})
            except Exception as e:
                self._send_json(500, {'error': str(e)})
        else:
            self._send_json(405, {'error': 'Method not allowed'})

    def do_POST(self):
        if self.path == '/api/chat':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode('utf-8'))

                api_key = data.get('apiKey', '')
                if not api_key:
                    self._send_json(400, {'error': 'API key is required'})
                    return

                # Build request payload for Anthropic API
                payload = {
                    'model': data.get('model', 'claude-sonnet-4-20250514'),
                    'max_tokens': data.get('max_tokens', 8192),
                    'messages': data.get('messages', []),
                }
                if data.get('system'):
                    payload['system'] = data['system']
                if data.get('tools'):
                    payload['tools'] = data['tools']

                req_body = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    'https://api.anthropic.com/v1/messages',
                    data=req_body,
                    headers={
                        'Content-Type': 'application/json',
                        'x-api-key': api_key,
                        'anthropic-version': '2023-06-01',
                    },
                    method='POST'
                )

                try:
                    with urllib.request.urlopen(req, timeout=120) as resp:
                        result = resp.read().decode('utf-8')
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(result.encode('utf-8'))
                except urllib.error.HTTPError as e:
                    error_body = e.read().decode('utf-8')
                    self._send_json(e.code, {'error': error_body})
                except urllib.error.URLError as e:
                    self._send_json(502, {'error': str(e.reason)})

            except json.JSONDecodeError:
                self._send_json(400, {'error': 'Invalid JSON'})
            except Exception as e:
                self._send_json(500, {'error': str(e)})
        else:
            self._send_json(405, {'error': 'Method not allowed'})

    def do_GET(self):
        if self.path == '/api/master':
            try:
                master_path = os.path.join(os.getcwd(), 'master_data.json')
                if os.path.exists(master_path):
                    with open(master_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self._send_json(200, data)
                else:
                    self._send_json(200, {
                        '_meta': {'version': '1.0'},
                        'variables': {},
                        'categories': {}
                    })
            except Exception as e:
                self._send_json(500, {'error': str(e)})

        elif self.path == '/api/files':
            try:
                files = []
                for folder in sorted(os.listdir('.')):
                    if os.path.isdir(folder) and re.match(r'^[A-Z]_', folder):
                        for fname in sorted(os.listdir(folder)):
                            if fname.endswith('.md'):
                                files.append({'folder': folder, 'file': fname})
                self._send_json(200, {'files': files})
            except Exception as e:
                self._send_json(500, {'error': str(e)})

        elif self.path == '/api/skills':
            try:
                skills_dir = os.path.join(os.getcwd(), '..', '..', '.claude', 'skills')
                skills_dir = os.path.normpath(skills_dir)
                result = []
                if os.path.isdir(skills_dir):
                    for name in sorted(os.listdir(skills_dir)):
                        skill_file = os.path.join(skills_dir, name, 'SKILL.md')
                        if os.path.isfile(skill_file):
                            with open(skill_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            lines = content.count('\n') + 1
                            # Extract first heading as display name
                            heading = name
                            for line in content.split('\n'):
                                if line.startswith('# '):
                                    heading = line[2:].strip()
                                    break
                            result.append({'id': name, 'name': heading, 'lines': lines})
                self._send_json(200, {'skills': result})
            except Exception as e:
                self._send_json(500, {'error': str(e)})

        elif self.path.startswith('/api/skills/'):
            try:
                skill_id = self.path[len('/api/skills/'):]
                if not re.match(r'^[a-z0-9-]+$', skill_id):
                    self._send_json(400, {'error': 'Invalid skill ID'})
                    return
                skills_dir = os.path.join(os.getcwd(), '..', '..', '.claude', 'skills')
                skill_file = os.path.normpath(os.path.join(skills_dir, skill_id, 'SKILL.md'))
                if not os.path.isfile(skill_file):
                    self._send_json(404, {'error': 'Skill not found'})
                    return
                with open(skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self._send_json(200, {'id': skill_id, 'content': content})
            except Exception as e:
                self._send_json(500, {'error': str(e)})
        else:
            super().do_GET()

    def end_headers(self):
        # Disable browser caching so viewer always loads fresh files
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def log_message(self, format, *args):
        # Log all requests
        super().log_message(format, *args)


if __name__ == '__main__':
    PORT = 8000
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = http.server.ThreadingHTTPServer(('', PORT), AuditViewerHandler)
    print(f'Audit Viewer Server running on http://localhost:{PORT}')
    print(f'Serving files from: {os.getcwd()}')
    print('Press Ctrl+C to stop.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
```

---

## 2. START_VIEWER.bat

```batch
@echo off
title Audit Working Papers Viewer - [CLIENT_NAME]
echo ============================================================
echo.
echo   [CLIENT_NAME]
echo   Company No: [COMPANY_NUMBER]
echo.
echo   AUDIT WORKING PAPERS
echo   Financial Year End: [FYE_DATE]
echo   Reporting Framework: [REPORTING_FRAMEWORK]
echo.
echo ============================================================
echo.
echo   DELIVERABLES:
echo   -------------
echo   [A]  Planning & Risk Assessment
echo   [B]  Internal Control
echo   [C]  Assets Testing
echo   [D]  Liabilities & Equity
echo   [E]  Income Statement
echo   [F]  Completion
echo   [G]  Outstanding Items
echo.
echo ============================================================
echo.
echo Starting local server...
echo.

cd /d "%~dp0"

:: Try to open browser after 2 seconds
start "" cmd /c "timeout /t 2 >nul && start http://localhost:8000/audit_viewer.html"

:: Start Python server
echo Server running at: http://localhost:8000/audit_viewer.html
echo.
echo Press Ctrl+C to stop the server when done.
echo ============================================================
echo.

python server.py

:: If Python fails, try python3
if %errorlevel% neq 0 (
    echo.
    echo Python not found. Trying python3...
    python3 server.py
)

:: If still fails, show error
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo ERROR: Python is not installed.
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo ============================================================
    pause
)
```

---

## 3. audit_viewer.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[CLIENT_NAME] - Audit Working Papers Viewer</title>
    <link rel="stylesheet" href="https://uicdn.toast.com/editor/3.2.2/toastui-editor.min.css" />
    <script src="https://uicdn.toast.com/editor/3.2.2/toastui-editor-all.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            height: 100vh;
            overflow: hidden;
            background: #f5f5f5;
        }
        #nav-panel {
            width: 320px;
            background: #1e293b;
            color: #e2e8f0;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        #nav-header {
            background: #0f172a;
            padding: 16px 20px;
            border-bottom: 1px solid #334155;
            display: flex;
            align-items: center;
            gap: 14px;
        }
        #nav-header img { width: 50px; height: 50px; object-fit: contain; }
        #nav-header .header-text { flex: 1; }
        #nav-header h1 { font-size: 14px; font-weight: 600; color: #60a5fa; margin-bottom: 4px; }
        #nav-header h2 { font-size: 11px; font-weight: 400; color: #94a3b8; }
        #search-box { padding: 12px 16px; background: #0f172a; }
        #search-input {
            width: 100%;
            padding: 8px 12px;
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 6px;
            color: #e2e8f0;
            font-size: 13px;
        }
        #search-input:focus { outline: none; border-color: #60a5fa; }
        #download-all-btn {
            margin: 12px 16px;
            padding: 10px 16px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.2s;
        }
        #download-all-btn:hover {
            background: linear-gradient(135deg, #059669 0%, #047857 100%);
            transform: translateY(-1px);
        }
        #download-all-btn:disabled {
            background: #6b7280;
            cursor: not-allowed;
            transform: none;
        }
        #master-data-btn { background: #7c3aed; display: flex; padding: 6px 12px; font-size: 11px; color: #fff; border: none; border-radius: 6px; cursor: pointer; align-items: center; justify-content: center; gap: 6px; margin: 6px 16px 0; font-weight: 500; transition: all 0.2s; }
        #master-data-btn:hover { background: #6d28d9; }
        #master-data-btn svg { width: 14px; height: 14px; }
        .master-editor { padding: 24px 40px; max-width: 800px; }
        .master-editor h2 { font-size: 20px; font-weight: 700; color: #1e293b; margin-bottom: 16px; }
        .master-tabs { display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap; }
        .master-tab { padding: 6px 14px; border: 1px solid #e2e8f0; border-radius: 6px; background: #f8fafc; cursor: pointer; font-size: 12px; font-weight: 500; color: #475569; transition: all 0.2s; }
        .master-tab.active { background: #7c3aed; color: #fff; border-color: #7c3aed; }
        .master-tab:hover:not(.active) { background: #f1f5f9; }
        .master-field { margin-bottom: 12px; }
        .master-field label { display: block; font-size: 11px; font-weight: 600; color: #64748b; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
        .master-field input { width: 100%; padding: 8px 12px; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 13px; color: #1e293b; transition: border-color 0.2s; }
        .master-field input:focus { outline: none; border-color: #7c3aed; box-shadow: 0 0 0 3px rgba(124,58,237,0.1); }
        .master-field .var-key { font-size: 10px; color: #94a3b8; font-family: monospace; margin-top: 2px; }
        .master-actions { display: flex; gap: 8px; margin-top: 20px; padding-top: 16px; border-top: 1px solid #e2e8f0; }
        .master-save-btn { padding: 8px 20px; background: #7c3aed; color: #fff; border: none; border-radius: 6px; font-size: 13px; font-weight: 500; cursor: pointer; }
        .master-save-btn:hover { background: #6d28d9; }
        .master-cancel-btn { padding: 8px 20px; background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 13px; cursor: pointer; }
        .master-cancel-btn:hover { background: #e2e8f0; }
        .master-add-section { margin-top: 16px; padding-top: 16px; border-top: 1px dashed #e2e8f0; }
        .master-add-btn { padding: 6px 14px; background: #f0fdf4; color: #15803d; border: 1px dashed #86efac; border-radius: 6px; font-size: 12px; cursor: pointer; }
        .master-add-btn:hover { background: #dcfce7; }
        .master-status { font-size: 12px; padding: 6px 12px; border-radius: 6px; display: none; }
        .master-status.saving { background: #fef3c7; color: #92400e; display: inline-block; }
        .master-status.saved { background: #d1fae5; color: #065f46; display: inline-block; }
        .master-status.error { background: #fee2e2; color: #991b1b; display: inline-block; }
        /* Inline variable editing */
        .var-inline {
            border-bottom: 2px solid #7c3aed;
            padding: 0 2px;
            border-radius: 1px;
            cursor: pointer;
            transition: all 0.15s;
        }
        .var-inline:hover {
            background: #ede9fe;
            border-bottom-color: #5b21b6;
        }
        /* Calculated/derived variable - teal underline */
        .var-calc {
            border-bottom-color: #0891b2 !important;
        }
        .var-calc:hover {
            background: #ecfeff !important;
            border-bottom-color: #0e7490 !important;
        }
        .var-calc-badge {
            display: inline-block;
            font-size: 9px;
            font-weight: 600;
            color: #0891b2;
            background: #ecfeff;
            border: 1px solid #cffafe;
            border-radius: 3px;
            padding: 0 4px;
            margin-left: 4px;
            vertical-align: middle;
            letter-spacing: 0.3px;
        }
        .var-formula-row {
            font-size: 11px;
            color: #0891b2;
            font-family: monospace;
            background: #f0fdfa;
            border: 1px solid #ccfbf1;
            border-radius: 5px;
            padding: 6px 10px;
            margin: 8px 0 4px;
            line-height: 1.6;
        }
        .var-formula-row .formula-label {
            font-size: 9px;
            font-weight: 600;
            color: #0e7490;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: block;
            margin-bottom: 2px;
        }
        .var-formula-row .formula-ref {
            color: #7c3aed;
            font-weight: 500;
        }
        .var-formula-row .formula-resolved {
            color: #64748b;
            font-size: 10px;
        }
        /* Popover color override for calc variables */
        .var-popover.popover-calc .var-popover-label {
            color: #0891b2;
        }
        .var-popover-readonly-value {
            background: #f0fdfa;
            border: 2px solid #99f6e4;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
            font-weight: 600;
            color: #0f766e;
            box-sizing: border-box;
        }
        .var-popover-readonly-hint {
            font-size: 10px;
            color: #94a3b8;
            margin-top: 8px;
            text-align: center;
        }
        .var-formula-row .formula-ref-link {
            color: #7c3aed;
            font-weight: 500;
            cursor: pointer;
            text-decoration: underline;
            text-decoration-style: dotted;
            text-underline-offset: 2px;
        }
        .var-formula-row .formula-ref-link:hover {
            color: #6d28d9;
            background: #f5f3ff;
            border-radius: 3px;
        }
        .var-popover {
            position: fixed;
            z-index: 3000;
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            padding: 16px;
            width: 340px;
        }
        .var-popover .var-popover-label {
            font-size: 11px;
            font-weight: 600;
            color: #7c3aed;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }
        .var-popover .var-popover-key {
            font-size: 10px;
            color: #94a3b8;
            font-family: monospace;
            margin-bottom: 10px;
        }
        .var-popover input {
            width: 100%;
            padding: 8px 12px;
            border: 2px solid #7c3aed;
            border-radius: 6px;
            font-size: 14px;
            color: #1e293b;
            outline: none;
            box-sizing: border-box;
        }
        .var-popover input:focus {
            box-shadow: 0 0 0 3px rgba(124,58,237,0.15);
        }
        .var-popover-actions {
            display: flex;
            gap: 8px;
            margin-top: 10px;
        }
        .var-popover-actions button {
            flex: 1;
            padding: 7px 12px;
            border: none;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s;
        }
        .var-popover .var-save { background: #7c3aed; color: #fff; }
        .var-popover .var-save:hover { background: #6d28d9; }
        .var-popover .var-cancel { background: #f1f5f9; color: #475569; }
        .var-popover .var-cancel:hover { background: #e2e8f0; }
        .var-toast {
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            z-index: 9999;
            animation: varToastIn 0.2s ease-out;
        }
        @keyframes varToastIn { from { opacity: 0; transform: translateX(-50%) translateY(10px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
        /* Variable context bar in edit mode */
        #var-context-bar {
            background: #f5f3ff;
            border-bottom: 1px solid #ddd6fe;
            padding: 8px 16px;
            font-size: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .var-chip {
            background: #ede9fe;
            color: #5b21b6;
            padding: 3px 10px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 11px;
            border: 1px solid #c4b5fd;
            white-space: nowrap;
            transition: all 0.15s;
        }
        .var-chip:hover { background: #ddd6fe; }
        #nav-content { flex: 1; overflow-y: auto; }
        .nav-section { border-bottom: 1px solid #334155; }
        .nav-section-header {
            display: flex;
            align-items: center;
            padding: 12px 16px;
            cursor: pointer;
            background: #1e293b;
            transition: background 0.2s;
        }
        .nav-section-header:hover { background: #334155; }
        .nav-section-header .icon {
            width: 24px; height: 24px;
            margin-right: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #374151;
            border-radius: 4px;
            color: #60a5fa;
            font-weight: 600;
            font-size: 11px;
        }
        .nav-section-header .title { flex: 1; font-size: 13px; font-weight: 500; }
        .nav-section-header .arrow { font-size: 10px; transition: transform 0.2s; color: #64748b; }
        .nav-section.expanded .arrow { transform: rotate(90deg); }
        .nav-section-items { display: none; background: #0f172a; }
        .nav-section.expanded .nav-section-items { display: block; }
        .nav-item {
            padding: 8px 16px 8px 50px;
            cursor: pointer;
            font-size: 12px;
            color: #94a3b8;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }
        .nav-item:hover { background: #1e293b; color: #e2e8f0; }
        .nav-item.active { background: #1e40af; color: #fff; border-left-color: #60a5fa; }
        #stats-bar { padding: 8px 16px; background: #0f172a; border-top: 1px solid #334155; font-size: 11px; color: #64748b; }
        #resizer { width: 4px; background: #334155; cursor: col-resize; }
        #resizer:hover { background: #60a5fa; }
        #preview-panel { flex: 1; display: flex; flex-direction: column; background: #fff; overflow: hidden; }
        #preview-header {
            padding: 16px 24px;
            background: #fff;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        #preview-header .breadcrumb { font-size: 12px; color: #64748b; }
        #preview-header .filename { font-size: 16px; font-weight: 600; color: #1e293b; }
        #preview-content { flex: 1; overflow-y: auto; padding: 24px 40px; }
        #preview-content h1 { font-size: 28px; font-weight: 700; color: #1e293b; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #e2e8f0; }
        #preview-content h2 { font-size: 22px; font-weight: 600; color: #334155; margin: 28px 0 12px; }
        #preview-content h3 { font-size: 18px; font-weight: 600; color: #475569; margin: 24px 0 10px; }
        #preview-content p { font-size: 14px; line-height: 1.7; color: #475569; margin-bottom: 12px; }
        #preview-content ul, #preview-content ol { margin: 12px 0 12px 24px; color: #475569; }
        #preview-content li { font-size: 14px; line-height: 1.7; margin-bottom: 4px; }
        #preview-content table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; }
        #preview-content th { background: #f1f5f9; padding: 10px 12px; text-align: left; font-weight: 600; color: #334155; border: 1px solid #e2e8f0; }
        #preview-content td { padding: 10px 12px; border: 1px solid #e2e8f0; color: #475569; }
        #preview-content tr:hover td { background: #f8fafc; }
        #preview-content code { background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-family: Consolas, Monaco, monospace; font-size: 13px; color: #e11d48; }
        #preview-content pre { background: #1e293b; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 16px 0; }
        #preview-content pre code { background: none; color: #e2e8f0; padding: 0; }
        #preview-content hr { border: none; border-top: 1px solid #e2e8f0; margin: 24px 0; }
        #preview-content strong { font-weight: 600; color: #1e293b; }
        .welcome { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #64748b; text-align: center; }
        .welcome h2 { font-size: 24px; color: #334155; margin-bottom: 12px; }
        /* Edit mode styles */
        .header-btn {
            padding: 6px 14px;
            border: none;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            display: none;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }
        #edit-btn { background: #f59e0b; color: #fff; }
        #edit-btn:hover { background: #d97706; }
        #save-btn { background: #10b981; color: #fff; }
        #save-btn:hover { background: #059669; }
        #cancel-btn { background: #6b7280; color: #fff; }
        #cancel-btn:hover { background: #4b5563; }
        #editor-container {
            flex: 1;
            overflow: hidden;
            display: none;
        }
        #editor-container .toastui-editor-defaultUI {
            border: none;
            height: 100% !important;
        }
        #editor-container .toastui-editor-defaultUI .toastui-editor-toolbar {
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
        }
        #editor-container .toastui-editor-contents {
            padding: 24px 40px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
        }
        #editor-container .toastui-editor-contents table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 12px;
        }
        #editor-container .toastui-editor-contents th {
            background: #f1f5f9;
            padding: 10px 12px;
            text-align: left;
            font-weight: 600;
            color: #334155;
            border: 1px solid #e2e8f0;
        }
        #editor-container .toastui-editor-contents td {
            padding: 10px 12px;
            border: 1px solid #e2e8f0;
            color: #475569;
        }
        #editor-container .toastui-editor-contents h1 {
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #e2e8f0;
        }
        #editor-container .toastui-editor-contents h2 {
            font-size: 20px;
            font-weight: 600;
            color: #334155;
            margin: 24px 0 12px;
        }
        #editor-container .toastui-editor-contents h3 {
            font-size: 16px;
            font-weight: 600;
            color: #475569;
            margin: 20px 0 10px;
        }
        .toastui-editor-mode-switch {
            display: none !important;
        }
        .save-status {
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 4px;
            display: none;
        }
        .save-status.saving { background: #fef3c7; color: #92400e; display: inline-block; }
        .save-status.saved { background: #d1fae5; color: #065f46; display: inline-block; }
        .save-status.error { background: #fee2e2; color: #991b1b; display: inline-block; }
        /* Sign-off panel styles */
        #signoff-panel {
            margin-top: 32px;
            padding: 20px;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }
        #signoff-panel h3 {
            font-size: 15px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e2e8f0;
        }
        .signoff-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
            flex-wrap: wrap;
        }
        .signoff-row label {
            font-size: 13px;
            font-weight: 600;
            color: #475569;
            width: 75px;
            flex-shrink: 0;
        }
        .signoff-row input {
            padding: 6px 10px;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            font-size: 12px;
            color: #1e293b;
            background: #fff;
        }
        .signoff-row input[type="text"] { width: 160px; }
        .signoff-row input[type="date"] { width: 140px; }
        .signoff-row button {
            padding: 6px 14px;
            background: #3b82f6;
            color: #fff;
            border: none;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
        }
        .signoff-row button:hover { background: #2563eb; }
        .signoff-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 12px;
            background: #d1fae5;
            color: #065f46;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
        }
        .signoff-badge svg { width: 14px; height: 14px; }
        .review-history { margin-top: 16px; }
        .review-history h4 { font-size: 13px; color: #475569; margin-bottom: 8px; }
        .review-history table { font-size: 12px; width: 100%; }
        .review-history th { background: #f1f5f9; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
        /* Nav action buttons */
        .nav-actions { padding: 8px 16px; background: #0f172a; display: flex; gap: 6px; flex-wrap: wrap; }
        .nav-action-btn {
            flex: 1; min-width: 120px; padding: 7px 10px; border: none; border-radius: 5px;
            font-size: 11px; font-weight: 500; cursor: pointer; display: flex;
            align-items: center; justify-content: center; gap: 5px; transition: all 0.2s; color: #fff;
        }
        .nav-action-btn svg { width: 14px; height: 14px; flex-shrink: 0; }
        #bulk-signoff-btn { background: #7c3aed; }
        #bulk-signoff-btn:hover { background: #6d28d9; }
        #review-summary-btn { background: #0891b2; }
        #review-summary-btn:hover { background: #0e7490; }
        /* Review note highlights */
        .review-note-highlight {
            background: #fef9c3; border-bottom: 2px solid #f59e0b; cursor: pointer; position: relative;
            transition: background 0.2s;
        }
        .review-note-highlight:hover { background: #fde68a; }
        .review-note-highlight.resolved { background: #d1fae5; border-bottom-color: #10b981; }
        .review-note-indicator {
            display: inline-flex; align-items: center; justify-content: center;
            width: 16px; height: 16px; background: #f59e0b; color: #fff; border-radius: 50%;
            font-size: 9px; font-weight: 700; margin-left: 2px; vertical-align: super; line-height: 1;
        }
        .review-note-highlight.resolved .review-note-indicator { background: #10b981; }
        /* Add note popup */
        .add-note-popup {
            position: fixed; z-index: 1000; background: #1e293b; color: #fff; padding: 6px 12px;
            border-radius: 6px; font-size: 12px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            display: flex; align-items: center; gap: 5px; transition: background 0.2s;
        }
        .add-note-popup:hover { background: #334155; }
        .add-note-popup svg { width: 14px; height: 14px; }
        /* Modal overlay (shared) */
        .modal-overlay {
            position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5);
            z-index: 2000; display: flex; align-items: center; justify-content: center;
            animation: fadeIn 0.15s ease-out;
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .modal-content {
            background: #fff; border-radius: 12px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-height: 85vh; overflow-y: auto; width: 90%; animation: slideUp 0.2s ease-out;
        }
        @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .modal-sm { max-width: 500px; }
        .modal-lg { max-width: 900px; }
        .modal-header {
            display: flex; align-items: center; justify-content: space-between; padding: 16px 20px;
            border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; background: #fff; z-index: 1;
            border-radius: 12px 12px 0 0;
        }
        .modal-header h3 { font-size: 16px; font-weight: 600; color: #1e293b; }
        .modal-close {
            width: 28px; height: 28px; border: none; background: #f1f5f9; border-radius: 6px;
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            color: #64748b; font-size: 16px; transition: all 0.2s;
        }
        .modal-close:hover { background: #e2e8f0; color: #1e293b; }
        .modal-body { padding: 20px; }
        .modal-footer {
            display: flex; justify-content: flex-end; gap: 8px; padding: 16px 20px;
            border-top: 1px solid #e2e8f0;
        }
        .modal-footer button, .modal-body button.action-btn {
            padding: 8px 16px; border: none; border-radius: 6px; font-size: 13px;
            font-weight: 500; cursor: pointer; transition: all 0.2s;
        }
        .btn-primary { background: #3b82f6; color: #fff; }
        .btn-primary:hover { background: #2563eb; }
        .btn-danger { background: #ef4444; color: #fff; }
        .btn-danger:hover { background: #dc2626; }
        .btn-secondary { background: #f1f5f9; color: #475569; }
        .btn-secondary:hover { background: #e2e8f0; }
        .btn-success { background: #10b981; color: #fff; }
        .btn-success:hover { background: #059669; }
        .btn-purple { background: #7c3aed; color: #fff; }
        .btn-purple:hover { background: #6d28d9; }
        /* Modal form fields */
        .modal-field { margin-bottom: 14px; }
        .modal-field label { display: block; font-size: 12px; font-weight: 600; color: #475569; margin-bottom: 4px; }
        .modal-field input, .modal-field textarea, .modal-field select {
            width: 100%; padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px;
            font-size: 13px; color: #1e293b; background: #fff;
        }
        .modal-field textarea { min-height: 80px; resize: vertical; font-family: inherit; }
        .modal-field input:focus, .modal-field textarea:focus, .modal-field select:focus { outline: none; border-color: #3b82f6; }
        .modal-field .selected-text {
            background: #fef9c3; padding: 8px 12px; border-radius: 6px; font-size: 13px;
            color: #92400e; border: 1px solid #fde68a; max-height: 60px; overflow-y: auto;
        }
        /* Review notes summary panel */
        #review-notes-panel {
            margin-top: 24px; padding: 16px; background: #fffbeb; border: 1px solid #fde68a;
            border-radius: 8px;
        }
        #review-notes-panel h3 {
            font-size: 14px; font-weight: 600; color: #92400e; margin-bottom: 12px;
            display: flex; align-items: center; justify-content: space-between;
        }
        .rn-filter-tabs { display: flex; gap: 4px; margin-bottom: 10px; }
        .rn-filter-tab {
            padding: 4px 10px; border: 1px solid #d1d5db; border-radius: 4px; font-size: 11px;
            cursor: pointer; background: #fff; color: #475569; transition: all 0.2s;
        }
        .rn-filter-tab.active { background: #f59e0b; color: #fff; border-color: #f59e0b; }
        .rn-table { width: 100%; border-collapse: collapse; font-size: 12px; }
        .rn-table th { background: #fef3c7; padding: 8px 10px; text-align: left; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #92400e; border: 1px solid #fde68a; }
        .rn-table td { padding: 8px 10px; border: 1px solid #fde68a; color: #475569; vertical-align: top; }
        .rn-table tr:hover td { background: #fef9c3; }
        .rn-status { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; text-transform: uppercase; }
        .rn-status-open { background: #fef3c7; color: #92400e; }
        .rn-status-resolved { background: #d1fae5; color: #065f46; }
        .rn-actions { display: flex; gap: 4px; }
        .rn-actions button { padding: 3px 8px; border: none; border-radius: 3px; font-size: 10px; cursor: pointer; }
        .rn-goto { background: #e0f2fe; color: #0369a1; }
        .rn-goto:hover { background: #bae6fd; }
        .rn-delete { background: #fee2e2; color: #991b1b; }
        .rn-delete:hover { background: #fecaca; }
        .rn-truncate { max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; vertical-align: middle; }
        /* Bulk signoff table */
        .bs-table { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 12px; }
        .bs-table th { background: #f1f5f9; padding: 8px 10px; text-align: left; font-size: 11px; border: 1px solid #e2e8f0; }
        .bs-table td { padding: 6px 10px; border: 1px solid #e2e8f0; }
        .bs-table tr:hover td { background: #f8fafc; }
        .bs-table input[type="checkbox"] { width: 16px; height: 16px; cursor: pointer; }
        .bs-progress { margin-top: 12px; }
        .bs-progress-bar { height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden; }
        .bs-progress-fill { height: 100%; background: #7c3aed; border-radius: 3px; transition: width 0.3s; }
        .bs-progress-text { font-size: 11px; color: #64748b; margin-top: 4px; }
        .bs-role-select { display: flex; gap: 8px; margin-bottom: 12px; }
        .bs-role-btn {
            padding: 6px 16px; border: 2px solid #d1d5db; border-radius: 6px; font-size: 12px;
            font-weight: 500; cursor: pointer; background: #fff; color: #475569; transition: all 0.2s;
        }
        .bs-role-btn.active { border-color: #7c3aed; background: #f5f3ff; color: #7c3aed; }
        /* AI Chat Widget */
        .ai-chat-toggle {
            position: fixed; bottom: 24px; right: 24px; width: 56px; height: 56px;
            border-radius: 50%; border: none; cursor: pointer; z-index: 9999;
            background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
            color: #fff; font-size: 18px; font-weight: 700;
            box-shadow: 0 4px 16px rgba(79,70,229,0.4);
            transition: all 0.3s; display: flex; align-items: center; justify-content: center;
        }
        .ai-chat-toggle:hover { transform: scale(1.1); box-shadow: 0 6px 24px rgba(79,70,229,0.5); }
        .ai-chat-toggle.active { background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%); box-shadow: 0 4px 16px rgba(220,38,38,0.4); }
        #ai-chat-panel {
            position: fixed; bottom: 90px; right: 24px; width: 420px; height: 560px; max-height: calc(100vh - 110px);
            background: #fff; border-radius: 16px; z-index: 9998;
            box-shadow: 0 8px 40px rgba(0,0,0,0.2); display: flex; flex-direction: column;
            overflow: hidden; border: 1px solid #e2e8f0;
        }
        .ai-chat-header {
            background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
            color: #fff; padding: 14px 16px; display: flex; align-items: center; gap: 10px;
            font-size: 14px; font-weight: 600;
        }
        .ai-chat-header span:first-child { flex: 1; }
        .ai-chat-header button {
            background: rgba(255,255,255,0.2); border: none; color: #fff;
            width: 30px; height: 30px; border-radius: 6px; cursor: pointer;
            font-size: 14px; display: flex; align-items: center; justify-content: center;
            transition: background 0.2s;
        }
        .ai-chat-header button:hover { background: rgba(255,255,255,0.35); }
        #ai-chat-messages {
            flex: 1; overflow-y: auto; padding: 16px; display: flex;
            flex-direction: column; gap: 12px; background: #f8fafc;
        }
        .ai-msg { max-width: 85%; padding: 10px 14px; border-radius: 12px; font-size: 13px; line-height: 1.6; word-wrap: break-word; }
        .ai-msg-user { align-self: flex-end; background: #4f46e5; color: #fff; border-bottom-right-radius: 4px; }
        .ai-msg-assistant { align-self: flex-start; background: #fff; color: #334155; border: 1px solid #e2e8f0; border-bottom-left-radius: 4px; }
        .ai-msg-assistant p { margin-bottom: 8px; }
        .ai-msg-assistant p:last-child { margin-bottom: 0; }
        .ai-msg-assistant code { background: #f1f5f9; padding: 1px 4px; border-radius: 3px; font-size: 12px; }
        .ai-msg-assistant ul, .ai-msg-assistant ol { margin: 4px 0 4px 18px; }
        .ai-msg-tool {
            align-self: center; background: #f0fdf4; border: 1px solid #bbf7d0;
            color: #166534; padding: 6px 12px; border-radius: 20px;
            font-size: 11px; font-weight: 500; display: flex; align-items: center; gap: 6px;
        }
        .ai-msg-tool .tool-spinner { width: 12px; height: 12px; border: 2px solid #bbf7d0; border-top-color: #166534; border-radius: 50%; animation: spin 0.8s linear infinite; }
        .ai-msg-error { align-self: center; background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; padding: 8px 14px; border-radius: 8px; font-size: 12px; }
        .ai-chat-input-area {
            padding: 12px; border-top: 1px solid #e2e8f0; background: #fff;
            display: flex; gap: 8px; align-items: flex-end;
        }
        #ai-input {
            flex: 1; border: 1px solid #d1d5db; border-radius: 10px;
            padding: 10px 14px; font-size: 13px; resize: none;
            min-height: 40px; max-height: 100px; font-family: inherit;
            outline: none; transition: border-color 0.2s;
        }
        #ai-input:focus { border-color: #7c3aed; }
        #ai-send-btn {
            width: 40px; height: 40px; border-radius: 10px; border: none;
            background: #4f46e5; color: #fff; cursor: pointer;
            display: flex; align-items: center; justify-content: center;
            transition: background 0.2s; flex-shrink: 0;
        }
        #ai-send-btn:hover { background: #4338ca; }
        #ai-send-btn:disabled { background: #9ca3af; cursor: not-allowed; }
        .ai-typing { display: flex; gap: 4px; padding: 12px 14px; align-self: flex-start; }
        .ai-typing span { width: 8px; height: 8px; background: #94a3b8; border-radius: 50%; animation: aiBounce 1.4s ease-in-out infinite; }
        .ai-typing span:nth-child(2) { animation-delay: 0.2s; }
        .ai-typing span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes aiBounce { 0%,80%,100% { transform: scale(0); } 40% { transform: scale(1); } }
        @keyframes spin { to { transform: rotate(360deg); } }
        .ai-welcome { text-align: center; color: #94a3b8; padding: 40px 20px; font-size: 13px; line-height: 1.8; }
        .ai-welcome h3 { color: #475569; font-size: 16px; margin-bottom: 8px; }
        .ai-actions { display: flex; gap: 6px; padding: 0 12px 8px; background: #fff; }
        .ai-action-btn { font-size: 11px; padding: 4px 10px; border: 1px solid #d1d5db; border-radius: 14px; background: #fff; color: #64748b; cursor: pointer; transition: all 0.2s; }
        .ai-action-btn:hover { border-color: #7c3aed; color: #7c3aed; background: #f5f3ff; }
        .ai-skills-bar { display: flex; flex-wrap: wrap; gap: 4px; padding: 8px 12px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
        .ai-skill-chip { font-size: 11px; padding: 3px 10px; border: 1px solid #d1d5db; border-radius: 14px; background: #fff; color: #64748b; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
        .ai-skill-chip:hover { border-color: #7c3aed; color: #7c3aed; }
        .ai-skill-chip.active { background: #7c3aed; color: #fff; border-color: #7c3aed; }
        .ai-skill-chip.more-btn { font-style: italic; color: #94a3b8; border-style: dashed; }
        .ai-skill-chip.more-btn:hover { color: #7c3aed; border-color: #7c3aed; }
        @media print { #nav-panel, #resizer { display: none; } #preview-panel { width: 100%; } #signoff-panel button, #signoff-panel input { display: none; } .review-note-highlight { background: #fef9c3 !important; -webkit-print-color-adjust: exact; } .add-note-popup, .modal-overlay, .ai-chat-toggle, #ai-chat-panel { display: none !important; } }
    </style>
</head>
<body>
    <div id="nav-panel">
        <div id="nav-header">
            <div class="header-text">
                <h1>[CLIENT_NAME]</h1>
                <h2>FYE [FYE_YEAR] - Audit Working Papers</h2>
            </div>
        </div>
        <div id="search-box">
            <input type="text" id="search-input" placeholder="Search files... (Ctrl+F)">
        </div>
        <div class="nav-actions">
            <button id="bulk-signoff-btn" class="nav-action-btn" onclick="openBulkSignoff()">
                <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
                Bulk Sign-Off
            </button>
            <button id="review-summary-btn" class="nav-action-btn" onclick="openCrossFileReviewSummary()">
                <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
                Review Notes
            </button>
        </div>
        <button id="download-all-btn" onclick="downloadAllDocuments()">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
            </svg>
            Download All Working Papers
        </button>
        <button id="master-data-btn" onclick="showMasterDataEditor()">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2 1 3 3 3h10c2 0 3-1 3-3V7M9 3h6l1 4H8L9 3zM8 11h8M8 15h5" />
            </svg>
            Master Data
        </button>
        <div id="nav-content"></div>
        <div id="stats-bar">Loading...</div>
    </div>
    <div id="resizer"></div>
    <div id="preview-panel">
        <div id="preview-header">
            <span class="breadcrumb">Select a file from the navigation</span>
            <span class="filename" style="flex:1;"></span>
            <span id="save-status" class="save-status"></span>
            <button id="edit-btn" class="header-btn" onclick="enterEditMode()">Edit</button>
            <button id="save-btn" class="header-btn" onclick="saveFile()">Save</button>
            <button id="cancel-btn" class="header-btn" onclick="cancelEdit()">Cancel</button>
        </div>
        <div id="editor-container" style="display:none; flex:1; overflow:hidden;"></div>
        <div id="preview-content">
            <div class="welcome">
                <h2>Audit Working Papers Viewer</h2>
                <p>[CLIENT_NAME] ([COMPANY_NUMBER])</p>
                <p>Financial Year End: [FYE_DATE]</p>
                <p>Reporting Framework: [REPORTING_FRAMEWORK]</p>
                <br>
                <p style="font-size:12px; color:#94a3b8;">
                    <strong>Audit Sections:</strong><br>
                    A - Planning & Risk Assessment<br>
                    B - Internal Control<br>
                    C - Assets Testing<br>
                    D - Liabilities & Equity<br>
                    E - Income Statement<br>
                    F - Completion<br>
                    G - Outstanding Items
                </p>
            </div>
        </div>
    </div>

<script>
// ========== MASTER DATA VARIABLE SYSTEM ==========
var masterData = null;
var lastViewedFile = null;

fetch('/api/master')
    .then(function(r) { return r.json(); })
    .then(function(data) { masterData = data; })
    .catch(function() { masterData = { _meta: {}, variables: {}, categories: {} }; });

function formatNumber(num) {
    return Math.abs(num).toLocaleString('en-MY', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatValue(value, defaultFormat, modifier) {
    var fmt = modifier || defaultFormat || 'text';
    if (fmt === 'text' || typeof value === 'string') return String(value);
    var num = Number(value);
    if (isNaN(num)) return String(value);
    switch (fmt) {
        case 'currency': return formatNumber(num);
        case 'rm': return 'RM ' + formatNumber(num);
        case 'currency_bracket': case 'bracket':
            return num < 0 ? '(' + formatNumber(num) + ')' : formatNumber(num);
        case 'rm_bracket':
            return num < 0 ? 'RM (' + formatNumber(num) + ')' : 'RM ' + formatNumber(num);
        case 'currency_nil': case 'nil':
            return num === 0 ? 'NIL' : formatNumber(num);
        case 'raw': return String(num);
        default: return String(value);
    }
}

function substituteVariables(markdown, interactive) {
    if (!masterData || !masterData.variables) return markdown;
    return markdown.replace(/\{\{([^}|]+?)(?:\|([^}]+?))?\}\}/g, function(match, varName, modifier) {
        varName = varName.replace(/\\_/g, '_').replace(/\\/g, '');
        if (modifier) modifier = modifier.replace(/\\_/g, '_').replace(/\\/g, '');
        var varDef = masterData.variables[varName];
        if (!varDef) return match;
        var val = formatValue(varDef.value, varDef.format, modifier);
        if (interactive) {
            return '\x01VSTART:' + varName + '\x01' + val + '\x01VEND\x01';
        }
        return val;
    });
}

function wrapVariableMarkers(html) {
    return html.replace(/\x01VSTART:(\w+)\x01(.*?)\x01VEND\x01/g, function(match, varName, val) {
        var varDef = masterData && masterData.variables ? masterData.variables[varName] : null;
        var label = varDef ? varDef.label : varName;
        var isCalc = varDef && varDef.formula;
        var cls = 'var-inline' + (isCalc ? ' var-calc' : '');
        var titlePrefix = isCalc ? 'Calculated: ' : 'Click to edit: ';
        return '<span class="' + cls + '" data-var="' + varName + '" title="' + titlePrefix + label + '">' + val + '</span>';
    });
}

// ========== INLINE VARIABLE EDITING ==========

var activeVarPopover = null;

function attachVariableClickHandlers() {
    document.querySelectorAll('#preview-content .var-inline').forEach(function(el) {
        el.addEventListener('click', function(e) {
            e.stopPropagation();
            openVarPopover(this);
        });
    });
}

function resolveFormulaDisplay(formula, clickable) {
    if (!masterData || !masterData.variables || !formula) return '';
    var html = formula.replace(/([a-z][a-z0-9_]+)/g, function(m, ref) {
        var v = masterData.variables[ref];
        if (!v) return ref;
        var fmtVal = formatValue(v.value, v.format);
        if (clickable) {
            return '<span class="formula-ref-link" data-formula-var="' + ref + '">' + v.label + '</span> <span class="formula-resolved">(' + fmtVal + ')</span>';
        }
        return '<span class="formula-ref">' + v.label + '</span> <span class="formula-resolved">(' + fmtVal + ')</span>';
    });
    html = html.replace(/ \* /g, ' &times; ').replace(/ \/ /g, ' &divide; ').replace(/ \+ /g, ' + ').replace(/ - /g, ' &minus; ');
    return html;
}

function openVarPopover(el) {
    closeVarPopover();
    var varName = el.getAttribute('data-var');
    var varDef = masterData.variables[varName];
    if (!varDef) return;

    var isCalc = !!varDef.formula;
    var rect = el.getBoundingClientRect();
    var popover = document.createElement('div');
    popover.className = 'var-popover' + (isCalc ? ' popover-calc' : '');
    var inputType = (typeof varDef.value === 'number') ? 'number' : 'text';
    var inputStep = (typeof varDef.value === 'number') ? ' step="0.01"' : '';
    var catLabel = (masterData.categories && masterData.categories[varDef.category]) ? masterData.categories[varDef.category].label : varDef.category;

    var calcBadge = isCalc ? ' <span class="var-calc-badge">CALC</span>' : '';

    if (isCalc) {
        var displayVal = formatValue(varDef.value, varDef.format);
        popover.innerHTML =
            '<div class="var-popover-label">' + varDef.label + calcBadge + '</div>' +
            '<div class="var-popover-key">{{' + varName + '}} &middot; ' + catLabel + '</div>' +
            '<div class="var-popover-readonly-value">' + displayVal + '</div>' +
            '<div class="var-formula-row">' +
                '<span class="formula-label">Formula</span>' +
                resolveFormulaDisplay(varDef.formula, true) +
            '</div>' +
            '<div class="var-popover-readonly-hint">Calculated field &mdash; edit the source variables above</div>';
    } else {
        popover.innerHTML =
            '<div class="var-popover-label">' + varDef.label + '</div>' +
            '<div class="var-popover-key">{{' + varName + '}} &middot; ' + catLabel + '</div>' +
            '<input type="' + inputType + '" value="' + String(varDef.value).replace(/"/g, '&quot;') + '"' + inputStep + ' />' +
            '<div class="var-popover-actions">' +
                '<button class="var-save">Save</button>' +
                '<button class="var-cancel">Cancel</button>' +
            '</div>';
    }

    var top = rect.bottom + 8;
    if (top + 180 > window.innerHeight) top = rect.top - 180;
    popover.style.top = top + 'px';
    popover.style.left = Math.max(8, Math.min(rect.left, window.innerWidth - 360)) + 'px';

    document.body.appendChild(popover);
    activeVarPopover = popover;

    if (isCalc) {
        popover.querySelectorAll('.formula-ref-link').forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.stopPropagation();
                var refVar = this.getAttribute('data-formula-var');
                var target = document.querySelector('.var-inline[data-var="' + refVar + '"]');
                if (target) {
                    closeVarPopover();
                    target.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    target.style.transition = 'background 0.3s';
                    target.style.background = '#fef3c7';
                    setTimeout(function() {
                        openVarPopover(target);
                        target.style.background = '';
                    }, 400);
                }
            });
        });
        document.addEventListener('keydown', function handler(e) {
            if (e.key === 'Escape') { closeVarPopover(); document.removeEventListener('keydown', handler); }
        });
    } else {
        var input = popover.querySelector('input');
        input.focus();
        input.select();

        popover.querySelector('.var-save').onclick = function() {
            saveVariableInline(varName, input.value, varDef);
        };
        popover.querySelector('.var-cancel').onclick = closeVarPopover;

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') saveVariableInline(varName, input.value, varDef);
            if (e.key === 'Escape') closeVarPopover();
        });
    }
}

function closeVarPopover() {
    if (activeVarPopover) {
        activeVarPopover.remove();
        activeVarPopover = null;
    }
}

document.addEventListener('click', function(e) {
    if (activeVarPopover && !activeVarPopover.contains(e.target) && !e.target.classList.contains('var-inline')) {
        closeVarPopover();
    }
});

function saveVariableInline(varName, newValue, varDef) {
    if (typeof varDef.value === 'number') {
        masterData.variables[varName].value = parseFloat(newValue) || 0;
    } else {
        masterData.variables[varName].value = newValue;
    }

    if (masterData._meta) masterData._meta.lastModified = new Date().toISOString();

    fetch('/api/master', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(masterData)
    })
    .then(function(r) {
        if (!r.ok) throw new Error('Save failed');
        return r.json();
    })
    .then(function() {
        closeVarPopover();
        if (currentFile.content) {
            var scrollPos = document.getElementById('preview-content').scrollTop;
            var parsed = parseFileContent(currentFile.content);
            document.getElementById('preview-content').innerHTML = wrapVariableMarkers(marked.parse(substituteVariables(parsed.docContent, true)));
            if (parsed.reviewNotes.length > 0) applyReviewNoteHighlights(parsed.reviewNotes);
            renderReviewNoteSummary(parsed.reviewNotes);
            renderSignoffPanel(parsed.signoff);
            attachSelectionListener();
            attachVariableClickHandlers();
            document.getElementById('preview-content').scrollTop = scrollPos;
        }
        showVarToast('Updated: ' + varDef.label, 'success');
    })
    .catch(function(err) {
        showVarToast('Error: ' + err.message, 'error');
    });
}

function showVarToast(message, type) {
    var existing = document.querySelector('.var-toast');
    if (existing) existing.remove();
    var toast = document.createElement('div');
    toast.className = 'var-toast';
    toast.style.background = type === 'success' ? '#d1fae5' : '#fee2e2';
    toast.style.color = type === 'success' ? '#065f46' : '#991b1b';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(function() { toast.remove(); }, 2500);
}

function showVariableContextBar() {
    var existing = document.getElementById('var-context-bar');
    if (existing) existing.remove();

    if (!masterData || !masterData.variables) return;

    var md = currentFile.content || '';
    var vars = [];
    var seen = {};
    var re = /\{\{(\w+)(?:\|\w+)?\}\}/g;
    var m;
    while ((m = re.exec(md)) !== null) {
        if (!seen[m[1]] && masterData.variables[m[1]]) {
            seen[m[1]] = true;
            vars.push(m[1]);
        }
    }
    if (vars.length === 0) return;

    var bar = document.createElement('div');
    bar.id = 'var-context-bar';
    bar.innerHTML = '<span style="color:#7c3aed;font-weight:600;font-size:11px;white-space:nowrap;">VARIABLES:</span>';

    vars.forEach(function(varName) {
        var v = masterData.variables[varName];
        var chip = document.createElement('span');
        chip.className = 'var-chip';
        var displayVal = formatValue(v.value, v.format);
        if (displayVal.length > 25) displayVal = displayVal.substring(0, 22) + '...';
        chip.textContent = v.label + ': ' + displayVal;
        chip.title = '{{' + varName + '}} - Click to edit';
        chip.setAttribute('data-var', varName);
        chip.onclick = function() { openVarPopover(chip); };
        bar.appendChild(chip);
    });

    var editorContainer = document.getElementById('editor-container');
    var toolbar = editorContainer.querySelector('.toastui-editor-toolbar');
    if (toolbar) {
        toolbar.parentNode.insertBefore(bar, toolbar.nextSibling);
    }
}

function showMasterDataEditor() {
    if (isEditMode) {
        if (!confirm('You have unsaved changes. Discard?')) return;
        cancelEdit();
    }
    document.querySelectorAll('.nav-item').forEach(function(item) { item.classList.remove('active'); });
    if (currentFile && currentFile.folder) lastViewedFile = { folder: currentFile.folder, name: currentFile.name, display: currentFile.display };
    currentFile = { folder: '', name: '', display: '', content: '' };

    document.getElementById('edit-btn').style.display = 'none';
    document.querySelector('#preview-header .breadcrumb').textContent = 'System /';
    document.querySelector('#preview-header .filename').textContent = 'Master Data Variables';

    if (!masterData || !masterData.variables) {
        document.getElementById('preview-content').innerHTML = '<div class="master-editor"><p>No master_data.json found. Master data will be created when you save.</p></div>';
        return;
    }

    var cats = masterData.categories || {};
    var sortedCats = Object.keys(cats).sort(function(a, b) { return (cats[a].order || 99) - (cats[b].order || 99); });
    if (sortedCats.length === 0) sortedCats = ['general'];

    var activeTab = sortedCats[0];
    var html = '<div class="master-editor">';
    html += '<h2>Master Data Variables</h2>';
    html += '<p style="color:#64748b;font-size:13px;margin-bottom:16px;">Edit shared data that appears across all working papers. Changes propagate automatically.</p>';
    html += '<span id="master-save-status" class="master-status"></span>';
    html += '<div class="master-tabs" id="master-tabs">';
    sortedCats.forEach(function(catKey, i) {
        var label = cats[catKey] ? cats[catKey].label : catKey;
        html += '<div class="master-tab' + (i === 0 ? ' active' : '') + '" data-cat="' + catKey + '" onclick="switchMasterTab(\'' + catKey + '\')">' + label + '</div>';
    });
    html += '</div>';

    sortedCats.forEach(function(catKey, i) {
        html += '<div class="master-cat-panel" id="master-cat-' + catKey + '" style="display:' + (i === 0 ? 'block' : 'none') + ';">';
        Object.keys(masterData.variables).forEach(function(varKey) {
            var v = masterData.variables[varKey];
            if (v.category !== catKey) return;
            var displayVal = v.value;
            html += '<div class="master-field">';
            html += '<label>' + v.label + '</label>';
            html += '<input type="' + (typeof v.value === 'number' ? 'number' : 'text') + '" data-var="' + varKey + '" value="' + String(displayVal).replace(/"/g, '&quot;') + '"' + (typeof v.value === 'number' ? ' step="0.01"' : '') + ' />';
            html += '<div class="var-key">{{' + varKey + '}}</div>';
            html += '</div>';
        });
        html += '<div class="master-add-section">';
        html += '<button class="master-add-btn" onclick="addMasterVariable(\'' + catKey + '\')">+ Add Variable to ' + (cats[catKey] ? cats[catKey].label : catKey) + '</button>';
        html += '</div>';
        html += '</div>';
    });

    html += '<div class="master-actions">';
    html += '<button class="master-save-btn" onclick="saveMasterData()">Save All Changes</button>';
    html += '<button class="master-cancel-btn" onclick="cancelMasterEditor()">Cancel</button>';
    html += '</div>';
    html += '</div>';

    document.getElementById('preview-content').innerHTML = html;
}

function switchMasterTab(catKey) {
    document.querySelectorAll('.master-tab').forEach(function(t) { t.classList.remove('active'); });
    document.querySelector('.master-tab[data-cat="' + catKey + '"]').classList.add('active');
    document.querySelectorAll('.master-cat-panel').forEach(function(p) { p.style.display = 'none'; });
    document.getElementById('master-cat-' + catKey).style.display = 'block';
}

function addMasterVariable(category) {
    var varKey = prompt('Variable key (snake_case, e.g., total_assets):');
    if (!varKey || !/^\w+$/.test(varKey)) return;
    if (masterData.variables[varKey]) { alert('Variable already exists.'); return; }
    var label = prompt('Display label (e.g., Total Assets):');
    if (!label) return;
    var fmt = prompt('Format (text, currency, currency_bracket, currency_nil):', 'text');
    var value = fmt !== 'text' ? 0 : '';

    masterData.variables[varKey] = { value: value, label: label, category: category, format: fmt || 'text' };
    showMasterDataEditor();
    switchMasterTab(category);
}

function saveMasterData() {
    var statusEl = document.getElementById('master-save-status');
    statusEl.className = 'master-status saving';
    statusEl.textContent = 'Saving...';

    document.querySelectorAll('.master-field input[data-var]').forEach(function(input) {
        var varKey = input.getAttribute('data-var');
        if (masterData.variables[varKey]) {
            var v = masterData.variables[varKey];
            if (typeof v.value === 'number') {
                v.value = parseFloat(input.value) || 0;
            } else {
                v.value = input.value;
            }
        }
    });

    fetch('/api/master', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(masterData)
    })
    .then(function(r) {
        if (!r.ok) throw new Error('Save failed');
        return r.json();
    })
    .then(function() {
        statusEl.className = 'master-status saved';
        statusEl.textContent = 'Saved - all working papers will reflect updated values';
        setTimeout(function() { statusEl.className = 'master-status'; }, 3000);
    })
    .catch(function(err) {
        statusEl.className = 'master-status error';
        statusEl.textContent = 'Error: ' + err.message;
    });
}

function cancelMasterEditor() {
    if (lastViewedFile) {
        loadFile(lastViewedFile.folder, lastViewedFile.name, lastViewedFile.display);
    } else {
        document.getElementById('preview-content').innerHTML = '<div class="welcome"><h2>Audit Working Papers Viewer</h2><p>Select a file from the navigation</p></div>';
        document.querySelector('#preview-header .breadcrumb').textContent = 'Select a file from the navigation';
        document.querySelector('#preview-header .filename').textContent = '';
    }
}

// ========== END MASTER DATA ==========

// ========== SECTIONS - AUTO-DISCOVERED FROM SERVER ==========

var SECTION_TITLES = {
    'A_Planning': 'A - Planning & Risk Assessment',
    'B_Internal_Control': 'B - Internal Control',
    'C_Assets': 'C - Assets',
    'D_Liabilities_Equity': 'D - Liabilities & Equity',
    'E_Income_Statement': 'E - Income Statement',
    'F_Completion': 'F - Completion',
    'G_Outstanding': 'G - Outstanding Items'
};

function folderToTitle(folder) {
    if (SECTION_TITLES[folder]) return SECTION_TITLES[folder];
    var parts = folder.split('_');
    var icon = parts[0] || '';
    return icon + ' - ' + parts.slice(1).join(' ');
}

function fileToDisplay(filename) {
    var base = filename.replace(/\.md$/, '');
    var parts = base.split('_');
    var index = parts[0] || '';
    var rest = parts.slice(1).join(' ');
    return index + ' - ' + rest;
}

var sections = [];
var allFiles = [];
var navContent = document.getElementById('nav-content');
var totalFiles = 0;
var currentFile = { folder: '', name: '', display: '', content: '' };

function buildSidebar(fileList) {
    navContent.innerHTML = '';
    sections = [];
    allFiles = [];
    totalFiles = 0;

    var grouped = {};
    var folderOrder = [];
    fileList.forEach(function(f) {
        if (!grouped[f.folder]) {
            grouped[f.folder] = [];
            folderOrder.push(f.folder);
        }
        grouped[f.folder].push(f.file);
    });

    folderOrder.forEach(function(folder) {
        var icon = folder.charAt(0);
        var title = folderToTitle(folder);
        var files = grouped[folder].map(function(fname) {
            return { name: fname, display: fileToDisplay(fname) };
        });
        var sec = { id: folder, icon: icon, title: title, files: files };
        sections.push(sec);

        var sectionEl = document.createElement('div');
        sectionEl.className = 'nav-section';
        sectionEl.setAttribute('data-folder', folder);

        var header = document.createElement('div');
        header.className = 'nav-section-header';
        header.innerHTML = '<span class="icon">' + icon + '</span><span class="title">' + title + '</span><span class="arrow">&#9658;</span>';
        header.onclick = function() { sectionEl.classList.toggle('expanded'); };

        var items = document.createElement('div');
        items.className = 'nav-section-items';

        files.forEach(function(file) {
            var item = document.createElement('div');
            item.className = 'nav-item';
            item.textContent = file.display;
            item.setAttribute('data-folder', folder);
            item.setAttribute('data-file', file.name);
            item.onclick = function() { loadFile(folder, file.name, file.display); };
            items.appendChild(item);
            allFiles.push({ folder: folder, name: file.name, display: file.display, element: item });
            totalFiles++;
        });

        sectionEl.appendChild(header);
        sectionEl.appendChild(items);
        navContent.appendChild(sectionEl);
    });

    document.getElementById('stats-bar').textContent = totalFiles + ' documents in ' + sections.length + ' sections';
    var firstSection = document.querySelector('.nav-section');
    if (firstSection) firstSection.classList.add('expanded');
}

// Fetch file list from server and build sidebar dynamically
fetch('/api/files')
    .then(function(r) { return r.json(); })
    .then(function(data) { buildSidebar(data.files || []); })
    .catch(function() {
        document.getElementById('stats-bar').textContent = 'Could not load file list from server';
    });

function loadFile(folder, filename, displayName) {
    if (isEditMode) {
        if (!confirm('You have unsaved changes. Discard and switch files?')) return;
        cancelEdit();
    }
    document.querySelectorAll('.nav-item').forEach(function(item) { item.classList.remove('active'); });
    var activeItem = document.querySelector('.nav-item[data-folder="' + folder + '"][data-file="' + filename + '"]');
    if (activeItem) activeItem.classList.add('active');

    var section = document.querySelector('.nav-section[data-folder="' + folder + '"]');
    if (section) section.classList.add('expanded');

    document.getElementById('preview-header').querySelector('.breadcrumb').textContent = folder + ' /';
    document.getElementById('preview-header').querySelector('.filename').textContent = displayName;
    document.getElementById('preview-content').innerHTML = '<div class="welcome"><p>Loading...</p></div>';
    document.getElementById('edit-btn').style.display = 'none';

    if (isEditMode) cancelEdit();

    currentFile = { folder: folder, name: filename, display: displayName, content: '' };

    fetch(folder + '/' + filename + '?t=' + Date.now())
        .then(function(response) {
            if (!response.ok) throw new Error('File not found');
            return response.text();
        })
        .then(function(markdown) {
            currentFile.content = markdown;
            var parsed = parseFileContent(markdown);
            document.getElementById('preview-content').innerHTML = wrapVariableMarkers(marked.parse(substituteVariables(parsed.docContent, true)));
            document.getElementById('edit-btn').style.display = 'flex';
            if (parsed.reviewNotes.length > 0) {
                applyReviewNoteHighlights(parsed.reviewNotes);
            }
            renderReviewNoteSummary(parsed.reviewNotes);
            renderSignoffPanel(parsed.signoff);
            attachSelectionListener();
            attachVariableClickHandlers();
        })
        .catch(function(error) {
            document.getElementById('preview-content').innerHTML = '<div class="welcome"><h2>Cannot Load File</h2><p>Run START_VIEWER.bat to view files.</p></div>';
            document.getElementById('edit-btn').style.display = 'none';
        });
}

// ========== CONTENT PARSING (unified) ==========

function parseFileContent(markdown) {
    var signoff = null;
    var reviewNotes = [];
    var clean = markdown;
    var signoffMatch = clean.match(/\n*<!-- SIGNOFF:([\s\S]*?) -->/);
    if (signoffMatch) {
        try { signoff = JSON.parse(signoffMatch[1]); } catch(e) {}
        clean = clean.replace(signoffMatch[0], '');
    }
    var notesMatch = clean.match(/\n*<!-- REVIEWNOTES:([\s\S]*?) -->/);
    if (notesMatch) {
        try { reviewNotes = JSON.parse(notesMatch[1]); } catch(e) {}
        clean = clean.replace(notesMatch[0], '');
    }
    return { docContent: clean.trim(), signoff: signoff, reviewNotes: reviewNotes };
}

function buildFileContent(docContent, signoff, reviewNotes) {
    var content = docContent;
    if (reviewNotes && reviewNotes.length > 0) {
        content += '\n\n<!-- REVIEWNOTES:' + JSON.stringify(reviewNotes) + ' -->';
    }
    if (signoff) {
        content += '\n\n<!-- SIGNOFF:' + JSON.stringify(signoff) + ' -->';
    }
    return content;
}

function extractSignoff(markdown) { return parseFileContent(markdown).signoff; }
function extractDocContent(markdown) { return parseFileContent(markdown).docContent; }

function todayStr() {
    var d = new Date();
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}

function escapeHtml(str) {
    var div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
}

function renderSignoffPanel(signoffData) {
    var existing = document.getElementById('signoff-panel');
    if (existing) existing.remove();

    var panel = document.createElement('div');
    panel.id = 'signoff-panel';
    var data = signoffData || { preparer: null, reviews: [] };

    var html = '<h3>Sign-Off Record</h3>';

    if (data.preparer && data.preparer.name) {
        html += '<div class="signoff-row">';
        html += '<label>Preparer:</label>';
        html += '<span class="signoff-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 13l4 4L19 7"/></svg> ' + escapeHtml(data.preparer.name) + ' &mdash; ' + escapeHtml(data.preparer.date) + '</span>';
        html += '</div>';
    } else {
        html += '<div class="signoff-row">';
        html += '<label>Preparer:</label>';
        html += '<input type="text" id="preparer-name" placeholder="Name">';
        html += '<input type="date" id="preparer-date" value="' + todayStr() + '">';
        html += '<button onclick="signOffPreparer()">Sign Off</button>';
        html += '</div>';
    }

    html += '<div class="signoff-row">';
    html += '<label>Reviewer:</label>';
    html += '<input type="text" id="reviewer-name" placeholder="Reviewer name">';
    html += '<input type="date" id="reviewer-date" value="' + todayStr() + '">';
    html += '<input type="text" id="reviewer-note" placeholder="Note (optional)" style="width:180px;">';
    html += '<button onclick="signOffReviewer()">Sign Off</button>';
    html += '</div>';

    if (data.reviews && data.reviews.length > 0) {
        html += '<div class="review-history">';
        html += '<h4>Review History</h4>';
        html += '<table><thead><tr><th>#</th><th>Reviewer</th><th>Date</th><th>Note</th></tr></thead><tbody>';
        for (var i = 0; i < data.reviews.length; i++) {
            var r = data.reviews[i];
            html += '<tr><td>' + (i + 1) + '</td><td>' + escapeHtml(r.name) + '</td><td>' + escapeHtml(r.date) + '</td><td>' + escapeHtml(r.note) + '</td></tr>';
        }
        html += '</tbody></table></div>';
    }

    panel.innerHTML = html;
    document.getElementById('preview-content').appendChild(panel);
}

function signOffPreparer() {
    var name = document.getElementById('preparer-name').value.trim();
    var date = document.getElementById('preparer-date').value;
    if (!name) { alert('Please enter preparer name.'); return; }
    if (!date) { alert('Please enter date.'); return; }

    var signoffData = extractSignoff(currentFile.content) || { preparer: null, reviews: [] };
    signoffData.preparer = { name: name, date: date };
    saveSignoff(signoffData);
}

function signOffReviewer() {
    var name = document.getElementById('reviewer-name').value.trim();
    var date = document.getElementById('reviewer-date').value;
    var note = document.getElementById('reviewer-note').value.trim();
    if (!name) { alert('Please enter reviewer name.'); return; }
    if (!date) { alert('Please enter date.'); return; }

    var signoffData = extractSignoff(currentFile.content) || { preparer: null, reviews: [] };
    signoffData.reviews.push({ name: name, date: date, note: note });
    saveSignoff(signoffData);
}

function saveSignoff(signoffData) {
    var parsed = parseFileContent(currentFile.content);
    var fullContent = buildFileContent(parsed.docContent, signoffData, parsed.reviewNotes);

    fetch('/api/save', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            folder: currentFile.folder,
            file: currentFile.name,
            content: fullContent
        })
    })
    .then(function(response) {
        if (!response.ok) throw new Error('Save failed');
        return response.json();
    })
    .then(function() {
        currentFile.content = fullContent;
        renderSignoffPanel(signoffData);
    })
    .catch(function(err) {
        alert('Failed to save sign-off: ' + err.message);
    });
}

// ========== EDIT MODE FUNCTIONS ==========

var isEditMode = false;
var tuiEditor = null;

function enterEditMode() {
    if (!currentFile.content) return;
    isEditMode = true;
    removeAddNotePopup();

    var editableContent = parseFileContent(currentFile.content).docContent;

    document.getElementById('editor-container').style.display = 'block';
    document.getElementById('preview-content').style.display = 'none';

    if (tuiEditor) { tuiEditor.destroy(); tuiEditor = null; }

    tuiEditor = new toastui.Editor({
        el: document.getElementById('editor-container'),
        height: '100%',
        initialEditType: 'wysiwyg',
        initialValue: editableContent,
        hideModeSwitch: true,
        usageStatistics: false,
        toolbarItems: [
            ['heading', 'bold', 'italic', 'strike'],
            ['hr', 'quote'],
            ['ul', 'ol', 'task'],
            ['table', 'link'],
            ['code', 'codeblock']
        ]
    });

    if (masterData && masterData.variables && Object.keys(masterData.variables).length > 0) {
        var toolbar = document.querySelector('#editor-container .toastui-editor-toolbar');
        if (toolbar) {
            var varBtn = document.createElement('button');
            varBtn.textContent = '{{x}} Insert Variable';
            varBtn.style.cssText = 'margin-left:8px;padding:4px 10px;background:#7c3aed;color:#fff;border:none;border-radius:4px;font-size:11px;cursor:pointer;';
            varBtn.onclick = function() {
                var cats = masterData.categories || {};
                var options = [];
                Object.keys(masterData.variables).forEach(function(k) {
                    var v = masterData.variables[k];
                    options.push(k + ' - ' + v.label + ' (' + (cats[v.category] ? cats[v.category].label : v.category) + ')');
                });
                var choice = prompt('Select variable (type number):\n' + options.map(function(o, i) { return (i+1) + '. ' + o; }).join('\n'));
                if (choice) {
                    var idx = parseInt(choice) - 1;
                    var keys = Object.keys(masterData.variables);
                    if (idx >= 0 && idx < keys.length) {
                        tuiEditor.insertText('{{' + keys[idx] + '}}');
                    }
                }
            };
            toolbar.appendChild(varBtn);
        }
    }

    document.getElementById('edit-btn').style.display = 'none';
    document.getElementById('save-btn').style.display = 'flex';
    document.getElementById('cancel-btn').style.display = 'flex';

    showVariableContextBar();
}

function cancelEdit() {
    isEditMode = false;

    if (tuiEditor) { tuiEditor.destroy(); tuiEditor = null; }
    document.getElementById('editor-container').innerHTML = '';
    document.getElementById('editor-container').style.display = 'none';
    document.getElementById('preview-content').style.display = 'block';

    document.getElementById('edit-btn').style.display = 'flex';
    document.getElementById('save-btn').style.display = 'none';
    document.getElementById('cancel-btn').style.display = 'none';
}

function saveFile() {
    var statusEl = document.getElementById('save-status');
    statusEl.className = 'save-status saving';
    statusEl.textContent = 'Saving...';

    var editedContent = tuiEditor.getMarkdown();

    var parsed = parseFileContent(currentFile.content);
    var fullContent = buildFileContent(editedContent, parsed.signoff, parsed.reviewNotes);

    fetch('/api/save', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            folder: currentFile.folder,
            file: currentFile.name,
            content: fullContent
        })
    })
    .then(function(response) {
        if (!response.ok) throw new Error('Save failed: ' + response.status);
        return response.json();
    })
    .then(function() {
        currentFile.content = fullContent;
        document.getElementById('preview-content').innerHTML = wrapVariableMarkers(marked.parse(substituteVariables(editedContent, true)));
        if (parsed.reviewNotes.length > 0) applyReviewNoteHighlights(parsed.reviewNotes);
        renderReviewNoteSummary(parsed.reviewNotes);
        renderSignoffPanel(parsed.signoff);
        attachSelectionListener();
        attachVariableClickHandlers();
        cancelEdit();
        statusEl.className = 'save-status saved';
        statusEl.textContent = 'Saved';
        setTimeout(function() { statusEl.className = 'save-status'; }, 2500);
    })
    .catch(function(err) {
        statusEl.className = 'save-status error';
        statusEl.textContent = 'Error: ' + err.message;
    });
}

window.addEventListener('beforeunload', function(e) {
    if (isEditMode) {
        e.preventDefault();
        e.returnValue = '';
    }
});

// ========== REVIEW NOTES ==========

function escapeRegExp(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function applyReviewNoteHighlights(reviewNotes) {
    var contentEl = document.getElementById('preview-content');
    var html = contentEl.innerHTML;
    var signoffPanel = document.getElementById('signoff-panel');
    if (signoffPanel) signoffPanel.remove();
    var rnPanel = document.getElementById('review-notes-panel');
    if (rnPanel) rnPanel.remove();

    html = contentEl.innerHTML;
    for (var i = 0; i < reviewNotes.length; i++) {
        var note = reviewNotes[i];
        var escapedText = escapeRegExp(note.highlighted);
        var regex = new RegExp('(' + escapedText + ')', 'i');
        var cls = note.status === 'resolved' ? 'review-note-highlight resolved' : 'review-note-highlight';
        var replacement = '<span class="' + cls + '" data-note-id="' + note.id + '" onclick="openNoteDetailModal(\'' + note.id + '\')">' +
            '$1<span class="review-note-indicator">' + (i + 1) + '</span></span>';
        html = html.replace(regex, replacement);
    }
    contentEl.innerHTML = html;
}

var addNotePopupEl = null;
var pendingSelectedText = '';

function removeAddNotePopup() {
    if (addNotePopupEl) { addNotePopupEl.remove(); addNotePopupEl = null; }
    pendingSelectedText = '';
}

function attachSelectionListener() {
    var contentEl = document.getElementById('preview-content');
    contentEl.removeEventListener('mouseup', handleTextSelection);
    contentEl.addEventListener('mouseup', handleTextSelection);
}

function handleTextSelection(e) {
    if (e.target.closest('#signoff-panel') || e.target.closest('#review-notes-panel') ||
        e.target.closest('.review-note-highlight') || e.target.closest('.add-note-popup')) return;

    setTimeout(function() {
        var sel = window.getSelection();
        var text = sel ? sel.toString().trim() : '';
        removeAddNotePopup();

        if (text.length < 3 || text.length > 500) return;

        if (!sel.rangeCount) return;
        var range = sel.getRangeAt(0);
        var container = document.getElementById('preview-content');
        if (!container.contains(range.commonAncestorContainer)) return;

        pendingSelectedText = text;
        var rect = range.getBoundingClientRect();
        var popup = document.createElement('div');
        popup.className = 'add-note-popup';
        popup.innerHTML = '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg> Add Review Note';
        popup.style.left = (rect.left + rect.width / 2 - 80) + 'px';
        popup.style.top = (rect.top - 36) + 'px';
        popup.onclick = function(ev) {
            ev.stopPropagation();
            openAddNoteModal(pendingSelectedText);
            removeAddNotePopup();
        };
        document.body.appendChild(popup);
        addNotePopupEl = popup;
    }, 10);
}

document.addEventListener('mousedown', function(e) {
    if (addNotePopupEl && !e.target.closest('.add-note-popup')) {
        removeAddNotePopup();
    }
});

function openAddNoteModal(selectedText) {
    var overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = 'add-note-overlay';
    overlay.innerHTML =
        '<div class="modal-content modal-sm">' +
        '  <div class="modal-header"><h3>Add Review Note</h3><button class="modal-close" onclick="closeModal(\'add-note-overlay\')">&times;</button></div>' +
        '  <div class="modal-body">' +
        '    <div class="modal-field"><label>Selected Text</label><div class="selected-text">' + escapeHtml(selectedText) + '</div></div>' +
        '    <div class="modal-field"><label>Reviewer Name</label><input type="text" id="rn-reviewer-name" placeholder="Enter your name"></div>' +
        '    <div class="modal-field"><label>Date</label><input type="date" id="rn-date" value="' + todayStr() + '"></div>' +
        '    <div class="modal-field"><label>Review Note</label><textarea id="rn-note-text" placeholder="Enter your review note..."></textarea></div>' +
        '  </div>' +
        '  <div class="modal-footer">' +
        '    <button class="btn-secondary" onclick="closeModal(\'add-note-overlay\')">Cancel</button>' +
        '    <button class="btn-primary" onclick="submitNewReviewNote()">Add Note</button>' +
        '  </div>' +
        '</div>';
    overlay.setAttribute('data-selected', selectedText);
    document.body.appendChild(overlay);
    document.getElementById('rn-reviewer-name').focus();
}

function submitNewReviewNote() {
    var name = document.getElementById('rn-reviewer-name').value.trim();
    var date = document.getElementById('rn-date').value;
    var note = document.getElementById('rn-note-text').value.trim();
    var overlay = document.getElementById('add-note-overlay');
    var selectedText = overlay.getAttribute('data-selected');

    if (!name) { alert('Please enter reviewer name.'); return; }
    if (!note) { alert('Please enter a review note.'); return; }

    var noteObj = {
        id: 'rn_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5),
        highlighted: selectedText,
        note: note,
        reviewer: name,
        date: date,
        status: 'open',
        response: '',
        responder: '',
        responseDate: ''
    };

    var parsed = parseFileContent(currentFile.content);
    parsed.reviewNotes.push(noteObj);
    var fullContent = buildFileContent(parsed.docContent, parsed.signoff, parsed.reviewNotes);

    fetch('/api/save', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder: currentFile.folder, file: currentFile.name, content: fullContent })
    })
    .then(function(r) { if (!r.ok) throw new Error('Save failed'); return r.json(); })
    .then(function() {
        currentFile.content = fullContent;
        document.getElementById('preview-content').innerHTML = wrapVariableMarkers(marked.parse(substituteVariables(parsed.docContent, true)));
        applyReviewNoteHighlights(parsed.reviewNotes);
        renderReviewNoteSummary(parsed.reviewNotes);
        renderSignoffPanel(parsed.signoff);
        attachSelectionListener();
        attachVariableClickHandlers();
        closeModal('add-note-overlay');
    })
    .catch(function(err) { alert('Failed to save review note: ' + err.message); });
}

function openNoteDetailModal(noteId) {
    var parsed = parseFileContent(currentFile.content);
    var note = null;
    for (var i = 0; i < parsed.reviewNotes.length; i++) {
        if (parsed.reviewNotes[i].id === noteId) { note = parsed.reviewNotes[i]; break; }
    }
    if (!note) return;

    var responseHtml = '';
    if (note.response) {
        responseHtml = '<div class="modal-field"><label>Response by ' + escapeHtml(note.responder) + ' (' + escapeHtml(note.responseDate) + ')</label>' +
            '<div style="background:#d1fae5;padding:8px 12px;border-radius:6px;font-size:13px;color:#065f46;border:1px solid #a7f3d0;">' + escapeHtml(note.response) + '</div></div>';
    }

    var overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = 'note-detail-overlay';
    overlay.innerHTML =
        '<div class="modal-content modal-sm">' +
        '  <div class="modal-header"><h3>Review Note</h3><button class="modal-close" onclick="closeModal(\'note-detail-overlay\')">&times;</button></div>' +
        '  <div class="modal-body">' +
        '    <div class="modal-field"><label>Highlighted Text</label><div class="selected-text">' + escapeHtml(note.highlighted) + '</div></div>' +
        '    <div class="modal-field"><label>Reviewer: ' + escapeHtml(note.reviewer) + ' | Date: ' + escapeHtml(note.date) + '</label>' +
        '      <div style="background:#fef9c3;padding:8px 12px;border-radius:6px;font-size:13px;color:#92400e;border:1px solid #fde68a;">' + escapeHtml(note.note) + '</div></div>' +
        '    <div class="modal-field"><label>Status</label><select id="nd-status"><option value="open"' + (note.status === 'open' ? ' selected' : '') + '>Open</option><option value="resolved"' + (note.status === 'resolved' ? ' selected' : '') + '>Resolved</option></select></div>' +
        responseHtml +
        '    <hr style="margin:12px 0;border:none;border-top:1px solid #e2e8f0;">' +
        '    <div class="modal-field"><label>Respond to this note</label><textarea id="nd-response" placeholder="Enter response...">' + escapeHtml(note.response) + '</textarea></div>' +
        '    <div class="modal-field"><label>Responder Name</label><input type="text" id="nd-responder" value="' + escapeHtml(note.responder) + '" placeholder="Your name"></div>' +
        '  </div>' +
        '  <div class="modal-footer">' +
        '    <button class="btn-danger" onclick="deleteReviewNote(\'' + noteId + '\')">Delete</button>' +
        '    <div style="flex:1;"></div>' +
        '    <button class="btn-secondary" onclick="closeModal(\'note-detail-overlay\')">Cancel</button>' +
        '    <button class="btn-primary" onclick="saveNoteResponse(\'' + noteId + '\')">Save</button>' +
        '  </div>' +
        '</div>';
    document.body.appendChild(overlay);
}

function saveNoteResponse(noteId) {
    var status = document.getElementById('nd-status').value;
    var response = document.getElementById('nd-response').value.trim();
    var responder = document.getElementById('nd-responder').value.trim();

    var parsed = parseFileContent(currentFile.content);
    for (var i = 0; i < parsed.reviewNotes.length; i++) {
        if (parsed.reviewNotes[i].id === noteId) {
            parsed.reviewNotes[i].status = status;
            if (response) {
                parsed.reviewNotes[i].response = response;
                parsed.reviewNotes[i].responder = responder;
                parsed.reviewNotes[i].responseDate = todayStr();
            }
            break;
        }
    }
    saveAndRerender(parsed, 'note-detail-overlay');
}

function deleteReviewNote(noteId) {
    if (!confirm('Delete this review note?')) return;
    var parsed = parseFileContent(currentFile.content);
    parsed.reviewNotes = parsed.reviewNotes.filter(function(n) { return n.id !== noteId; });
    saveAndRerender(parsed, 'note-detail-overlay');
}

function saveAndRerender(parsed, modalId) {
    var fullContent = buildFileContent(parsed.docContent, parsed.signoff, parsed.reviewNotes);
    fetch('/api/save', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folder: currentFile.folder, file: currentFile.name, content: fullContent })
    })
    .then(function(r) { if (!r.ok) throw new Error('Save failed'); return r.json(); })
    .then(function() {
        currentFile.content = fullContent;
        document.getElementById('preview-content').innerHTML = wrapVariableMarkers(marked.parse(substituteVariables(parsed.docContent, true)));
        if (parsed.reviewNotes.length > 0) applyReviewNoteHighlights(parsed.reviewNotes);
        renderReviewNoteSummary(parsed.reviewNotes);
        renderSignoffPanel(parsed.signoff);
        attachSelectionListener();
        attachVariableClickHandlers();
        if (modalId) closeModal(modalId);
    })
    .catch(function(err) { alert('Failed to save: ' + err.message); });
}

function closeModal(id) {
    var el = document.getElementById(id);
    if (el) el.remove();
}

// ========== REVIEW NOTES SUMMARY (per-file) ==========

var rnFilterStatus = 'all';

function renderReviewNoteSummary(reviewNotes) {
    var existing = document.getElementById('review-notes-panel');
    if (existing) existing.remove();
    if (!reviewNotes || reviewNotes.length === 0) return;

    var openCount = reviewNotes.filter(function(n) { return n.status === 'open'; }).length;
    var resolvedCount = reviewNotes.length - openCount;

    var panel = document.createElement('div');
    panel.id = 'review-notes-panel';

    var html = '<h3>Review Notes <span style="font-weight:400;font-size:12px;">(' + openCount + ' open, ' + resolvedCount + ' resolved)</span>' +
        '<button class="rn-delete" onclick="clearResolvedNotes()" style="font-size:11px;padding:4px 10px;">Clear Resolved</button></h3>';

    html += '<div class="rn-filter-tabs">' +
        '<span class="rn-filter-tab' + (rnFilterStatus === 'all' ? ' active' : '') + '" onclick="filterRN(\'all\')">All (' + reviewNotes.length + ')</span>' +
        '<span class="rn-filter-tab' + (rnFilterStatus === 'open' ? ' active' : '') + '" onclick="filterRN(\'open\')">Open (' + openCount + ')</span>' +
        '<span class="rn-filter-tab' + (rnFilterStatus === 'resolved' ? ' active' : '') + '" onclick="filterRN(\'resolved\')">Resolved (' + resolvedCount + ')</span>' +
        '</div>';

    html += '<table class="rn-table"><thead><tr><th>#</th><th>Text</th><th>Reviewer Note</th><th>Response</th><th>Status</th><th>Actions</th></tr></thead><tbody>';

    for (var i = 0; i < reviewNotes.length; i++) {
        var n = reviewNotes[i];
        if (rnFilterStatus !== 'all' && n.status !== rnFilterStatus) continue;
        html += '<tr>' +
            '<td>' + (i + 1) + '</td>' +
            '<td><span class="rn-truncate" title="' + escapeHtml(n.highlighted) + '">' + escapeHtml(n.highlighted.substring(0, 40)) + '</span></td>' +
            '<td><strong>' + escapeHtml(n.reviewer) + '</strong> (' + escapeHtml(n.date) + ')<br>' + escapeHtml(n.note) + '</td>' +
            '<td>' + (n.response ? '<strong>' + escapeHtml(n.responder) + '</strong><br>' + escapeHtml(n.response) : '<span style="color:#94a3b8;">--</span>') + '</td>' +
            '<td><span class="rn-status rn-status-' + n.status + '">' + n.status + '</span></td>' +
            '<td class="rn-actions">' +
            '<button class="rn-goto" onclick="scrollToNote(\'' + n.id + '\')">Go to</button>' +
            '<button class="rn-delete" onclick="deleteReviewNote(\'' + n.id + '\')">Delete</button>' +
            '</td></tr>';
    }
    html += '</tbody></table>';

    panel.innerHTML = html;
    document.getElementById('preview-content').appendChild(panel);
}

function filterRN(status) {
    rnFilterStatus = status;
    var parsed = parseFileContent(currentFile.content);
    renderReviewNoteSummary(parsed.reviewNotes);
}

function scrollToNote(noteId) {
    var el = document.querySelector('[data-note-id="' + noteId + '"]');
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.outline = '3px solid #f59e0b';
        setTimeout(function() { el.style.outline = ''; }, 2000);
    }
}

function clearResolvedNotes() {
    var parsed = parseFileContent(currentFile.content);
    var openNotes = parsed.reviewNotes.filter(function(n) { return n.status !== 'resolved'; });
    if (openNotes.length === parsed.reviewNotes.length) { alert('No resolved notes to clear.'); return; }
    if (!confirm('Clear all resolved review notes?')) return;
    parsed.reviewNotes = openNotes;
    saveAndRerender(parsed, null);
}

// ========== CROSS-FILE REVIEW SUMMARY ==========

async function openCrossFileReviewSummary() {
    var overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = 'cross-review-overlay';
    overlay.innerHTML =
        '<div class="modal-content modal-lg">' +
        '  <div class="modal-header"><h3>Review Notes Summary - All Files</h3><button class="modal-close" onclick="closeModal(\'cross-review-overlay\')">&times;</button></div>' +
        '  <div class="modal-body"><p style="color:#64748b;">Loading files...</p></div>' +
        '</div>';
    document.body.appendChild(overlay);

    var allNotes = [];
    var total = 0;
    for (var i = 0; i < sections.length; i++) {
        for (var j = 0; j < sections[i].files.length; j++) total++;
    }
    var loaded = 0;

    for (var i = 0; i < sections.length; i++) {
        var sec = sections[i];
        for (var j = 0; j < sec.files.length; j++) {
            var file = sec.files[j];
            try {
                var response = await fetch(sec.id + '/' + file.name + '?t=' + Date.now());
                if (response.ok) {
                    var md = await response.text();
                    var parsed = parseFileContent(md);
                    if (parsed.reviewNotes.length > 0) {
                        for (var k = 0; k < parsed.reviewNotes.length; k++) {
                            allNotes.push({
                                folder: sec.id,
                                filename: file.name,
                                display: file.display,
                                note: parsed.reviewNotes[k]
                            });
                        }
                    }
                }
            } catch(e) {}
            loaded++;
            var bodyEl = overlay.querySelector('.modal-body');
            if (bodyEl) bodyEl.innerHTML = '<p style="color:#64748b;">Loading files... ' + loaded + '/' + total + '</p>';
        }
    }

    renderCrossFileSummary(allNotes);
}

var crossFilterStatus = 'all';

function renderCrossFileSummary(allNotes) {
    var overlay = document.getElementById('cross-review-overlay');
    if (!overlay) return;

    var openCount = allNotes.filter(function(n) { return n.note.status === 'open'; }).length;
    var resolvedCount = allNotes.length - openCount;

    var html = '<div class="rn-filter-tabs" style="margin-bottom:12px;">' +
        '<span class="rn-filter-tab' + (crossFilterStatus === 'all' ? ' active' : '') + '" onclick="crossFilterRN(\'all\')">All (' + allNotes.length + ')</span>' +
        '<span class="rn-filter-tab' + (crossFilterStatus === 'open' ? ' active' : '') + '" onclick="crossFilterRN(\'open\')">Open (' + openCount + ')</span>' +
        '<span class="rn-filter-tab' + (crossFilterStatus === 'resolved' ? ' active' : '') + '" onclick="crossFilterRN(\'resolved\')">Resolved (' + resolvedCount + ')</span>' +
        '</div>';

    if (allNotes.length === 0) {
        html += '<p style="color:#64748b;text-align:center;padding:30px;">No review notes found across all files.</p>';
    } else {
        html += '<table class="rn-table"><thead><tr><th>File</th><th>Text</th><th>Reviewer Note</th><th>Response</th><th>Status</th><th>Actions</th></tr></thead><tbody>';
        for (var i = 0; i < allNotes.length; i++) {
            var item = allNotes[i];
            var n = item.note;
            if (crossFilterStatus !== 'all' && n.status !== crossFilterStatus) continue;
            html += '<tr>' +
                '<td style="font-size:11px;">' + escapeHtml(item.display) + '</td>' +
                '<td><span class="rn-truncate" title="' + escapeHtml(n.highlighted) + '">' + escapeHtml(n.highlighted.substring(0, 30)) + '</span></td>' +
                '<td><strong>' + escapeHtml(n.reviewer) + '</strong><br>' + escapeHtml(n.note.substring(0, 50)) + '</td>' +
                '<td>' + (n.response ? escapeHtml(n.response.substring(0, 40)) : '<span style="color:#94a3b8;">--</span>') + '</td>' +
                '<td><span class="rn-status rn-status-' + n.status + '">' + n.status + '</span></td>' +
                '<td><button class="rn-goto" onclick="goToNote(\'' + item.folder + '\',\'' + item.filename + '\',\'' + escapeHtml(item.display).replace(/'/g, "\\'") + '\',\'' + n.id + '\')">Go to</button></td>' +
                '</tr>';
        }
        html += '</tbody></table>';
    }

    html += '<div style="margin-top:16px;display:flex;justify-content:flex-end;gap:8px;">' +
        '<button class="btn-danger" onclick="clearAllResolvedNotes()">Clear All Resolved</button>' +
        '</div>';

    overlay.querySelector('.modal-body').innerHTML = html;
    window._crossReviewNotes = allNotes;
}

function crossFilterRN(status) {
    crossFilterStatus = status;
    if (window._crossReviewNotes) renderCrossFileSummary(window._crossReviewNotes);
}

function goToNote(folder, filename, display, noteId) {
    closeModal('cross-review-overlay');
    loadFile(folder, filename, display);
    setTimeout(function() { scrollToNote(noteId); }, 800);
}

async function clearAllResolvedNotes() {
    if (!confirm('Clear all resolved review notes across all files? This cannot be undone.')) return;
    var notes = window._crossReviewNotes || [];
    var filesToUpdate = {};
    for (var i = 0; i < notes.length; i++) {
        if (notes[i].note.status === 'resolved') {
            var key = notes[i].folder + '/' + notes[i].filename;
            if (!filesToUpdate[key]) filesToUpdate[key] = { folder: notes[i].folder, filename: notes[i].filename };
        }
    }
    var keys = Object.keys(filesToUpdate);
    for (var i = 0; i < keys.length; i++) {
        var info = filesToUpdate[keys[i]];
        try {
            var resp = await fetch(info.folder + '/' + info.filename + '?t=' + Date.now());
            if (!resp.ok) continue;
            var md = await resp.text();
            var parsed = parseFileContent(md);
            parsed.reviewNotes = parsed.reviewNotes.filter(function(n) { return n.status !== 'resolved'; });
            var fullContent = buildFileContent(parsed.docContent, parsed.signoff, parsed.reviewNotes);
            await fetch('/api/save', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folder: info.folder, file: info.filename, content: fullContent })
            });
            if (currentFile.folder === info.folder && currentFile.name === info.filename) {
                currentFile.content = fullContent;
            }
        } catch(e) {}
    }
    closeModal('cross-review-overlay');
    openCrossFileReviewSummary();
    if (currentFile.folder && currentFile.name) loadFile(currentFile.folder, currentFile.name, currentFile.display);
}

// ========== BULK SIGN-OFF ==========

var bulkSignoffRole = 'preparer';
var bulkSignoffData = [];

async function openBulkSignoff() {
    bulkSignoffData = [];
    var overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.id = 'bulk-signoff-overlay';
    overlay.innerHTML =
        '<div class="modal-content modal-lg">' +
        '  <div class="modal-header"><h3>Bulk Sign-Off</h3><button class="modal-close" onclick="closeModal(\'bulk-signoff-overlay\')">&times;</button></div>' +
        '  <div class="modal-body"><p style="color:#64748b;">Loading file statuses...</p></div>' +
        '</div>';
    document.body.appendChild(overlay);

    var total = 0;
    for (var i = 0; i < sections.length; i++) total += sections[i].files.length;
    var loaded = 0;

    for (var i = 0; i < sections.length; i++) {
        var sec = sections[i];
        for (var j = 0; j < sec.files.length; j++) {
            var file = sec.files[j];
            try {
                var response = await fetch(sec.id + '/' + file.name + '?t=' + Date.now());
                if (response.ok) {
                    var md = await response.text();
                    var parsed = parseFileContent(md);
                    bulkSignoffData.push({
                        folder: sec.id, filename: file.name, display: file.display,
                        sectionTitle: sec.title, signoff: parsed.signoff, content: md
                    });
                }
            } catch(e) {}
            loaded++;
            var bodyEl = overlay.querySelector('.modal-body');
            if (bodyEl) bodyEl.innerHTML = '<p style="color:#64748b;">Loading... ' + loaded + '/' + total + '</p>';
        }
    }

    renderBulkSignoffModal();
}

function renderBulkSignoffModal() {
    var overlay = document.getElementById('bulk-signoff-overlay');
    if (!overlay) return;

    var html = '<div class="bs-role-select">' +
        '<button class="bs-role-btn' + (bulkSignoffRole === 'preparer' ? ' active' : '') + '" onclick="setBulkRole(\'preparer\')">Preparer</button>' +
        '<button class="bs-role-btn' + (bulkSignoffRole === 'reviewer' ? ' active' : '') + '" onclick="setBulkRole(\'reviewer\')">Reviewer</button>' +
        '</div>';

    html += '<div style="display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap;align-items:end;">' +
        '<div class="modal-field" style="margin:0;flex:1;min-width:150px;"><label>Name</label><input type="text" id="bs-name" placeholder="Enter name"></div>' +
        '<div class="modal-field" style="margin:0;"><label>Date</label><input type="date" id="bs-date" value="' + todayStr() + '"></div>';
    if (bulkSignoffRole === 'reviewer') {
        html += '<div class="modal-field" style="margin:0;flex:1;min-width:150px;"><label>Note (optional)</label><input type="text" id="bs-note" placeholder="Note"></div>';
    }
    html += '</div>';

    html += '<div style="display:flex;gap:8px;margin-bottom:8px;">' +
        '<button class="btn-secondary" onclick="toggleBulkSelectAll(true)" style="font-size:11px;padding:4px 12px;">Select All</button>' +
        '<button class="btn-secondary" onclick="toggleBulkSelectAll(false)" style="font-size:11px;padding:4px 12px;">Deselect All</button>' +
        '<span style="flex:1;"></span>' +
        '<span id="bs-selected-count" style="font-size:11px;color:#64748b;align-self:center;">0 selected</span>' +
        '</div>';

    html += '<div style="max-height:350px;overflow-y:auto;"><table class="bs-table"><thead><tr>' +
        '<th style="width:30px;"><input type="checkbox" onchange="toggleBulkSelectAll(this.checked)" checked></th>' +
        '<th>File</th><th>Preparer</th><th>Reviewer</th>' +
        '</tr></thead><tbody>';

    for (var i = 0; i < bulkSignoffData.length; i++) {
        var item = bulkSignoffData[i];
        var s = item.signoff || { preparer: null, reviews: [] };
        var preparerStr = s.preparer ? escapeHtml(s.preparer.name) + ' (' + escapeHtml(s.preparer.date) + ')' : '<span style="color:#94a3b8;">Not signed</span>';
        var reviewerStr = s.reviews && s.reviews.length > 0 ? escapeHtml(s.reviews[s.reviews.length - 1].name) + ' (' + escapeHtml(s.reviews[s.reviews.length - 1].date) + ')' : '<span style="color:#94a3b8;">Not reviewed</span>';

        html += '<tr><td><input type="checkbox" class="bs-checkbox" data-idx="' + i + '" checked onchange="updateBulkCount()"></td>' +
            '<td style="font-size:11px;">' + escapeHtml(item.display) + '</td>' +
            '<td>' + preparerStr + '</td>' +
            '<td>' + reviewerStr + '</td></tr>';
    }

    html += '</tbody></table></div>';

    html += '<div id="bs-progress" class="bs-progress" style="display:none;">' +
        '<div class="bs-progress-bar"><div class="bs-progress-fill" id="bs-progress-fill" style="width:0%;"></div></div>' +
        '<div class="bs-progress-text" id="bs-progress-text">Signing...</div></div>';

    html += '<div style="margin-top:16px;display:flex;justify-content:flex-end;">' +
        '<button class="btn-purple" id="bs-apply-btn" onclick="applyBulkSignoff()">Apply Sign-Off</button></div>';

    overlay.querySelector('.modal-body').innerHTML = html;
    updateBulkCount();
}

function setBulkRole(role) {
    bulkSignoffRole = role;
    renderBulkSignoffModal();
}

function toggleBulkSelectAll(checked) {
    document.querySelectorAll('.bs-checkbox').forEach(function(cb) { cb.checked = checked; });
    updateBulkCount();
}

function updateBulkCount() {
    var count = document.querySelectorAll('.bs-checkbox:checked').length;
    var el = document.getElementById('bs-selected-count');
    if (el) el.textContent = count + ' selected';
}

async function applyBulkSignoff() {
    var name = document.getElementById('bs-name').value.trim();
    var date = document.getElementById('bs-date').value;
    if (!name) { alert('Please enter name.'); return; }
    if (!date) { alert('Please enter date.'); return; }
    var note = '';
    if (bulkSignoffRole === 'reviewer') {
        var noteEl = document.getElementById('bs-note');
        if (noteEl) note = noteEl.value.trim();
    }

    var selected = [];
    document.querySelectorAll('.bs-checkbox:checked').forEach(function(cb) {
        selected.push(parseInt(cb.getAttribute('data-idx')));
    });

    if (selected.length === 0) { alert('No files selected.'); return; }

    document.getElementById('bs-progress').style.display = 'block';
    document.getElementById('bs-apply-btn').disabled = true;

    var done = 0;
    var failed = 0;

    for (var i = 0; i < selected.length; i++) {
        var idx = selected[i];
        var item = bulkSignoffData[idx];
        try {
            var resp = await fetch(item.folder + '/' + item.filename + '?t=' + Date.now());
            if (!resp.ok) { failed++; continue; }
            var md = await resp.text();
            var parsed = parseFileContent(md);
            var signoff = parsed.signoff || { preparer: null, reviews: [] };

            if (bulkSignoffRole === 'preparer') {
                signoff.preparer = { name: name, date: date };
            } else {
                signoff.reviews.push({ name: name, date: date, note: note });
            }

            var fullContent = buildFileContent(parsed.docContent, signoff, parsed.reviewNotes);
            var saveResp = await fetch('/api/save', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folder: item.folder, file: item.filename, content: fullContent })
            });
            if (!saveResp.ok) { failed++; continue; }

            bulkSignoffData[idx].signoff = signoff;
            bulkSignoffData[idx].content = fullContent;

            if (currentFile.folder === item.folder && currentFile.name === item.filename) {
                currentFile.content = fullContent;
            }
        } catch(e) { failed++; }

        done++;
        var pct = Math.round((done / selected.length) * 100);
        document.getElementById('bs-progress-fill').style.width = pct + '%';
        document.getElementById('bs-progress-text').textContent = 'Signing... ' + done + '/' + selected.length + (failed > 0 ? ' (' + failed + ' failed)' : '');
    }

    document.getElementById('bs-progress-text').textContent = 'Complete! ' + (done - failed) + ' signed' + (failed > 0 ? ', ' + failed + ' failed' : '');
    document.getElementById('bs-apply-btn').disabled = false;

    setTimeout(function() { renderBulkSignoffModal(); }, 1000);

    if (currentFile.folder && currentFile.name) {
        loadFile(currentFile.folder, currentFile.name, currentFile.display);
    }
}

// ========== SEARCH ==========

document.getElementById('search-input').addEventListener('input', function(e) {
    var query = e.target.value.toLowerCase();
    allFiles.forEach(function(file) {
        var matches = file.display.toLowerCase().includes(query) || file.name.toLowerCase().includes(query);
        file.element.style.display = matches ? '' : 'none';
    });
    if (query) {
        document.querySelectorAll('.nav-section').forEach(function(section) {
            var hasVisible = section.querySelectorAll('.nav-item:not([style*="display: none"])').length > 0;
            if (hasVisible) section.classList.add('expanded');
        });
    }
});

var resizer = document.getElementById('resizer');
var navPanel = document.getElementById('nav-panel');
var isResizing = false;
resizer.onmousedown = function() { isResizing = true; document.body.style.cursor = 'col-resize'; };
document.onmousemove = function(e) { if (isResizing && e.clientX > 200 && e.clientX < 500) navPanel.style.width = e.clientX + 'px'; };
document.onmouseup = function() { isResizing = false; document.body.style.cursor = ''; };
document.onkeydown = function(e) { if (e.key === 'f' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); document.getElementById('search-input').focus(); } };

async function downloadAllDocuments() {
    var btn = document.getElementById('download-all-btn');
    var originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = 'Fetching files...';

    var loadedFiles = [];
    var totalFilesCount = 0;
    var loadedCount = 0;

    sections.forEach(function(sec) { totalFilesCount += sec.files.length; });

    for (var i = 0; i < sections.length; i++) {
        var sec = sections[i];
        for (var j = 0; j < sec.files.length; j++) {
            var file = sec.files[j];
            try {
                var response = await fetch(sec.id + '/' + file.name + '?t=' + Date.now());
                if (response.ok) {
                    var content = await response.text();
                    loadedFiles.push({
                        section: sec.title, sectionId: sec.id, sectionIcon: sec.icon,
                        name: file.name, display: file.display, content: content,
                        html: marked.parse(substituteVariables(content))
                    });
                }
            } catch (e) { console.log('Could not load: ' + sec.id + '/' + file.name); }
            loadedCount++;
            btn.innerHTML = 'Fetching... ' + loadedCount + '/' + totalFilesCount;
        }
    }

    btn.innerHTML = 'Generating HTML...';

    var filesBySection = {};
    loadedFiles.forEach(function(item) {
        if (!filesBySection[item.sectionId]) {
            filesBySection[item.sectionId] = { title: item.section, icon: item.sectionIcon, files: [] };
        }
        filesBySection[item.sectionId].files.push(item);
    });

    var html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">';
    html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">';
    html += '<title>[CLIENT_NAME] - Audit Working Papers (Offline)</title>';
    html += '<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;display:flex;height:100vh;overflow:hidden;background:#f5f5f5}#nav-panel{width:320px;background:#1e293b;color:#e2e8f0;overflow-y:auto;display:flex;flex-direction:column}#nav-header{background:#0f172a;padding:16px 20px;border-bottom:1px solid #334155}#nav-header h1{font-size:14px;font-weight:600;color:#60a5fa;margin-bottom:4px}#nav-header h2{font-size:11px;color:#94a3b8}#nav-content{flex:1;overflow-y:auto}.nav-section{border-bottom:1px solid #334155}.nav-section-header{display:flex;align-items:center;padding:12px 16px;cursor:pointer;background:#1e293b}.nav-section-header:hover{background:#334155}.nav-section-header .icon{width:24px;height:24px;margin-right:10px;display:flex;align-items:center;justify-content:center;background:#374151;border-radius:4px;color:#60a5fa;font-weight:600;font-size:11px}.nav-section-header .title{flex:1;font-size:13px;font-weight:500}.nav-section-header .arrow{font-size:10px;color:#64748b;transition:transform .2s}.nav-section.expanded .arrow{transform:rotate(90deg)}.nav-section-items{display:none;background:#0f172a}.nav-section.expanded .nav-section-items{display:block}.nav-item{padding:8px 16px 8px 50px;cursor:pointer;font-size:12px;color:#94a3b8;border-left:3px solid transparent}.nav-item:hover{background:#1e293b;color:#e2e8f0}.nav-item.active{background:#1e40af;color:#fff;border-left-color:#60a5fa}#preview-panel{flex:1;display:flex;flex-direction:column;background:#fff;overflow:hidden}#preview-header{padding:16px 24px;background:#fff;border-bottom:1px solid #e2e8f0}#preview-header .breadcrumb{font-size:12px;color:#64748b;margin-right:8px}#preview-header .filename{font-size:16px;font-weight:600;color:#1e293b}#preview-content{flex:1;overflow-y:auto;padding:24px 40px}#preview-content h1{font-size:28px;font-weight:700;color:#1e293b;margin-bottom:16px;padding-bottom:12px;border-bottom:2px solid #e2e8f0}#preview-content h2{font-size:22px;font-weight:600;color:#334155;margin:28px 0 12px}#preview-content h3{font-size:18px;font-weight:600;color:#475569;margin:24px 0 10px}#preview-content p{font-size:14px;line-height:1.7;color:#475569;margin-bottom:12px}#preview-content ul,#preview-content ol{margin:12px 0 12px 24px;color:#475569}#preview-content li{font-size:14px;line-height:1.7;margin-bottom:4px}#preview-content table{width:100%;border-collapse:collapse;margin:16px 0;font-size:12px}#preview-content th{background:#f1f5f9;padding:10px 12px;text-align:left;font-weight:600;color:#334155;border:1px solid #e2e8f0}#preview-content td{padding:10px 12px;border:1px solid #e2e8f0;color:#475569}#preview-content tr:hover td{background:#f8fafc}#preview-content code{background:#f1f5f9;padding:2px 6px;border-radius:4px;font-family:Consolas,Monaco,monospace;font-size:13px;color:#e11d48}#preview-content pre{background:#1e293b;padding:16px;border-radius:8px;overflow-x:auto;margin:16px 0}#preview-content pre code{background:none;color:#e2e8f0;padding:0}#preview-content strong{font-weight:600;color:#1e293b}.welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:#64748b;text-align:center}.welcome h2{font-size:24px;color:#334155;margin-bottom:12px}</style></head><body>';
    html += '<div id="nav-panel"><div id="nav-header"><h1>[CLIENT_NAME]</h1><h2>Audit Working Papers (Offline)</h2></div><div id="nav-content">';

    Object.keys(filesBySection).forEach(function(secId) {
        var sec = filesBySection[secId];
        html += '<div class="nav-section" data-section="' + secId + '">';
        html += '<div class="nav-section-header" onclick="this.parentElement.classList.toggle(\'expanded\')">';
        html += '<span class="icon">' + sec.icon + '</span><span class="title">' + sec.title + '</span><span class="arrow">&#9658;</span></div>';
        html += '<div class="nav-section-items">';
        sec.files.forEach(function(f, idx) {
            html += '<div class="nav-item" data-idx="' + loadedFiles.indexOf(f) + '" onclick="showFile(' + loadedFiles.indexOf(f) + ')">' + f.display + '</div>';
        });
        html += '</div></div>';
    });

    html += '</div></div><div id="preview-panel"><div id="preview-header"><span class="breadcrumb">Select a file</span><span class="filename"></span></div>';
    html += '<div id="preview-content"><div class="welcome"><h2>[CLIENT_NAME]</h2><p>Audit Working Papers - FYE [FYE_YEAR]</p></div></div></div>';

    html += '<scr' + 'ipt>\n';
    html += 'var filesData = ' + JSON.stringify(loadedFiles.map(function(f) {
        var safeHtml = f.html.split('</' + 'script>').join('&lt;/script&gt;').split('<' + 'script').join('&lt;script');
        return { sectionId: f.sectionId, section: f.section, name: f.name, display: f.display, html: safeHtml };
    })) + ';\n';
    html += 'function showFile(idx) {\n';
    html += '  var f = filesData[idx];\n';
    html += '  document.querySelectorAll(".nav-item").forEach(function(el){el.classList.remove("active");});\n';
    html += '  document.querySelector(".nav-item[data-idx=\\""+idx+"\\"]").classList.add("active");\n';
    html += '  var sec = document.querySelector(".nav-section[data-section=\\""+f.sectionId+"\\"]");\n';
    html += '  if(sec) sec.classList.add("expanded");\n';
    html += '  document.getElementById("preview-header").innerHTML = \'<span class="breadcrumb">\'+f.section+\' /</span><span class="filename">\'+f.display+\'</span>\';\n';
    html += '  document.getElementById("preview-content").innerHTML = f.html;\n';
    html += '}\n';
    html += 'document.querySelector(".nav-section").classList.add("expanded");\n';
    html += '</' + 'script>\n';
    html += '</body></html>';

    var blob = new Blob([html], {type: 'text/html'});
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = '[CLIENT_NAME]_Audit_Working_Papers_FYE[FYE_YEAR].html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    btn.disabled = false;
    btn.innerHTML = originalText;
}

// ============================================================
// AI CHAT AGENT
// ============================================================

var aiConversation = [];
var aiSending = false;

function buildFileIndex() {
    var idx = '';
    sections.forEach(function(sec) {
        idx += sec.id + '/\n';
        sec.files.forEach(function(f) { idx += '  ' + f.name + ' (' + f.display + ')\n'; });
    });
    return idx;
}

var aiSystemPrompt = 'You are a professional Malaysian audit workpaper assistant embedded in an audit working papers viewer.\n\n' +
    'You help prepare and maintain audit working papers for statutory audits. You have expertise in:\n' +
    '- ISA (International Standards on Auditing) as adopted in Malaysia\n' +
    '- MPERS (Malaysian Private Entities Reporting Standards)\n' +
    '- MFRS (Malaysian Financial Reporting Standards)\n' +
    '- Companies Act 2016\n' +
    '- Ensuring consistency and completeness across all audit working papers\n\n' +
    'AVAILABLE WORKPAPER FILES:\n' + buildFileIndex() + '\n\n' +
    'MASTER DATA VARIABLE SYSTEM:\n' +
    'Working papers use {{variable_name}} placeholders instead of hardcoded values. These are substituted at render time from master_data.json.\n' +
    'Examples: {{company_name}}, {{fye_date}}, {{total_revenue}}, {{total_assets}}, {{materiality_level}}\n' +
    'Modifiers: {{total_revenue|rm}} adds RM prefix, {{amount|bracket}} shows negative in brackets, {{amount|rm_bracket}} combines both.\n\n' +
    'CRITICAL RULES FOR VARIABLES:\n' +
    '- When editing files, ALWAYS preserve existing {{variable}} placeholders. NEVER replace them with hardcoded values.\n' +
    '- If a value appears repeatedly across files (company name, figures, addresses), it MUST use a {{variable}} placeholder.\n' +
    '- To change a variable value (e.g. company name, a financial figure), use the update_master_data tool — do NOT hardcode the new value in the markdown.\n' +
    '- Use read_master_data to see all available variables and their current values.\n' +
    '- When creating new content that references company info or financial figures, use the appropriate {{variable}} placeholder.\n\n' +
    'RULES:\n' +
    '1. ALWAYS use read_file to read a file BEFORE updating it.\n' +
    '2. When updating a file with update_file, you MUST preserve any <!-- SIGNOFF:... --> and <!-- REVIEWNOTES:... --> HTML comments at the end of the file. Do NOT remove or alter them.\n' +
    '3. NEVER replace {{variable}} placeholders with hardcoded values. To change a value, use update_master_data instead.\n' +
    '4. When a user asks for changes, identify ALL related files that need updating and update them all to maintain consistency.\n' +
    '5. Ensure all audit procedures are documented per ISA requirements.\n' +
    '6. Use proper Malaysian audit terminology.\n' +
    '7. Format content in Markdown.\n' +
    '8. Be concise in chat responses but thorough in file updates.\n' +
    '9. Maintain professional skepticism in all audit conclusions.\n' +
    '10. You have access to specialized skill documents with detailed audit knowledge. Active skills (if any) are appended below. Use the read_skill tool to fetch additional skills not pre-loaded.';

var aiToolDefs = [
    {
        name: 'read_file',
        description: 'Read the contents of a workpaper markdown file. Use this before making any updates.',
        input_schema: {
            type: 'object',
            properties: {
                folder: { type: 'string', description: 'Folder name, e.g. A_Planning, C_Assets' },
                filename: { type: 'string', description: 'File name, e.g. A1_Planning_Memo.md' }
            },
            required: ['folder', 'filename']
        }
    },
    {
        name: 'update_file',
        description: 'Update (overwrite) a workpaper markdown file with new content. Always read the file first. Preserve SIGNOFF and REVIEWNOTES comments.',
        input_schema: {
            type: 'object',
            properties: {
                folder: { type: 'string', description: 'Folder name' },
                filename: { type: 'string', description: 'File name' },
                content: { type: 'string', description: 'Complete new file content in Markdown. Must preserve any existing SIGNOFF and REVIEWNOTES HTML comments.' }
            },
            required: ['folder', 'filename', 'content']
        }
    },
    {
        name: 'list_files',
        description: 'List all available workpaper files and their folders.',
        input_schema: { type: 'object', properties: {} }
    },
    {
        name: 'read_master_data',
        description: 'Read all master data variables and their current values. Use this to see what {{variable}} placeholders are available and their values.',
        input_schema: { type: 'object', properties: {} }
    },
    {
        name: 'update_master_data',
        description: 'Update a master data variable value. This changes the value everywhere it appears via {{variable}} placeholders. Use this instead of hardcoding values in files.',
        input_schema: {
            type: 'object',
            properties: {
                variable_name: { type: 'string', description: 'Variable name, e.g. company_name, total_revenue, materiality_level' },
                new_value: { type: 'string', description: 'New value for the variable. Use string for text, number string for currency values.' }
            },
            required: ['variable_name', 'new_value']
        }
    },
    {
        name: 'read_skill',
        description: 'Read a specialized audit knowledge document for detailed reference. Available skills: audit-working-papers (AWP templates, index structure), financial-statements (MPERS/MFRS FS preparation), pbc-query-management (PBC checklists, query lists), materiality (materiality calculation), risk-assessment (risk assessment procedures). Use when you need detailed audit standards, procedures, or templates.',
        input_schema: {
            type: 'object',
            properties: {
                skill_id: { type: 'string', description: 'Skill ID, e.g. audit-working-papers, financial-statements, pbc-query-management' }
            },
            required: ['skill_id']
        }
    }
];

// ========== SKILL SYSTEM ==========
var aiSkillCache = {};
var aiActiveSkills = [];

(function() {
    try {
        var saved = localStorage.getItem('ai_active_skills');
        if (saved) aiActiveSkills = JSON.parse(saved);
    } catch(e) {}
})();

function toggleSkillChip(el) {
    var skillId = el.getAttribute('data-skill');
    var idx = aiActiveSkills.indexOf(skillId);
    if (idx >= 0) {
        aiActiveSkills.splice(idx, 1);
        el.classList.remove('active');
    } else {
        aiActiveSkills.push(skillId);
        el.classList.add('active');
        if (!aiSkillCache[skillId]) {
            fetch('/api/skills/' + encodeURIComponent(skillId))
                .then(function(r) { return r.json(); })
                .then(function(data) { if (data.content) aiSkillCache[skillId] = data.content; })
                .catch(function() {});
        }
    }
    localStorage.setItem('ai_active_skills', JSON.stringify(aiActiveSkills));
}

function toggleMoreSkills() {
    var extras = document.querySelectorAll('.ai-skill-chip[data-extra]');
    var btn = document.getElementById('ai-more-skills-btn');
    var showing = extras[0] && extras[0].style.display !== 'none';
    extras.forEach(function(el) { el.style.display = showing ? 'none' : ''; });
    btn.textContent = showing ? '+ More' : '- Less';
}

function restoreSkillChips() {
    aiActiveSkills.forEach(function(skillId) {
        var chip = document.querySelector('.ai-skill-chip[data-skill="' + skillId + '"]');
        if (chip) {
            chip.classList.add('active');
            if (chip.getAttribute('data-extra')) {
                document.querySelectorAll('.ai-skill-chip[data-extra]').forEach(function(el) { el.style.display = ''; });
                document.getElementById('ai-more-skills-btn').textContent = '- Less';
            }
        }
        if (!aiSkillCache[skillId]) {
            fetch('/api/skills/' + encodeURIComponent(skillId))
                .then(function(r) { return r.json(); })
                .then(function(data) { if (data.content) aiSkillCache[skillId] = data.content; })
                .catch(function() {});
        }
    });
}
document.addEventListener('DOMContentLoaded', restoreSkillChips);

async function buildSkillPrompt() {
    if (aiActiveSkills.length === 0) return '';
    var parts = [];
    for (var i = 0; i < aiActiveSkills.length; i++) {
        var skillId = aiActiveSkills[i];
        if (!aiSkillCache[skillId]) {
            try {
                var resp = await fetch('/api/skills/' + encodeURIComponent(skillId));
                var data = await resp.json();
                if (data.content) aiSkillCache[skillId] = data.content;
            } catch(e) {}
        }
        if (aiSkillCache[skillId]) {
            parts.push('\n\n--- ACTIVE SKILL: ' + skillId + ' ---\n' + aiSkillCache[skillId]);
        }
    }
    return parts.join('');
}

function toggleAIChat() {
    var panel = document.getElementById('ai-chat-panel');
    var btn = document.querySelector('.ai-chat-toggle');
    if (panel.style.display === 'none') {
        panel.style.display = 'flex';
        btn.classList.add('active');
        btn.textContent = '\u2715';
        if (aiConversation.length === 0) showAIWelcome();
        var input = document.getElementById('ai-input');
        setTimeout(function() { input.focus(); }, 100);
    } else {
        panel.style.display = 'none';
        btn.classList.remove('active');
        btn.textContent = 'AI';
    }
}

function showAIWelcome() {
    var msgs = document.getElementById('ai-chat-messages');
    msgs.innerHTML = '<div class="ai-welcome"><h3>AI Audit Assistant</h3>' +
        '<p>I can help you read, update, and maintain your audit working papers.</p>' +
        '<p style="margin-top:8px;font-size:12px;color:#94a3b8;">Enter your API key in settings (gear icon) to get started.</p></div>';
}

function openAISettings() {
    var key = localStorage.getItem('ai_api_key') || '';
    var model = localStorage.getItem('ai_model') || 'claude-sonnet-4-20250514';
    var modal = document.getElementById('ai-settings-modal');
    document.getElementById('ai-key-input').value = key;
    document.getElementById('ai-model-select').value = model;
    modal.style.display = 'flex';
}

function saveAISettings() {
    var key = document.getElementById('ai-key-input').value.trim();
    var model = document.getElementById('ai-model-select').value;
    if (key) localStorage.setItem('ai_api_key', key);
    else localStorage.removeItem('ai_api_key');
    localStorage.setItem('ai_model', model);
    document.getElementById('ai-settings-modal').style.display = 'none';
}

function clearAIChat() {
    aiConversation = [];
    localStorage.removeItem('ai_conversation');
    showAIWelcome();
}

function appendAIMessage(role, content) {
    var msgs = document.getElementById('ai-chat-messages');
    var welcome = msgs.querySelector('.ai-welcome');
    if (welcome) welcome.remove();

    var div = document.createElement('div');
    if (role === 'user') {
        div.className = 'ai-msg ai-msg-user';
        div.textContent = content;
    } else if (role === 'assistant') {
        div.className = 'ai-msg ai-msg-assistant';
        div.innerHTML = marked.parse(content);
    } else if (role === 'error') {
        div.className = 'ai-msg-error';
        div.textContent = content;
    }
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}

function appendToolIndicator(toolName, input, status) {
    var msgs = document.getElementById('ai-chat-messages');
    var div = document.createElement('div');
    div.className = 'ai-msg-tool';
    div.setAttribute('data-tool-id', toolName + '_' + Date.now());
    var label = toolName;
    if (toolName === 'read_file' && input) label = 'Reading ' + (input.filename || '');
    else if (toolName === 'update_file' && input) label = 'Updating ' + (input.filename || '');
    else if (toolName === 'list_files') label = 'Listing files';
    else if (toolName === 'read_master_data') label = 'Reading master data';
    else if (toolName === 'update_master_data' && input) label = 'Updating ' + (input.variable_name || 'variable');
    else if (toolName === 'read_skill' && input) label = 'Loading skill: ' + (input.skill_id || '');
    if (status === 'running') {
        div.innerHTML = '<span class="tool-spinner"></span>' + label + '...';
    } else {
        div.innerHTML = '\u2713 ' + label;
        div.style.background = '#f0fdf4';
    }
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
}

function showTyping() {
    var msgs = document.getElementById('ai-chat-messages');
    var div = document.createElement('div');
    div.className = 'ai-typing';
    div.id = 'ai-typing-indicator';
    div.innerHTML = '<span></span><span></span><span></span>';
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
}

function hideTyping() {
    var el = document.getElementById('ai-typing-indicator');
    if (el) el.remove();
}

async function executeTool(toolName, toolInput) {
    if (toolName === 'list_files') {
        var result = [];
        sections.forEach(function(sec) {
            sec.files.forEach(function(f) {
                result.push({ folder: sec.id, file: f.name, display: f.display, section: sec.title });
            });
        });
        return JSON.stringify(result);
    } else if (toolName === 'read_file') {
        try {
            var resp = await fetch(toolInput.folder + '/' + toolInput.filename + '?t=' + Date.now());
            if (!resp.ok) return 'Error: File not found (' + resp.status + ')';
            return await resp.text();
        } catch (e) {
            return 'Error: ' + e.message;
        }
    } else if (toolName === 'update_file') {
        try {
            var resp = await fetch('/api/save', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folder: toolInput.folder, file: toolInput.filename, content: toolInput.content })
            });
            var data = await resp.json();
            if (resp.ok) {
                if (currentFile.folder === toolInput.folder && currentFile.name === toolInput.filename) {
                    loadFile(currentFile.folder, currentFile.name, currentFile.display);
                }
                return 'File updated successfully.';
            } else {
                return 'Error saving file: ' + (data.error || resp.status);
            }
        } catch (e) {
            return 'Error: ' + e.message;
        }
    } else if (toolName === 'read_master_data') {
        if (masterData && masterData.variables) {
            var summary = {};
            Object.keys(masterData.variables).forEach(function(k) {
                var v = masterData.variables[k];
                summary[k] = { value: v.value, label: v.label, format: v.format, category: v.category };
            });
            return JSON.stringify(summary, null, 2);
        }
        return 'Error: Master data not loaded.';
    } else if (toolName === 'update_master_data') {
        var varName = toolInput.variable_name;
        if (!masterData || !masterData.variables || !masterData.variables[varName]) {
            return 'Error: Variable "' + varName + '" not found in master data.';
        }
        var varDef = masterData.variables[varName];
        if (typeof varDef.value === 'number') {
            masterData.variables[varName].value = parseFloat(toolInput.new_value) || 0;
        } else {
            masterData.variables[varName].value = toolInput.new_value;
        }
        if (masterData._meta) masterData._meta.lastModified = new Date().toISOString();
        try {
            var resp = await fetch('/api/master', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(masterData)
            });
            if (!resp.ok) return 'Error saving master data: ' + resp.status;
            if (currentFile.folder && currentFile.name) {
                loadFile(currentFile.folder, currentFile.name, currentFile.display);
            }
            return 'Updated "' + varDef.label + '" to: ' + toolInput.new_value;
        } catch (e) {
            return 'Error: ' + e.message;
        }
    } else if (toolName === 'read_skill') {
        try {
            var resp = await fetch('/api/skills/' + encodeURIComponent(toolInput.skill_id));
            if (!resp.ok) return 'Error: Skill not found (' + resp.status + ')';
            var data = await resp.json();
            return data.content || 'Empty skill document.';
        } catch (e) {
            return 'Error: ' + e.message;
        }
    }
    return 'Unknown tool: ' + toolName;
}

var aiEnrichedPrompt = '';

async function callClaudeAPI(messages) {
    var apiKey = localStorage.getItem('ai_api_key');
    if (!apiKey) {
        throw new Error('No API key set. Click the gear icon to enter your Anthropic API key.');
    }
    var model = localStorage.getItem('ai_model') || 'claude-sonnet-4-20250514';
    var systemPrompt = aiEnrichedPrompt || aiSystemPrompt;
    var resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            apiKey: apiKey,
            model: model,
            max_tokens: 8192,
            system: systemPrompt,
            tools: aiToolDefs,
            messages: messages
        })
    });
    if (!resp.ok) {
        var errText = await resp.text();
        try { var errData = JSON.parse(errText); throw new Error(errData.error || 'API error ' + resp.status); }
        catch(e) { if (e.message.includes('API error') || e.message.includes('api_key')) throw e; throw new Error('Server error: ' + resp.status); }
    }
    return await resp.json();
}

async function runToolLoop(response, messages) {
    while (response.stop_reason === 'tool_use') {
        var assistantContent = response.content;
        messages.push({ role: 'assistant', content: assistantContent });

        var toolResults = [];
        for (var i = 0; i < assistantContent.length; i++) {
            var block = assistantContent[i];
            if (block.type === 'tool_use') {
                var indicator = appendToolIndicator(block.name, block.input, 'running');
                var result = await executeTool(block.name, block.input);
                indicator.innerHTML = '\u2713 ' + indicator.textContent.replace('...', '');
                indicator.querySelector('.tool-spinner')?.remove();
                toolResults.push({ type: 'tool_result', tool_use_id: block.id, content: result });
            } else if (block.type === 'text' && block.text) {
                appendAIMessage('assistant', block.text);
            }
        }

        messages.push({ role: 'user', content: toolResults });
        showTyping();
        response = await callClaudeAPI(messages);
        hideTyping();
    }

    var finalText = '';
    if (response.content) {
        response.content.forEach(function(block) {
            if (block.type === 'text') finalText += block.text;
        });
    }
    if (finalText) appendAIMessage('assistant', finalText);

    messages.push({ role: 'assistant', content: response.content });
    aiConversation = messages;
    try { localStorage.setItem('ai_conversation', JSON.stringify(aiConversation)); } catch(e) {}
}

async function sendAIMessage() {
    if (aiSending) return;
    var input = document.getElementById('ai-input');
    var text = input.value.trim();
    if (!text) return;

    input.value = '';
    input.style.height = 'auto';
    appendAIMessage('user', text);

    var messages = aiConversation.slice();
    messages.push({ role: 'user', content: text });

    aiSending = true;
    document.getElementById('ai-send-btn').disabled = true;
    showTyping();

    try {
        var skillContent = await buildSkillPrompt();
        aiEnrichedPrompt = aiSystemPrompt + skillContent;
        var response = await callClaudeAPI(messages);
        hideTyping();
        await runToolLoop(response, messages);
    } catch (e) {
        hideTyping();
        appendAIMessage('error', e.message);
    }

    aiSending = false;
    document.getElementById('ai-send-btn').disabled = false;
    document.getElementById('ai-input').focus();
}

// Load saved conversation on page load
(function() {
    try {
        var saved = localStorage.getItem('ai_conversation');
        if (saved) {
            aiConversation = JSON.parse(saved);
        }
    } catch(e) {}
})();

// Re-render saved conversation when chat is opened
var _origToggle = toggleAIChat;
toggleAIChat = function() {
    var panel = document.getElementById('ai-chat-panel');
    var wasHidden = panel.style.display === 'none';
    _origToggle();
    if (wasHidden && aiConversation.length > 0) {
        var msgs = document.getElementById('ai-chat-messages');
        msgs.innerHTML = '';
        aiConversation.forEach(function(msg) {
            if (msg.role === 'user' && typeof msg.content === 'string') {
                appendAIMessage('user', msg.content);
            } else if (msg.role === 'assistant' && Array.isArray(msg.content)) {
                msg.content.forEach(function(block) {
                    if (block.type === 'text' && block.text) appendAIMessage('assistant', block.text);
                    else if (block.type === 'tool_use') appendToolIndicator(block.name, block.input, 'done');
                });
            } else if (msg.role === 'assistant' && typeof msg.content === 'string') {
                appendAIMessage('assistant', msg.content);
            }
        });
    }
};
</script>

<!-- AI Chat Toggle Button -->
<button class="ai-chat-toggle" onclick="toggleAIChat()" title="AI Audit Assistant">AI</button>

<!-- AI Chat Panel -->
<div id="ai-chat-panel" style="display:none">
    <div class="ai-chat-header">
        <span>AI Audit Assistant</span>
        <button onclick="clearAIChat()" title="Clear chat" style="font-size:12px;">&#x1f5d1;</button>
        <button onclick="openAISettings()" title="Settings">&#9881;</button>
        <button onclick="toggleAIChat()" title="Close">&#10005;</button>
    </div>
    <div class="ai-skills-bar" id="ai-skills-bar">
        <span class="ai-skill-chip" data-skill="audit-working-papers" onclick="toggleSkillChip(this)" title="AWP templates, index structure">Working Papers</span>
        <span class="ai-skill-chip" data-skill="financial-statements" onclick="toggleSkillChip(this)" title="MPERS/MFRS FS preparation">Financial Statements</span>
        <span class="ai-skill-chip" data-skill="pbc-query-management" onclick="toggleSkillChip(this)" title="PBC checklists, query lists">PBC & Queries</span>
        <span class="ai-skill-chip more-btn" onclick="toggleMoreSkills()" id="ai-more-skills-btn" title="Show more skills">+ More</span>
        <span class="ai-skill-chip" data-skill="materiality" onclick="toggleSkillChip(this)" title="Materiality calculation" style="display:none" data-extra="1">Materiality</span>
        <span class="ai-skill-chip" data-skill="risk-assessment" onclick="toggleSkillChip(this)" title="Risk assessment" style="display:none" data-extra="1">Risk Assessment</span>
    </div>
    <div id="ai-chat-messages"></div>
    <div class="ai-actions">
        <button class="ai-action-btn" onclick="document.getElementById('ai-input').value='List all workpaper files';sendAIMessage();">List files</button>
        <button class="ai-action-btn" onclick="if(currentFile.folder){document.getElementById('ai-input').value='Read and summarize '+currentFile.name;sendAIMessage();}">Summarize current</button>
        <button class="ai-action-btn" onclick="document.getElementById('ai-input').value='Check completeness across all audit sections';sendAIMessage();">Check completeness</button>
    </div>
    <div class="ai-chat-input-area">
        <textarea id="ai-input" placeholder="Ask about workpapers..." rows="1" onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendAIMessage();}" oninput="this.style.height='auto';this.style.height=Math.min(this.scrollHeight,100)+'px';"></textarea>
        <button id="ai-send-btn" onclick="sendAIMessage()" title="Send">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
        </button>
    </div>
</div>

<!-- AI Settings Modal -->
<div id="ai-settings-modal" class="modal-overlay" style="display:none" onclick="if(event.target===this)this.style.display='none'">
    <div class="modal-content modal-sm" style="max-width:400px;">
        <h3 style="margin-bottom:16px;font-size:16px;color:#1e293b;">AI Assistant Settings</h3>
        <div class="modal-field">
            <label>Anthropic API Key</label>
            <input type="password" id="ai-key-input" placeholder="sk-ant-..." style="width:100%;padding:8px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:13px;">
            <p style="font-size:11px;color:#94a3b8;margin-top:4px;">Your key is stored locally in your browser only.</p>
        </div>
        <div class="modal-field" style="margin-top:12px;">
            <label>Model</label>
            <select id="ai-model-select" style="width:100%;padding:8px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:13px;">
                <option value="claude-sonnet-4-20250514">Claude Sonnet 4 (Recommended)</option>
                <option value="claude-haiku-4-5-20251001">Claude Haiku 4.5 (Faster)</option>
                <option value="claude-opus-4-6">Claude Opus 4.6 (Most Capable)</option>
            </select>
        </div>
        <div style="display:flex;gap:8px;margin-top:20px;justify-content:flex-end;">
            <button onclick="document.getElementById('ai-settings-modal').style.display='none'" style="padding:8px 16px;border:1px solid #d1d5db;border-radius:6px;background:#fff;cursor:pointer;font-size:13px;">Cancel</button>
            <button onclick="saveAISettings()" style="padding:8px 16px;border:none;border-radius:6px;background:#4f46e5;color:#fff;cursor:pointer;font-size:13px;">Save</button>
        </div>
    </div>
</div>

</body>
</html>
```

---

## 4. master_data.json

```json
{
  "_meta": {
    "version": "1.0",
    "lastModified": "",
    "description": "Master data variables for [CLIENT_NAME] FYE [FYE_YEAR]"
  },
  "variables": {
    "company_name": {
      "value": "",
      "label": "Company Name",
      "category": "company",
      "format": "text"
    },
    "company_reg_no": {
      "value": "",
      "label": "Company Registration No.",
      "category": "company",
      "format": "text"
    },
    "fye_date": {
      "value": "",
      "label": "Financial Year End",
      "category": "company",
      "format": "text"
    },
    "fye_year": {
      "value": "",
      "label": "FYE Year",
      "category": "company",
      "format": "text"
    },
    "reporting_framework": {
      "value": "MPERS",
      "label": "Reporting Framework",
      "category": "company",
      "format": "text"
    },
    "registered_address": {
      "value": "",
      "label": "Registered Address",
      "category": "company",
      "format": "text"
    },
    "business_address": {
      "value": "",
      "label": "Business Address",
      "category": "company",
      "format": "text"
    },
    "nature_of_business": {
      "value": "",
      "label": "Nature of Business",
      "category": "company",
      "format": "text"
    },
    "date_of_incorporation": {
      "value": "",
      "label": "Date of Incorporation",
      "category": "company",
      "format": "text"
    },
    "paid_up_capital": {
      "value": 0,
      "label": "Paid-up Capital",
      "category": "company",
      "format": "currency"
    },
    "total_revenue": {
      "value": 0,
      "label": "Total Revenue",
      "category": "financial",
      "format": "currency"
    },
    "total_assets": {
      "value": 0,
      "label": "Total Assets",
      "category": "financial",
      "format": "currency"
    },
    "total_liabilities": {
      "value": 0,
      "label": "Total Liabilities",
      "category": "financial",
      "format": "currency"
    },
    "total_equity": {
      "value": 0,
      "label": "Total Equity",
      "category": "financial",
      "format": "currency",
      "formula": "total_assets - total_liabilities"
    },
    "net_profit_before_tax": {
      "value": 0,
      "label": "Net Profit Before Tax",
      "category": "financial",
      "format": "currency"
    },
    "net_profit_after_tax": {
      "value": 0,
      "label": "Net Profit After Tax",
      "category": "financial",
      "format": "currency"
    },
    "cost_of_sales": {
      "value": 0,
      "label": "Cost of Sales",
      "category": "financial",
      "format": "currency"
    },
    "gross_profit": {
      "value": 0,
      "label": "Gross Profit",
      "category": "financial",
      "format": "currency",
      "formula": "total_revenue - cost_of_sales"
    },
    "total_operating_expenses": {
      "value": 0,
      "label": "Total Operating Expenses",
      "category": "financial",
      "format": "currency"
    },
    "cash_and_bank": {
      "value": 0,
      "label": "Cash & Bank Balances",
      "category": "financial",
      "format": "currency"
    },
    "trade_receivables": {
      "value": 0,
      "label": "Trade Receivables",
      "category": "financial",
      "format": "currency"
    },
    "inventory": {
      "value": 0,
      "label": "Inventory",
      "category": "financial",
      "format": "currency"
    },
    "ppe_net": {
      "value": 0,
      "label": "PPE (Net Book Value)",
      "category": "financial",
      "format": "currency"
    },
    "trade_payables": {
      "value": 0,
      "label": "Trade Payables",
      "category": "financial",
      "format": "currency"
    },
    "borrowings": {
      "value": 0,
      "label": "Borrowings",
      "category": "financial",
      "format": "currency"
    },
    "share_capital": {
      "value": 0,
      "label": "Share Capital",
      "category": "financial",
      "format": "currency"
    },
    "retained_earnings": {
      "value": 0,
      "label": "Retained Earnings",
      "category": "financial",
      "format": "currency"
    },
    "auditor_firm": {
      "value": "",
      "label": "Audit Firm",
      "category": "audit",
      "format": "text"
    },
    "engagement_partner": {
      "value": "",
      "label": "Engagement Partner",
      "category": "audit",
      "format": "text"
    },
    "materiality_level": {
      "value": 0,
      "label": "Overall Materiality",
      "category": "audit",
      "format": "currency"
    },
    "performance_materiality": {
      "value": 0,
      "label": "Performance Materiality",
      "category": "audit",
      "format": "currency"
    },
    "trivial_threshold": {
      "value": 0,
      "label": "Trivial Threshold (AMPT)",
      "category": "audit",
      "format": "currency"
    },
    "audit_opinion": {
      "value": "Unmodified",
      "label": "Audit Opinion",
      "category": "audit",
      "format": "text"
    },
    "prior_year_revenue": {
      "value": 0,
      "label": "Prior Year Revenue",
      "category": "financial",
      "format": "currency"
    },
    "prior_year_total_assets": {
      "value": 0,
      "label": "Prior Year Total Assets",
      "category": "financial",
      "format": "currency"
    },
    "prior_year_net_profit": {
      "value": 0,
      "label": "Prior Year Net Profit",
      "category": "financial",
      "format": "currency"
    }
  },
  "categories": {
    "company": {
      "label": "Company Identity",
      "order": 1
    },
    "financial": {
      "label": "Key Financial Figures",
      "order": 2
    },
    "audit": {
      "label": "Audit Information",
      "order": 3
    }
  }
}
```
