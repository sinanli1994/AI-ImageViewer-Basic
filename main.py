import sys
import os
import json
import traceback
from PIL import Image

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QSplitter, QTextBrowser, QFileDialog,
    QToolBar, QMessageBox, QFrame, QPushButton, QSizePolicy,
    QStackedWidget, QScrollArea
)
from PyQt6.QtGui import (
    QPixmap, QIcon, QAction, QDragEnterEvent, QDropEvent,
    QImage, QResizeEvent, QColor, QPainter,
    QShortcut, QKeySequence
)
from PyQt6.QtCore import Qt, QSize, QTimer, QUrl

# --- 异常捕获 ---
def exception_hook(exctype, value, tb):
    err_msg = "".join(traceback.format_exception(exctype, value, tb))
    print(err_msg)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Error")
    msg.setText("An unexpected error occurred.")
    msg.setDetailedText(err_msg)
    msg.exec()

sys.excepthook = exception_hook

VALID_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')

# ==========================================
# --- 🎨 现代原生风格配色 (Modern Native) ---
# ==========================================
class NativeTheme:
    FONT_FAMILY = "'Segoe UI', 'Microsoft YaHei', sans-serif"

    LIGHT = {
        "bg_main": "#ffffff",
        "bg_panel": "#fcfcfc",
        "text_main": "#333333",
        "text_sub": "#666666",
        "accent": "#0067c0",
        "border": "#e5e5e5",
        "hover": "#f0f0f0",
        "selected": "#e8f1fa",
        "prompt_bg": "#f0f6ff",
        "neg_bg": "#fff5f5",
        "code_bg": "#f7f7f7"
    }

    DARK = {
        "bg_main": "#202020",
        "bg_panel": "#2b2b2b",
        "text_main": "#e0e0e0",
        "text_sub": "#aaaaaa",
        "accent": "#4cc2ff",
        "border": "#3d3d3d",
        "hover": "#333333",
        "selected": "#3a3a3a",
        "prompt_bg": "#2a3a4a",
        "neg_bg": "#4a2a2a",
        "code_bg": "#333333"
    }


# --- 多语言字典 ---
TRANSLATIONS = {
    'en': {
        'title': "AI Image Metadata Viewer (Basic)",
        'open_file': "Open Image",
        'clear': "Clear All",
        'theme': "Theme",
        'lang_btn': "中文",
        'drag_hint': "Drop image here to view",
        'preview': "Preview",
        'file_info': "Metadata",
        'filename': "File:",
        'size': "Size:",
        'model': "Model",
        'prompt': "Prompt",
        'negative': "Negative",
        'params': "Settings",
        'copy_btn': "Copy",
        'no_data': "No Metadata Detected",
        'no_data_desc': "This image does not contain generation data.",
        'comfy_err': "ComfyUI Parse Error",
        'copied': "Copied!",
        'width': "W",
        'height': "H",
        'cleared': "Cleared",
        'lora': "LoRA",
    },
    'cn': {
        'title': "AI 图片元数据查看器 (基础版)",
        'open_file': "打开图片",
        'clear': "清空",
        'theme': "切换主题",
        'lang_btn': "English",
        'drag_hint': "拖入图片查看元数据",
        'preview': "预览",
        'file_info': "元数据详情",
        'filename': "文件:",
        'size': "尺寸:",
        'model': "基础模型",
        'prompt': "正向提示词",
        'negative': "负面提示词",
        'params': "生成参数",
        'copy_btn': "复制",
        'no_data': "未检测到元数据",
        'no_data_desc': "该图片可能不是原图或已被清理信息。",
        'comfy_err': "ComfyUI 解析错误",
        'copied': "已复制！",
        'width': "宽",
        'height': "高",
        'cleared': "已清空",
        'lora': "LoRA",
    }
}


