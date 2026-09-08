import sys
import os
from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    QSettings,
    QTimer,
)
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
    QDialog,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QDialogButtonBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
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


class SettingsDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings(
            "PaddleOCR Offline",
            "PaddleOCR Offline",
        )

        self.setWindowTitle("设置")

        self.setMinimumWidth(420)

        self.init_ui()

        self.load_settings()

    def init_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        layout.setSpacing(15)

        batch_title = QLabel("批量处理")

        batch_title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            """
        )

        layout.addWidget(batch_title)

        batch_line = QLabel(
            "────────────────────────"
        )

        layout.addWidget(batch_line)

        batch_layout = QHBoxLayout()

        batch_label = QLabel(
            "一次最多添加图片："
        )

        self.max_images_spin = QSpinBox()

        self.max_images_spin.setMinimum(1)

        self.max_images_spin.setMaximum(100)

        self.max_images_spin.setValue(1)

        self.max_images_spin.setSuffix(" 张")

        batch_layout.addWidget(
            batch_label
        )

        batch_layout.addWidget(
            self.max_images_spin
        )

        batch_layout.addStretch()

        layout.addLayout(
            batch_layout
        )

        range_label = QLabel(
            "范围：1 ～ 100"
        )

        range_label.setStyleSheet(
            "color: #888888;"
        )

        layout.addWidget(
            range_label
        )

        layout.addSpacing(10)

        ocr_title = QLabel(
            "OCR"
        )

        ocr_title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            """
        )

        layout.addWidget(
            ocr_title
        )

        ocr_line = QLabel(
            "────────────────────────"
        )

        layout.addWidget(
            ocr_line
        )

        self.angle_cls_checkbox = QCheckBox(
            "启用方向分类"
        )

        layout.addWidget(
            self.angle_cls_checkbox
        )

        self.confidence_checkbox = QCheckBox(
            "保留识别置信度"
        )

        layout.addWidget(
            self.confidence_checkbox
        )

        layout.addSpacing(10)

        output_title = QLabel(
            "输出"
        )

        output_title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            """
        )

        layout.addWidget(
            output_title
        )

        output_line = QLabel(
            "────────────────────────"
        )

        layout.addWidget(
            output_line
        )

        output_layout = QHBoxLayout()

        output_label = QLabel(
            "默认导出格式："
        )

        self.export_format_combo = QComboBox()

        self.export_format_combo.addItems(
            [
                "TXT",
                "Markdown",
            ]
        )

        output_layout.addWidget(
            output_label
        )

        output_layout.addWidget(
            self.export_format_combo
        )

        output_layout.addStretch()

        layout.addLayout(
            output_layout
        )

        layout.addStretch()

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        button_box.button(
            QDialogButtonBox.StandardButton.Ok
        ).setText(
            "确认"
        )

        button_box.button(
            QDialogButtonBox.StandardButton.Cancel
        ).setText(
            "取消"
        )

        button_box.accepted.connect(
            self.save_and_accept
        )

        button_box.rejected.connect(
            self.reject
        )

        layout.addWidget(
            button_box
        )

    def load_settings(self):

        max_images = self.settings.value(
            "max_images",
            1,
            type=int,
        )

        angle_cls = self.settings.value(
            "use_angle_cls",
            True,
            type=bool,
        )

        confidence = self.settings.value(
            "show_confidence",
            False,
            type=bool,
        )

        export_format = self.settings.value(
            "export_format",
            "TXT",
            type=str,
        )

        self.max_images_spin.setValue(
            max_images
        )

        self.angle_cls_checkbox.setChecked(
            angle_cls
        )

        self.confidence_checkbox.setChecked(
            confidence
        )

        index = (
            self.export_format_combo
            .findText(export_format)
        )

        if index >= 0:

            self.export_format_combo.setCurrentIndex(
                index
            )

    def save_and_accept(self):

        self.settings.setValue(
            "max_images",
            self.max_images_spin.value(),
        )

        self.settings.setValue(
            "use_angle_cls",
            self.angle_cls_checkbox.isChecked(),
        )

        self.settings.setValue(
            "show_confidence",
            self.confidence_checkbox.isChecked(),
        )

        self.settings.setValue(
            "export_format",
            self.export_format_combo.currentText(),
        )

        self.accept()


class OCRWorker(QThread):

    status = Signal(str)

    progress = Signal(int, int)

    task_started = Signal(int)

    task_finished = Signal(
        int,
        str,
    )

    task_error = Signal(
        int,
        str,
    )

    finished_all = Signal()

    def __init__(
        self,
        image_paths,
        use_angle_cls,
        show_confidence,
    ):

        super().__init__()

        self.image_paths = image_paths

        self.use_angle_cls = (
            use_angle_cls
        )

        self.show_confidence = (
            show_confidence
        )

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

                if not os.path.exists(
                    model_dir
                ):

                    raise RuntimeError(
                        "本地 OCR 模型不存在：\n"
                        f"{model_dir}"
                    )

            ocr = PaddleOCR(
                use_angle_cls=self.use_angle_cls,
                lang="ch",
                det_model_dir=det_model_dir,
                rec_model_dir=rec_model_dir,
                cls_model_dir=cls_model_dir,
                use_gpu=False,
                show_log=False,
            )

            total = len(
                self.image_paths
            )

            for index, image_path in enumerate(
                self.image_paths
            ):

                current = index + 1

                self.task_started.emit(
                    index
                )

                self.status.emit(
                    f"正在识别 {current} / {total}"
                )

                self.progress.emit(
                    current - 1,
                    total,
                )

                try:

                    result = ocr.ocr(
                        image_path,
                        cls=self.use_angle_cls,
                    )

                    lines = []

                    if (
                        result
                        and result[0]
                    ):

                        for item in result[0]:

                            text = item[1][0]

                            confidence = item[1][1]

                            if (
                                self.show_confidence
                            ):

                                lines.append(
                                    f"{text}"
                                    f"  "
                                    f"[置信度："
                                    f"{confidence * 100:.2f}%]"
                                )

                            else:

                                lines.append(
                                    text
                                )

                    text_result = (
                        "\n".join(
                            lines
                        )
                    )

                    if not text_result.strip():

                        text_result = (
                            "未识别到文字。"
                        )

                    self.task_finished.emit(
                        index,
                        text_result,
                    )

                except Exception as e:

                    self.task_error.emit(
                        index,
                        str(e),
                    )

            self.progress.emit(
                total,
                total,
            )

            self.status.emit(
                "全部识别完成"
            )

            self.finished_all.emit()

        except Exception as e:

            self.status.emit(
                f"OCR 初始化失败：{str(e)}"
            )

            self.finished_all.emit()


class ImagePreview(QLabel):

    fileDropped = Signal(str)

    def __init__(self):

        super().__init__()

        self.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.setAcceptDrops(
            True
        )

        self.setMinimumSize(
            300,
            300,
        )

        self.setText(
            "将图片拖到这里\n\n"
            "或者点击「选择图片」"
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

        self.original_pixmap = None

    def dragEnterEvent(
        self,
        event,
    ):

        if (
            event.mimeData()
            .hasUrls()
        ):

            event.acceptProposedAction()

    def dropEvent(
        self,
        event,
    ):

        urls = (
            event.mimeData()
            .urls()
        )

        if not urls:

            return

        path = (
            urls[0]
            .toLocalFile()
        )

        if path:

            self.fileDropped.emit(
                path
            )

    def load_image(
        self,
        image_path,
    ):

        self.image_path = image_path

        pixmap = QPixmap(
            image_path
        )

        if pixmap.isNull():

            self.original_pixmap = None

            self.setText(
                "无法加载图片"
            )

            return

        self.original_pixmap = pixmap

        self.update_preview()

    def update_preview(self):

        if (
            self.original_pixmap is None
        ):

            return

        available_width = max(
            1,
            self.width() - 20,
        )

        available_height = max(
            1,
            self.height() - 20,
        )

        scaled = (
            self.original_pixmap.scaled(
                available_width,
                available_height,
                Qt.AspectRatioMode
                .KeepAspectRatio,
                Qt.TransformationMode
                .SmoothTransformation,
            )
        )

        self.setPixmap(
            scaled
        )

    def clear_preview(self):

        self.image_path = None

        self.original_pixmap = None

        self.clear()

        self.setText(
            "将图片拖到这里\n\n"
            "或者点击「选择图片」"
        )

    def resizeEvent(
        self,
        event,
    ):

        super().resizeEvent(
            event
        )

        self.update_preview()


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.settings = QSettings(
            "PaddleOCR Offline",
            "PaddleOCR Offline",
        )

        self.image_paths = []

        self.ocr_results = {}

        self.task_status = {}

        self.current_index = None

        self.worker = None

        self.load_settings()

        self.setWindowTitle(
            APP_NAME
        )

        self.resize(
            1300,
            760,
        )

        self.init_ui()

        self.update_mode_layout()

        QTimer.singleShot(
            0,
            self.restore_layout_state,
        )

    def load_settings(self):

        self.max_images = (
            self.settings.value(
                "max_images",
                1,
                type=int,
            )
        )

        self.use_angle_cls = (
            self.settings.value(
                "use_angle_cls",
                True,
                type=bool,
            )
        )

        self.show_confidence = (
            self.settings.value(
                "show_confidence",
                False,
                type=bool,
            )
        )

        self.export_format = (
            self.settings.value(
                "export_format",
                "TXT",
                type=str,
            )
        )

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

        main_layout.setSpacing(
            8
        )

        # =========================
        # 顶部标题区域
        # =========================

        title_layout = QHBoxLayout()

        title_box = QVBoxLayout()

        title = QLabel(
            APP_NAME
        )

        title.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            """
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

        title_box.addWidget(
            title
        )

        title_box.addWidget(
            subtitle
        )

        title_layout.addLayout(
            title_box
        )

        title_layout.addStretch()

        self.settings_button = QPushButton(
            "设置 ⚙"
        )

        title_layout.addWidget(
            self.settings_button
        )

        main_layout.addLayout(
            title_layout
        )

        # =========================
        # 主工作区 / 底部控制区
        # 可上下拖动的垂直分隔器
        # =========================

        self.vertical_splitter = QSplitter(
            Qt.Orientation.Vertical
        )

        self.vertical_splitter.setChildrenCollapsible(
            False
        )

        main_layout.addWidget(
            self.vertical_splitter,
            1,
        )

        # =========================
        # 上半部分：主 OCR 工作区
        # =========================

        work_area = QWidget()

        work_layout = QVBoxLayout(
            work_area
        )

        work_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.main_splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        self.main_splitter.setChildrenCollapsible(
            False
        )

        self.task_table = QTableWidget()

        self.task_table.setColumnCount(
            3
        )

        self.task_table.setHorizontalHeaderLabels(
            [
                "序号",
                "文件名",
                "状态",
            ]
        )

        self.task_table.verticalHeader().setVisible(
            False
        )

        self.task_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior
            .SelectRows
        )

        self.task_table.setEditTriggers(
            QTableWidget.EditTrigger
            .NoEditTriggers
        )

        self.task_table.setHorizontalScrollMode(
            QTableWidget.ScrollMode
            .ScrollPerPixel
        )

        self.task_table.setVerticalScrollMode(
            QTableWidget.ScrollMode
            .ScrollPerPixel
        )

        self.task_table.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.ResizeMode
            .ResizeToContents,
        )

        self.task_table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.ResizeMode
            .Interactive,
        )

        self.task_table.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeMode
            .ResizeToContents,
        )

        self.task_table.setColumnWidth(
            1,
            220,
        )

        self.preview = ImagePreview()

        self.preview.fileDropped.connect(
            self.handle_dropped_file
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

        self.main_splitter.addWidget(
            self.task_table
        )

        self.main_splitter.addWidget(
            self.preview
        )

        self.main_splitter.addWidget(
            self.result_text
        )

        work_layout.addWidget(
            self.main_splitter
        )

        # =========================
        # 下半部分：控制区域
        # =========================

        control_area = QWidget()

        control_layout = QVBoxLayout(
            control_area
        )

        control_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        control_layout.setSpacing(
            8
        )

        self.progress = QProgressBar()

        self.progress.setVisible(
            False
        )

        control_layout.addWidget(
            self.progress
        )

        self.status_label = QLabel(
            "状态：就绪"
        )

        self.status_label.setStyleSheet(
            """
            color: #888888;
            """
        )

        control_layout.addWidget(
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
            "保存"
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

        control_layout.addLayout(
            button_layout
        )

        # =========================
        # 加入垂直 Splitter
        # =========================

        self.vertical_splitter.addWidget(
            work_area
        )

        self.vertical_splitter.addWidget(
            control_area
        )

        self.vertical_splitter.setStretchFactor(
            0,
            1,
        )

        self.vertical_splitter.setStretchFactor(
            1,
            0,
        )

        self.vertical_splitter.setSizes(
            [
                600,
                120,
            ]
        )

        self.vertical_splitter.splitterMoved.connect(
            self.save_layout_state
        )

        # =========================
        # 信号连接
        # =========================

        self.settings_button.clicked.connect(
            self.open_settings
        )

        self.select_button.clicked.connect(
            self.select_images
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

        self.task_table.itemSelectionChanged.connect(
            self.task_selection_changed
        )

    def open_settings(self):

        dialog = SettingsDialog(
            self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:

            old_max_images = (
                self.max_images
            )

            self.load_settings()

            if (
                self.max_images
                != old_max_images
            ):

                if (
                    len(self.image_paths)
                    > self.max_images
                ):

                    QMessageBox.information(
                        self,
                        "任务数量调整",
                        "当前图片数量超过新的限制，"
                        "任务已自动清空。",
                    )

                    self.clear_all()

            self.update_mode_layout()

    def update_mode_layout(self):

        batch_mode = (
            self.max_images > 1
        )

        self.task_table.setVisible(
            batch_mode
        )

        if batch_mode:

            self.main_splitter.setSizes(
                [
                    280,
                    500,
                    500,
                ]
            )

        else:

            self.main_splitter.setSizes(
                [
                    0,
                    600,
                    600,
                ]
            )

    def save_layout_state(
        self,
        pos,
        index,
    ):

        self.settings.setValue(
            "vertical_splitter_state",
            self.vertical_splitter.saveState(),
        )

        self.settings.sync()

    def restore_layout_state(self):

        state = self.settings.value(
            "vertical_splitter_state",
            None,
        )

        if state:

            restored = (
                self.vertical_splitter.restoreState(
                    state
                )
            )

            if restored:

                return

        self.vertical_splitter.setSizes(
            [
                600,
                120,
            ]
        )

    def select_images(self):

        if self.max_images == 1:

            file_path, _ = (
                QFileDialog.getOpenFileName(
                    self,
                    "选择图片",
                    "",
                    "Images "
                    "(*.png *.jpg *.jpeg "
                    "*.bmp *.webp "
                    "*.tiff *.tif)",
                )
            )

            if file_path:

                self.add_images(
                    [file_path]
                )

        else:

            file_paths, _ = (
                QFileDialog.getOpenFileNames(
                    self,
                    "选择图片",
                    "",
                    "Images "
                    "(*.png *.jpg *.jpeg "
                    "*.bmp *.webp "
                    "*.tiff *.tif)",
                )
            )

            if file_paths:

                self.add_images(
                    file_paths
                )

    def handle_dropped_file(
        self,
        file_path,
    ):

        self.add_images(
            [file_path]
        )

    def add_images(
        self,
        file_paths,
    ):

        valid_paths = []

        for file_path in file_paths:

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
                    f"不支持的图片格式："
                    f"{path.name}",
                )

                continue

            valid_paths.append(
                str(path)
            )

        if not valid_paths:

            return

        if self.max_images == 1:

            valid_paths = [
                valid_paths[0]
            ]

            self.image_paths = (
                valid_paths
            )

            self.ocr_results.clear()

            self.task_status.clear()

            self.current_index = 0

            self.preview.load_image(
                valid_paths[0]
            )

            self.result_text.clear()

            self.status_label.setText(
                f"状态：已加载 "
                f"{Path(valid_paths[0]).name}"
            )

        else:

            if (
                len(valid_paths)
                > self.max_images
            ):

                QMessageBox.warning(
                    self,
                    "图片数量超过限制",
                    f"一次最多添加 "
                    f"{self.max_images} 张图片。\n\n"
                    f"你选择了 "
                    f"{len(valid_paths)} 张图片。",
                )

                return

            self.image_paths = (
                valid_paths
            )

            self.ocr_results.clear()

            self.task_status.clear()

            for index in range(
                len(self.image_paths)
            ):

                self.task_status[index] = (
                    "等待"
                )

            self.populate_task_table()

            if self.image_paths:

                self.current_index = 0

                self.task_table.selectRow(
                    0
                )

                self.show_task(
                    0
                )

            self.status_label.setText(
                f"状态：已添加 "
                f"{len(self.image_paths)} 张图片"
            )

        self.ocr_button.setEnabled(
            bool(
                self.image_paths
            )
        )

    def populate_task_table(self):

        self.task_table.setRowCount(
            len(self.image_paths)
        )

        for index, image_path in enumerate(
            self.image_paths
        ):

            number_item = QTableWidgetItem(
                str(index + 1)
            )

            filename_item = QTableWidgetItem(
                Path(image_path).name
            )

            status_item = QTableWidgetItem(
                self.task_status.get(
                    index,
                    "等待",
                )
            )

            self.task_table.setItem(
                index,
                0,
                number_item,
            )

            self.task_table.setItem(
                index,
                1,
                filename_item,
            )

            self.task_table.setItem(
                index,
                2,
                status_item,
            )

    def update_task_status(
        self,
        index,
        status,
    ):

        self.task_status[index] = (
            status
        )

        item = (
            self.task_table.item(
                index,
                2,
            )
        )

        if item:

            item.setText(
                status
            )

    def task_selection_changed(self):

        selected_rows = (
            self.task_table
            .selectionModel()
            .selectedRows()
        )

        if not selected_rows:

            return

        index = (
            selected_rows[0].row()
        )

        self.show_task(
            index
        )

    def show_task(
        self,
        index,
    ):

        if (
            index < 0
            or index >= len(
                self.image_paths
            )
        ):

            return

        self.current_index = (
            index
        )

        image_path = (
            self.image_paths[index]
        )

        self.preview.load_image(
            image_path
        )

        text = (
            self.ocr_results.get(
                index,
                "",
            )
        )

        self.result_text.setPlainText(
            text
        )

    def start_ocr(self):

        if not self.image_paths:

            QMessageBox.warning(
                self,
                "提示",
                "请先选择图片。",
            )

            return

        self.set_busy(
            True
        )

        self.progress.setVisible(
            True
        )

        self.progress.setRange(
            0,
            len(
                self.image_paths
            ),
        )

        self.progress.setValue(
            0
        )

        self.worker = OCRWorker(
            self.image_paths,
            self.use_angle_cls,
            self.show_confidence,
        )

        self.worker.status.connect(
            self.set_status
        )

        self.worker.progress.connect(
            self.update_progress
        )

        self.worker.task_started.connect(
            self.ocr_task_started
        )

        self.worker.task_finished.connect(
            self.ocr_task_finished
        )

        self.worker.task_error.connect(
            self.ocr_task_error
        )

        self.worker.finished_all.connect(
            self.ocr_finished_all
        )

        self.worker.start()

    def set_status(
        self,
        message,
    ):

        self.status_label.setText(
            f"状态：{message}"
        )

    def update_progress(
        self,
        current,
        total,
    ):

        self.progress.setRange(
            0,
            total,
        )

        self.progress.setValue(
            current
        )

    def ocr_task_started(
        self,
        index,
    ):

        if self.max_images > 1:

            self.update_task_status(
                index,
                "识别中",
            )

    def ocr_task_finished(
        self,
        index,
        text,
    ):

        self.ocr_results[index] = (
            text
        )

        if self.max_images > 1:

            self.update_task_status(
                index,
                "已完成",
            )

        if (
            self.current_index
            == index
        ):

            self.result_text.setPlainText(
                text
            )

    def ocr_task_error(
        self,
        index,
        message,
    ):

        self.ocr_results[index] = (
            f"识别失败：\n{message}"
        )

        if self.max_images > 1:

            self.update_task_status(
                index,
                "失败",
            )

        if (
            self.current_index
            == index
        ):

            self.result_text.setPlainText(
                self.ocr_results[index]
            )

    def ocr_finished_all(self):

        self.progress.setValue(
            self.progress.maximum()
        )

        self.set_busy(
            False
        )

        self.status_label.setText(
            "状态：全部识别完成"
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
            "状态：文字已复制到剪贴板"
        )

    def save_text(self):

        if not self.ocr_results:

            QMessageBox.information(
                self,
                "提示",
                "没有可保存的 OCR 结果。",
            )

            return

        if (
            self.export_format
            == "Markdown"
        ):

            default_name = (
                "ocr_result.md"
            )

            file_filter = (
                "Markdown Files (*.md)"
            )

        else:

            default_name = (
                "ocr_result.txt"
            )

            file_filter = (
                "Text Files (*.txt)"
            )

        file_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "保存 OCR 结果",
                default_name,
                file_filter,
            )
        )

        if not file_path:

            return

        try:

            if (
                self.export_format
                == "Markdown"
            ):

                content = (
                    self.generate_markdown()
                )

            else:

                content = (
                    self.generate_txt()
                )

            with open(
                file_path,
                "w",
                encoding="utf-8",
            ) as f:

                f.write(
                    content
                )

            self.status_label.setText(
                f"状态：已保存 "
                f"{Path(file_path).name}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "保存失败",
                str(e),
            )

    def generate_txt(self):

        contents = []

        for index, image_path in enumerate(
            self.image_paths
        ):

            filename = (
                Path(image_path).name
            )

            text = (
                self.ocr_results.get(
                    index,
                    "",
                )
            )

            if not text:

                text = (
                    "未识别"
                )

            contents.append(
                filename
            )

            contents.append(
                "=" * 50
            )

            contents.append(
                text
            )

            contents.append(
                ""
            )

        return "\n".join(
            contents
        )

    def generate_markdown(self):

        contents = [
            "# PaddleOCR Offline 识别结果",
            "",
        ]

        for index, image_path in enumerate(
            self.image_paths
        ):

            filename = (
                Path(image_path).name
            )

            text = (
                self.ocr_results.get(
                    index,
                    "",
                )
            )

            if not text:

                text = (
                    "未识别"
                )

            contents.append(
                f"## {filename}"
            )

            contents.append(
                ""
            )

            contents.append(
                text
            )

            contents.append(
                ""
            )

            contents.append(
                "---"
            )

            contents.append(
                ""
            )

        return "\n".join(
            contents
        )

    def clear_all(self):

        self.image_paths.clear()

        self.ocr_results.clear()

        self.task_status.clear()

        self.current_index = None

        self.task_table.setRowCount(
            0
        )

        self.preview.clear_preview()

        self.result_text.clear()

        self.status_label.setText(
            "状态：就绪"
        )

        self.progress.setVisible(
            False
        )

        self.progress.setValue(
            0
        )

        self.ocr_button.setEnabled(
            False
        )

    def set_busy(
        self,
        busy,
    ):

        self.settings_button.setEnabled(
            not busy
        )

        self.select_button.setEnabled(
            not busy
        )

        self.ocr_button.setEnabled(
            (
                not busy
                and bool(
                    self.image_paths
                )
            )
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

        if not busy:

            self.progress.setVisible(
                False
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