# AI Image Viewer – Basic

A minimal offline viewer for AI-generated image metadata.

Open an image and instantly view its prompt and generation parameters.

---

## Download

Prebuilt Windows executable is available on the Releases page:

https://github.com/sinanli1994/AI-ImageViewer-Basic/releases

---

## Features

- Drag & drop image support
- View embedded metadata (ComfyUI, Stable Diffusion)
- Clean and distraction-free interface
- Fully offline – no telemetry, no internet connection required

---

## Installation (Source)

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application:

```bash
python main.py
```

---

## Build Executable (Optional)

To create a standalone executable:

```bash
pyinstaller --noconsole --onefile --icon=app.ico --add-data "app.ico;." --version-file=version.txt --name=AI_ImageViewer_Basic main.py
```

---

If you find this tool useful, you can support future development:

☕ https://buymeacoffee.com/creativelax