def create_emoji_icon(emoji_char, size=64, color: str | None = None):
    """生成 emoji 图标，可选指定颜色"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    font = painter.font()
    font.setFamily("Segoe UI Emoji")
    font.setPixelSize(int(size * 0.6))
    painter.setFont(font)
    if color:
        painter.setPen(QColor(color))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, emoji_char)
    painter.end()
    return QIcon(pixmap)


def pil2pixmap(pil_image):
    if pil_image.mode == "RGB":
        pil_image = pil_image.convert("RGBA")
    elif pil_image.mode == "L":
        pil_image = pil_image.convert("RGBA")
    if pil_image.mode != "RGBA":
        pil_image = pil_image.convert("RGBA")
    r, g, b, a = pil_image.split()
    im_rgba = Image.merge("RGBA", (r, g, b, a))
    data = im_rgba.tobytes("raw", "RGBA")
    qim = QImage(data, im_rgba.size[0], im_rgba.size[1], QImage.Format.Format_RGBA8888)
    return QPixmap.fromImage(qim)


# --- 自定义滚轮行为的图片滚动区域 ---
class ImageScrollArea(QScrollArea):
    def __init__(self, owner=None, parent=None):
        super().__init__(parent)
        self.owner = owner


# --- 资源路径解析 ---
def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = 'en'
        self.setWindowTitle("AI Image Metadata Viewer Basic v1.0.0")
        self.resize(1200, 800)
        self.setAcceptDrops(True)
        icon_path = resource_path("app.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.dark_mode = False
        self.current_image_path = None
        self.current_pos_text = ""
        self.current_neg_text = ""
        self.last_html = ""

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_toolbar()
        self.setup_ui()
        self.setup_toast()

        self.apply_style()
        self.update_ui_text()
        
        # Start at page 0
        self.stacked_widget.setCurrentIndex(0)

    # ---------- Toast ----------
    def setup_toast(self):
        self.toast_label = QLabel(self)
        self.toast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.toast_label.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(40, 40, 40, 0.9);
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-family: {NativeTheme.FONT_FAMILY};
                font-size: 14px;
                font-weight: 500;
            }}
        """)
        self.toast_label.hide()

    def show_toast(self, message):
        self.toast_label.setText(message)
        self.toast_label.adjustSize()
        x = (self.width() - self.toast_label.width()) // 2
        y = self.height() - 100
        self.toast_label.move(x, y)
        self.toast_label.show()
        self.toast_label.raise_()
        QTimer.singleShot(2000, self.toast_label.hide)

    # ---------- i18n ----------
    def tr(self, key):
        return TRANSLATIONS[self.lang].get(key, key)

    # ---------- Toolbar ----------
    def setup_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(20, 20))
        self.toolbar.setMovable(False)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.addToolBar(self.toolbar)

        # 打开图片
        self.action_file = QAction(self.tr('open_file'), self)
        self.action_file.setIcon(create_emoji_icon("📄"))
        self.action_file.triggered.connect(self.open_file_dialog)
        self.toolbar.addAction(self.action_file)

        # 中间空白
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(empty)

        # 语言 / 主题 / 清空
        self.lang_action = QAction(self.tr('lang_btn'), self)
        self.lang_action.setIcon(create_emoji_icon("🌐"))
        self.lang_action.triggered.connect(self.toggle_language)
        self.toolbar.addAction(self.lang_action)

        self.theme_action = QAction(self.tr('theme'), self)
        self.theme_action.setIcon(create_emoji_icon("🌗"))
        self.theme_action.triggered.connect(self.toggle_theme)
        self.toolbar.addAction(self.theme_action)

        self.action_clear = QAction(self.tr('clear'), self)
        self.action_clear.setIcon(create_emoji_icon("🧹", color="#ff4d4f"))
        self.action_clear.triggered.connect(self.clear_all)
        self.toolbar.addAction(self.action_clear)

    # ---------- UI Setup ----------
    def setup_ui(self):
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        # --- Page 0: Start Screen ---
        self.start_page = QWidget()
        start_layout = QVBoxLayout(self.start_page)
        self.start_label = QLabel(self.tr('drag_hint'))
        self.start_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 初始大字样式
        self.start_label.setStyleSheet(f"color: #aaa; font-family: {NativeTheme.FONT_FAMILY}; font-size: 32px; font-weight: 300;")
        start_layout.addWidget(self.start_label)
        self.stacked_widget.addWidget(self.start_page)

        # --- Page 1: Split View ---
        self.content_page = QWidget()
        content_layout = QVBoxLayout(self.content_page)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(1)

        # Left: Image Area (Inner)
        self.image_container = QWidget()
        img_layout = QHBoxLayout(self.image_container)
        img_layout.setContentsMargins(0, 0, 0, 0)
        img_layout.setSpacing(0)
        
        self.image_scroll = ImageScrollArea(owner=self)
        self.image_scroll.setWidgetResizable(True)
        self.image_scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        self.image_label = QLabel("")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_scroll.setWidget(self.image_label)
        
        img_layout.addWidget(self.image_scroll)
        
        self.splitter.addWidget(self.image_container)

        # Right: Info Area
        self.info_text = QTextBrowser()
        self.info_text.setOpenExternalLinks(False)
        self.info_text.anchorClicked.connect(self.on_link_clicked)
        self.info_text.setFrameShape(QFrame.Shape.NoFrame)
        self.splitter.addWidget(self.info_text)

        self.splitter.setStretchFactor(0, 70)
        self.splitter.setStretchFactor(1, 30)
        content_layout.addWidget(self.splitter)
        
        self.stacked_widget.addWidget(self.content_page)

    # ---------- Core Logic ----------
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )
        if file_path:
            self.show_image(file_path)

    def show_image(self, path):
        self.current_image_path = path

        # Switch to content page
        self.stacked_widget.setCurrentIndex(1)
        self.action_clear.setEnabled(True)

        # 1. Display Image (Fit)
        self.display_image_fit(path)

        # 2. Parse Metadata
        try:
            with Image.open(path) as img:
                self.parse_metadata(img, path, img.width, img.height)
        except Exception as e:
            print(f"Error loading metadata: {e}")
            self.info_text.setHtml(f"<div style='color:red'>Error reading file: {e}</div>")

        self.update_ui_text_only()

    def display_image_fit(self, path):
        if not path or not os.path.exists(path):
            return
            
        try:
            # Get available size
            view_w = self.image_scroll.viewport().width()
            view_h = self.image_scroll.viewport().height()
            
            if view_w <= 10 or view_h <= 10:
                 # retry slightly later if UI not ready
                QTimer.singleShot(50, lambda: self.display_image_fit(path))
                return

            # --- High DPI Fix Start ---
            dpr = self.image_label.devicePixelRatio()
            target_w = int((view_w - 10) * dpr)
            target_h = int((view_h - 10) * dpr)

            with Image.open(path) as img:
                pixmap = pil2pixmap(img)
                scaled = pixmap.scaled(
                    target_w,
                    target_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                scaled.setDevicePixelRatio(dpr)
                self.image_label.setPixmap(scaled)
            # --- High DPI Fix End ---
        except Exception:
            self.image_label.setText("Error displaying image")

    def resizeEvent(self, event: QResizeEvent):
        if self.current_image_path and self.stacked_widget.currentIndex() == 1:
             QTimer.singleShot(50, lambda: self.display_image_fit(self.current_image_path))
        super().resizeEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        try:
            urls = event.mimeData().urls()
            if urls:
                path = urls[0].toLocalFile()
                if os.path.isfile(path) and path.lower().endswith(VALID_EXTENSIONS):
                    self.show_image(path)
        except:
            pass

    def clear_all(self):
        self.current_image_path = None
        self.current_pos_text = ""
        self.current_neg_text = ""
        self.last_html = ""
        
        self.image_label.clear()
        self.info_text.clear()
        
        # Back to Start Page
        self.stacked_widget.setCurrentIndex(0)
        
        self.show_toast(self.tr('cleared'))

    def toggle_language(self):
        self.lang = 'cn' if self.lang == 'en' else 'en'
        self.update_ui_text()

    def update_ui_text(self):
        self.update_ui_text_only()
        # Refresh metadata view if image loaded to update headers labels
        if self.current_image_path:
             try:
                with Image.open(self.current_image_path) as img:
                    self.parse_metadata(img, self.current_image_path, img.width, img.height)
             except:
                pass

    def update_ui_text_only(self):
        self.setWindowTitle(self.tr('title'))
        self.action_file.setText(self.tr('open_file'))
        self.action_clear.setText(self.tr('clear'))
        self.theme_action.setText(self.tr('theme'))
        self.lang_action.setText(self.tr('lang_btn'))
        
        self.start_label.setText(self.tr('drag_hint'))

    def on_link_clicked(self, url: QUrl):
        if url.toString() == 'copy_pos':
            QApplication.clipboard().setText(self.current_pos_text)
            self.show_toast(self.tr('copied'))
            self.info_text.setHtml(self.last_html)
        elif url.toString() == 'copy_neg':
            QApplication.clipboard().setText(self.current_neg_text)
            self.show_toast(self.tr('copied'))
            self.info_text.setHtml(self.last_html)

    # ---------- 主题 + 元数据解析 (COPIED FROM ORIGIN) ----------
    def get_theme(self):
        return NativeTheme.DARK if self.dark_mode else NativeTheme.LIGHT

    def parse_comfy_data(self, comfy_json):
        t = self.get_theme()
        try:
            data = json.loads(comfy_json)
            pos, neg = "", ""
            params = {}
            sampler_node = None
            model_lines = []
            qwen_pos_candidate = ""
            qwen_neg_candidate = ""
            lora_infos = []

            for key, node in data.items():
                ctype = node.get('class_type', '')
                inputs = node.get('inputs', {}) or {}
                ctype_lower = ctype.lower()

                if 'checkpointloader' in ctype_lower:
                    name = inputs.get('ckpt_name') or inputs.get('model_name') or inputs.get('ckpt_path') or ''
                    if name:
                        line = f"Checkpoint: {name}"
                        if line not in model_lines: model_lines.append(line)

                if 'unet' in ctype_lower:
                    name = inputs.get('unet_name') or inputs.get('model') or inputs.get('name') or ''
                    if name:
                        line = f"Diffusion Model: {name}"
                        if line not in model_lines: model_lines.append(line)

                if 'ksampler' in ctype_lower:
                    sampler_node = node
                    for k in ['seed', 'steps', 'cfg', 'sampler_name', 'scheduler', 'denoise']:
                        if k in inputs:
                            params[k.capitalize()] = inputs[k]

                if 'lora' in ctype_lower:
                    name = inputs.get('lora_name') or inputs.get('model') or inputs.get('name') or ''
                    sm = inputs.get('strength_model', None)
                    sc = inputs.get('strength_clip', None)
                    parts = []
                    if name: parts.append(str(name))
                    if sm is not None: parts.append(f"model: {sm}")
                    if sc is not None: parts.append(f"clip: {sc}")
                    if parts: lora_infos.append(" | ".join(parts))

                if 'qwen' in ctype_lower:
                    p = inputs.get('prompt') or inputs.get('text') or ""
                    n = inputs.get('negative_prompt') or inputs.get('negative') or ""
                    if isinstance(p, str) and p.strip(): qwen_pos_candidate = p.strip()
                    if isinstance(n, str) and n.strip(): qwen_neg_candidate = n.strip()

            if sampler_node:
                inputs = sampler_node.get('inputs', {}) or {}
                for key, prompt_type in [('positive', 'pos'), ('negative', 'neg')]:
                    ref = inputs.get(key)
                    if ref:
                        text_node = data.get(str(ref[0]), {})
                        text = text_node.get('inputs', {}).get('text', '')
                        if prompt_type == 'pos': pos = text
                        else: neg = text

            if not pos and not neg:
                for key, node in data.items():
                    if 'cliptextencode' in node.get('class_type', '').lower():
                        text = node.get('inputs', {}).get('text', '')
                        if not text: continue
                        if any(x in text.lower() for x in ['quality', 'nsfw', 'worst']):
                            if not neg: neg = text
                        else:
                            if not pos: pos = text

            if (not pos) and qwen_pos_candidate: pos = qwen_pos_candidate
            if (not neg) and qwen_neg_candidate: neg = qwen_neg_candidate

            self.current_pos_text, self.current_neg_text = pos, neg

            copy_style = (
                f"text-decoration:none; font-size:12px; color:{t['accent']}; "
                f"border:1px solid {t['accent']}; padding:2px 8px; border-radius:10px;"
            )

            def make_header(title, copy_link=None):
                btn = f"<a href='{copy_link}' style='{copy_style}'>{self.tr('copy_btn')}</a>" if copy_link else ""
                return (
                    "<div style='margin-bottom:6px; margin-top:16px;'>"
                    f"<span style='color:{t['text_sub']}; font-weight:bold; font-size:13px;'>{title}</span> &nbsp; {btn}</div>"
                )

            html = ""
            if model_lines:
                html += make_header(self.tr('model'))
                html += f"<div style='color:{t['accent']}; font-weight:bold;'>" + "<br>".join(model_lines) + "</div>"

            if lora_infos:
                html += make_header(self.tr('lora'))
                html += (
                    f"<div style='background:{t['code_bg']}; padding:10px; "
                    f"border-radius:6px; color:{t['text_sub']}; font-family:Consolas; font-size:12px;'>"
                    + "<br>".join(lora_infos) + "</div>"
                )

            if pos:
                html += make_header(self.tr('prompt'), 'copy_pos')
                html += (
                    f"<div style='background:{t['prompt_bg']}; padding:10px; "
                    f"border-radius:6px; line-height:1.5;'>{pos}</div>"
                )

            if neg:
                html += make_header(self.tr('negative'), 'copy_neg')
                html += (
                    f"<div style='background:{t['neg_bg']}; padding:10px; "
                    f"border-radius:6px; line-height:1.5;'>{neg}</div>"
                )

            if params:
                html += make_header(self.tr('params'))
                html += (
                    f"<div style='background:{t['code_bg']}; padding:10px; border-radius:6px; "
                    f"color:{t['text_sub']}; font-family:Consolas; font-size:12px;'>"
                    + " | ".join([f"{k}: {v}" for k, v in params.items()]) + "</div>"
                )
            return html
        except:
            return self.tr('comfy_err')

    def parse_metadata(self, img, path, w, h):
        t = self.get_theme()
        self.current_pos_text, self.current_neg_text = "", ""

        html = (
            f"<div style='font-size:16px; font-weight:bold; color:{t['text_main']};'>"
            f"{os.path.basename(path)} <span style='color:{t['accent']}; font-size:12px; vertical-align:middle;'>[Basic Edition]</span></div>"
        )
        html += (
            f"<div style='color:{t['text_sub']}; margin-bottom:15px;'>{w} x {h} px</div>"
            f"<hr style='border:0; border-top:1px solid {t['border']};'>"
        )

        info = img.info
        if 'prompt' in info:
            html += self.parse_comfy_data(info['prompt'])
        elif 'parameters' in info:
            text = info['parameters']
            parts = text.split("Negative prompt:")
            pos = parts[0].strip()
            neg = ""
            if len(parts) > 1:
                if "Steps:" in parts[1]:
                    neg = parts[1].split("Steps:")[0].strip()
                else:
                    neg = parts[1].strip()

            full_params = ""
            if "Steps:" in text:
                full_params = "Steps:" + text.split("Steps:", 1)[1].strip()

            model_name = ""
            if full_params:
                idx_m = full_params.find("Model:")
                if idx_m != -1:
                    after = full_params[idx_m + len("Model:"):].lstrip()
                    end_m = after.find(",")
                    if end_m != -1:
                        model_name = after[:end_m].strip()
                        full_params = (full_params[:idx_m].rstrip(" ,") + ", " + after[end_m + 1:].lstrip()).strip(" ,")
                    else:
                        model_name = after.strip()
                        full_params = full_params[:idx_m].rstrip(" ,")

            lora_list = []
            params_display = full_params
            if full_params:
                lower = full_params.lower()
                idx = lower.find("lora:")
                if idx != -1:
                    cut_start = idx + len("lora:")
                    lora_part = full_params[cut_start:].strip(" ,")
                    lora_items = [s.strip() for s in lora_part.split(",") if s.strip()]
                    if lora_items: lora_list = lora_items
                    params_display = full_params[:idx].rstrip(" ,")

            self.current_pos_text, self.current_neg_text = pos, neg

            copy_style = (
                f"text-decoration:none; font-size:12px; color:{t['accent']}; "
                f"border:1px solid {t['accent']}; padding:2px 8px; border-radius:10px;"
            )
            def make_header(title, copy_link=None):
                btn = f"<a href='{copy_link}' style='{copy_style}'>{self.tr('copy_btn')}</a>" if copy_link else ""
                return (
                    "<div style='margin-bottom:6px; margin-top:16px;'>"
                    f"<span style='color:{t['text_sub']}; font-weight:bold; font-size:13px;'>{title}</span> &nbsp; {btn}</div>"
                )

            if model_name:
                html += make_header(self.tr('model'))
                html += f"<div style='color:{t['accent']}; font-weight:bold;'>{model_name}</div>"

            html += make_header(self.tr('prompt'), 'copy_pos')
            html += (
                f"<div style='background:{t['prompt_bg']}; padding:10px; "
                f"border-radius:6px; line-height:1.5;'>{pos}</div>"
            )

            if neg:
                html += make_header(self.tr('negative'), 'copy_neg')
                html += (
                    f"<div style='background:{t['neg_bg']}; padding:10px; "
                    f"border-radius:6px; line-height:1.5;'>{neg}</div>"
                )

            if lora_list:
                html += make_header(self.tr('lora'))
                html += (
                    f"<div style='background:{t['code_bg']}; padding:10px; "
                    f"border-radius:6px; color:{t['text_sub']}; font-family:Consolas; font-size:12px;'>"
                    + "<br>".join(lora_list) + "</div>"
                )

            if params_display:
                html += make_header(self.tr('params'))
                html += (
                    f"<div style='background:{t['code_bg']}; padding:10px; border-radius:10px; "
                    f"color:{t['text_sub']}; font-family:Consolas; font-size:12px; line-height:1.5;'>{params_display}</div>"
                )

        else:
            html += f"<p style='color:{t['text_sub']}; margin-top:20px;'>{self.tr('no_data_desc')}</p>"

        self.last_html = html
        self.info_text.setHtml(html)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_style()
        self.update_ui_text_only()
        if self.current_image_path:
             try:
                with Image.open(self.current_image_path) as img:
                    self.parse_metadata(img, self.current_image_path, img.width, img.height)
             except:
                pass


    def apply_style(self):
        t = self.get_theme()
        btn_color = "rgba(255,255,255,0.7)" if self.dark_mode else "rgba(0,0,0,0.5)"
        btn_hover = "rgba(255,255,255,0.1)" if self.dark_mode else "rgba(0,0,0,0.05)"

        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {t['bg_main']};
                color: {t['text_main']};
                font-family: {NativeTheme.FONT_FAMILY};
            }}
            QToolBar {{
                background-color: {t['bg_main']};
                border-bottom: 1px solid {t['border']};
                padding: 5px;
                spacing: 10px;
            }}
            QToolButton {{
                background-color: transparent;
                border-radius: 4px;
                padding: 6px 10px;
                color: {t['text_main']};
                font-size: 13px;
            }}
            QToolButton:hover {{
                background-color: {t['hover']};
            }}
            QTextBrowser {{
                background-color: {t['bg_panel']};
                border-left: 1px solid {t['border']};
                padding: 20px;
                font-size: 14px;
            }}
            QSplitter::handle {{
                background-color: {t['border']};
            }}
             QPushButton {{
                color: {btn_color};
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
                color: {t['accent']};
            }}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = app.font()
    font.setFamily("Segoe UI")
    app.setFont(font)

    def resource_path(relative_path: str) -> str:
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    icon_path = resource_path("app.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
