# Viewer Templates

## START_VIEWER.bat

```batch
@echo off
title Audit Working Papers Viewer - [CLIENT NAME]
color 0A

echo.
echo  ========================================================
echo.
echo     [CLIENT NAME]
echo     Audit Working Papers Viewer
echo.
echo     Company No: [COMPANY NUMBER]
echo     FYE: [FINANCIAL YEAR END]
echo.
echo  ========================================================
echo.
echo  Starting server on PORT 8888...
echo.

cd /d "%~dp0"

:: Try to open browser after 2 seconds
start "" cmd /c "timeout /t 2 >nul && start http://localhost:8888/audit_viewer.html"

:: Start Python HTTP server
echo  Server running at: http://localhost:8888/audit_viewer.html
echo.
echo  --------------------------------------------------------
echo  FEATURES:
echo    - Click documents to preview
echo    - Search working papers (Ctrl+F)
echo    - Download All for offline viewing
echo  --------------------------------------------------------
echo.
echo  Press Ctrl+C to stop the server when done.
echo.

python -m http.server 8888

:: If Python fails, try python3
if %errorlevel% neq 0 (
    echo.
    echo  Python not found. Trying python3...
    python3 -m http.server 8888
)

:: If still fails, show error
if %errorlevel% neq 0 (
    echo.
    echo  ========================================================
    echo  ERROR: Python is not installed.
    echo.
    echo  Please install Python from:
    echo  https://www.python.org/downloads/
    echo.
    echo  Or open audit_viewer.html directly in your browser.
    echo  ========================================================
    pause
)
```

## audit_viewer.html Structure

The HTML file must follow this structure:

### 1. Head Section
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AWP Viewer - [CLIENT NAME]</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- All CSS inline -->
</head>
```

### 2. Sections Array (JavaScript)
```javascript
const sections = [
    {
        name: "A - Planning",
        folder: "A_Planning",
        items: [
            { file: "A1_Planning_Memo.md", name: "Planning Memorandum", ref: "A1" },
            { file: "A2_Materiality.md", name: "Materiality", ref: "A2" }
        ]
    },
    // ... more sections
];
```

### 3. Key CSS Rules
- Nav panel: `background: #1e293b; color: white; width: 300px`
- Preview: `flex: 1; background: white; padding: 40px`
- Tables: `border-collapse: collapse` with alternating `#f8fafc` rows
- Download button: `background: #22c55e; color: white` at bottom of nav

### 4. Download All Function
The `downloadAllDocuments()` function must:
1. Fetch all `.md` files from sections array
2. Convert markdown to HTML using `marked.parse()`
3. Build standalone HTML with navigation sidebar
4. Use string concatenation for script tags: `'<scr' + 'ipt>'`
5. Store all content in hidden `<div>` elements
6. Trigger download as `.html` file
