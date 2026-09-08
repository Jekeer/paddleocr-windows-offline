import sys
import os
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QSplitter,
    QProgressBar,
)

from paddleocr import PaddleOCR


APP_NAME = "PaddleOCR Offline"


SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".webp",
    ".tiff",
    ".tif",
}


def get_base_path():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent

    return Path(__file__).resolve().parent


def get_model_paths():
    base_path = get_base_path()

    models_path = base_path / "models"

    det_model = models_path / "det"
    rec_model = models_path / "rec"
    cls_model = models_path / "cls"

    return (
        str(det_model),
        str(rec_model),
        str(cls_model),
    )


class OCRWorker(QThread):

    finished = Signal(str)
    error = Signal(str)
    status = Signal(str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        try:
            self.status.emit(
                "正在加载本地 OCR 模型..."
            )

            (
                det_model_dir,
                rec_model_dir,
                cls_model_dir,
            ) = get_model_paths()

            for model_dir in (
                det_model_dir,
                rec_model_dir,
                cls_model_dir,
            ):
                if not os.path.exists(model_dir):
                    raise RuntimeError(
                        f"本地 OCR 模型不存在：\n{model_dir}"
                    )

            ocr = PaddleOCR(
                use_angle_cls=True,
                lang="ch",
                det_model_dir=det_model_dir,
                rec_model_dir=rec_model_dir,
                cls_model_dir=cls_model_dir,
                use_gpu=False,
                show_log=False,
            )

            self.status.emit(
                "正在识别图片..."
            )

            result = ocr.ocr(
                self.image_path,
                cls=True,
            )

            lines = []

            if result and result[0]:
                for item in result[0]:
                    text = item[1][0]
                    lines.append(text)

            text_result = "\n".join(lines)

            if not text_result.strip():
                text_result = "未识别到文字。"

            self.finished.emit(
                text_result
            )

        except Exception as e:
            self.error.emit(
                str(e)
            )


class ImagePreview(QLabel):

    fileDropped = Signal(str)

    def __init__(self):
        super().__init__()

        self.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.setAcceptDrops(True)

        self.setText(
            "将图片拖到这里\n\n"
            "或者点击下方「选择图片」"
        )

        self.setStyleSheet(
            """
            QLabel {
                border: 2px dashed #777;
                border-radius: 10px;
                background-color: #202124;
                color: #cccccc;
                font-size: 18px;
            }
            """
        )

        self.image_path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()

        if not urls:
            return

        path = urls[0].toLocalFile()

        if path:
            self.fileDropped.emit(path)

    def load_image(self, image_path):
        self.image_path = image_path

        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            self.setText(
                "无法加载图片"
            )
            return

        self.update_preview()

    def update_preview(self):
        if not self.image_path:
            return

        pixmap = QPixmap(
            self.image_path
        )

        if pixmap.isNull():
            return

        scaled = pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.setPixmap(
            scaled
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_preview()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_image = None
        self.worker = None

        self.setWindowTitle(
            APP_NAME
        )

        self.resize(
            1200,
            720,
        )

        self.init_ui()

    def init_ui(self):
        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QVBoxLayout(
            central
        )

        main_layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        title = QLabel(
            "PaddleOCR Offline"
        )

        title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            """
        )

        main_layout.addWidget(
            title
        )

        subtitle = QLabel(
            "Windows · CPU · 完全本地离线 OCR"
        )

        subtitle.setStyleSheet(
            """
            color: #888888;
            font-size: 13px;
            """
        )

        main_layout.addWidget(
            subtitle
        )

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.preview = ImagePreview()

        self.preview.fileDropped.connect(
            self.load_image
        )

        self.result_text = QTextEdit()

        self.result_text.setPlaceholderText(
            "OCR 识别结果会显示在这里..."
        )

        self.result_text.setStyleSheet(
            """
            QTextEdit {
                font-size: 15px;
                padding: 10px;
            }
            """
        )

        splitter.addWidget(
            self.preview
        )

        splitter.addWidget(
            self.result_text
        )

        splitter.setSizes(
            [600, 600]
        )

        main_layout.addWidget(
            splitter
        )

        self.progress = QProgressBar()

        self.progress.setVisible(
            False
        )

        main_layout.addWidget(
            self.progress
        )

        self.status_label = QLabel(
            "就绪"
        )

        self.status_label.setStyleSheet(
            """
            color: #888888;
            """
        )

        main_layout.addWidget(
            self.status_label
        )

        button_layout = QHBoxLayout()

        self.select_button = QPushButton(
            "选择图片"
        )

        self.ocr_button = QPushButton(
            "开始识别"
        )

        self.copy_button = QPushButton(
            "复制文字"
        )

        self.save_button = QPushButton(
            "保存 TXT"
        )

        self.clear_button = QPushButton(
            "清空"
        )

        self.ocr_button.setEnabled(
            False
        )

        button_layout.addWidget(
            self.select_button
        )

        button_layout.addWidget(
            self.ocr_button
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.copy_button
        )

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        main_layout.addLayout(
            button_layout
        )

        self.select_button.clicked.connect(
            self.select_image
        )

        self.ocr_button.clicked.connect(
            self.start_ocr
        )

        self.copy_button.clicked.connect(
            self.copy_text
        )

        self.save_button.clicked.connect(
            self.save_text
        )

        self.clear_button.clicked.connect(
            self.clear_all
        )

    def select_image(self):
        file_path, _ = (
            QFileDialog.getOpenFileName(
                self,
                "选择图片",
                "",
                "Images (*.png *.jpg *.jpeg *.bmp *.webp *.tiff *.tif)",
            )
        )

        if file_path:
            self.load_image(
                file_path
            )

    def load_image(self, file_path):
        path = Path(
            file_path
        )

        if (
            path.suffix.lower()
            not in SUPPORTED_EXTENSIONS
        ):
            QMessageBox.warning(
                self,
                "不支持的文件",
                "请选择支持的图片格式。",
            )
            return

        self.current_image = file_path

        self.preview.load_image(
            file_path
        )

        self.status_label.setText(
            f"已加载：{path.name}"
        )

        self.ocr_button.setEnabled(
            True
        )

    def start_ocr(self):
        if not self.current_image:
            QMessageBox.warning(
                self,
                "提示",
                "请先选择图片。",
            )
            return

        self.result_text.clear()

        self.set_busy(
            True
        )

        self.worker = OCRWorker(
            self.current_image
        )

        self.worker.status.connect(
            self.status_label.setText
        )

        self.worker.finished.connect(
            self.ocr_finished
        )

        self.worker.error.connect(
            self.ocr_error
        )

        self.worker.start()

    def ocr_finished(self, text):
        self.result_text.setPlainText(
            text
        )

        self.status_label.setText(
            "识别完成"
        )

        self.set_busy(
            False
        )

    def ocr_error(self, message):
        self.status_label.setText(
            "识别失败"
        )

        self.set_busy(
            False
        )

        QMessageBox.critical(
            self,
            "OCR 错误",
            message,
        )

    def copy_text(self):
        text = (
            self.result_text
            .toPlainText()
        )

        if not text.strip():
            QMessageBox.information(
                self,
                "提示",
                "没有可复制的文字。",
            )
            return

        clipboard = (
            QApplication.clipboard()
        )

        clipboard.setText(
            text
        )

        self.status_label.setText(
            "文字已复制到剪贴板"
        )

    def save_text(self):
        text = (
            self.result_text
            .toPlainText()
        )

        if not text.strip():
            QMessageBox.information(
                self,
                "提示",
                "没有可保存的文字。",
            )
            return

        file_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "保存 TXT",
                "ocr_result.txt",
                "Text Files (*.txt)",
            )
        )

        if not file_path:
            return

        try:
            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as f:
                f.write(
                    text
                )

            self.status_label.setText(
                f"已保存：{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "保存失败",
                str(e),
            )

    def clear_all(self):
        self.current_image = None

        self.preview.clear()

        self.preview.image_path = None

        self.preview.setText(
            "将图片拖到这里\n\n"
            "或者点击下方「选择图片」"
        )

        self.result_text.clear()

        self.status_label.setText(
            "就绪"
        )

        self.ocr_button.setEnabled(
            False
        )

    def set_busy(self, busy):
        self.select_button.setEnabled(
            not busy
        )

        self.ocr_button.setEnabled(
            not busy
            and self.current_image is not None
        )

        self.copy_button.setEnabled(
            not busy
        )

        self.save_button.setEnabled(
            not busy
        )

        self.clear_button.setEnabled(
            not busy
        )

        self.progress.setVisible(
            busy
        )

        if busy:
            self.progress.setRange(
                0,
                0,
            )

        else:
            self.progress.setRange(
                0,
                1,
            )

            self.progress.setValue(
                0
            )


def main():
    QApplication.setApplicationName(
        APP_NAME
    )

    app = QApplication(
        sys.argv
    )

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()