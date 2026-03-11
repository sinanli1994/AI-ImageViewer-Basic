# AI Image Metadata Viewer

A lightweight desktop viewer for metadata embedded in AI-generated images  
(Stable Diffusion / ComfyUI / Automatic1111).

Runs fully offline. No telemetry. No internet connection required.

---

## Screenshots

### Grid browsing

![Grid View](screenshots/grid-view.png)

### Metadata viewer

![Metadata Panel](screenshots/metadata-panel.png)

### Drag & drop interface

![Drop Interface](screenshots/drop-view.png)

---

## Download

Prebuilt Windows executable is available on the Releases page:

https://github.com/sinanli1994/ai-image-metadata-viewer/releases

---

## Features

- View embedded metadata from AI-generated images
- Supports Stable Diffusion and ComfyUI images
- Grid thumbnail browsing
- Folder browsing support
- Drag & drop images or folders
- Floating sort menu (Name / Modified Time)
- Keyboard navigation (Arrow keys / Enter / Delete)
- Safe delete (moves images to system Recycle Bin)

### Interface

- Clean distraction-free UI
- Multi-language interface
  - English
  - Simplified Chinese
  - Traditional Chinese
  - Japanese
  - Korean
- Remembers language and theme settings

### Privacy

- Fully offline
- No telemetry
- No internet connection required

---

## Installation (Source)

Requires Python 3.10+

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
pyinstaller --noconsole --onefile --icon=app.ico --add-data "app.ico;." --version-file=version.txt --name=AI_Image_Metadata_Viewer
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
