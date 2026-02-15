# AI Image Viewer - Basic Version

A lightweight, local image viewer with metadata inspection capabilities.

## Features
- Fast image viewing (drag & drop support).
- Inspect metadata for AI-generated images (ComfyUI, Stable Diffusion).
- Clean and simple interface.

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application:
```bash
python main.py
```

## Packaging
To create a standalone executable:
```bash
pyinstaller --noconsole --onefile --icon=app.ico --add-data "app.ico;." --version-file=version.txt --name=AI_ImageViewer_Basic main.py
```
