# AI Image Viewer – Basic

A lightweight offline viewer for AI-generated image metadata.

Open an image and instantly view its prompt and generation parameters.  
Designed for images generated with **Stable Diffusion / ComfyUI** workflows.

The application runs completely **offline** — no telemetry, no internet connection required.

---

## Download

Prebuilt Windows executable is available on the Releases page:

https://github.com/sinanli1994/AI-ImageViewer-Basic/releases

---

## Features

- Grid thumbnail browsing
- Open and browse entire folders
- Drag & drop images or folders
- View embedded metadata (ComfyUI, Stable Diffusion)
- Floating sort menu (Name / Modified Time)
- Keyboard navigation (Arrow keys / Enter / Delete)
- Safe delete (images moved to system Recycle Bin)
- Multi-language UI  
  - English  
  - Simplified Chinese  
  - Traditional Chinese  
  - Japanese  
  - Korean
- Remembers language and theme settings after restart
- Clean and distraction-free interface
- Fully offline – no telemetry, no internet connection required

---

## Installation (Source)

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

Dependencies:

- PyQt6
- Pillow
- send2trash

---

## Usage

Run the application:

```bash
python main.py
```

---

## Build Executable (Optional)

To create a standalone Windows executable:

```bash
pyinstaller --noconsole --onefile --icon=app.ico --add-data "app.ico;." --version-file=version.txt --name=AI_ImageViewer_Basic main.py
```

---

## Version

### v1.1.0

Major usability update.

New:
- Grid thumbnail browsing
- Folder loading support
- Floating sort menu (Name / Modified Time)
- Keyboard navigation (Arrow keys / Enter / Delete)
- Safe delete (images moved to system Recycle Bin)

Improvements:
- Improved browsing workflow
- Automatic grid layout based on window size
- UI refinements and smoother navigation

Dependencies:
- Added `send2trash` for safe file deletion

---

### v1.0.1

Updates:
- Added Traditional Chinese, Japanese, and Korean UI languages
- App now remembers language and theme settings after restart

---

### v1.0.0

Initial release.

Basic functionality:
- Drag & drop image support
- View embedded AI image metadata
- Minimal offline interface

---

## Support

If you find this tool useful, you can support future development:

☕ https://buymeacoffee.com/creativelax
