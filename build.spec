from PyInstaller.utils.hooks import collect_all, copy_metadata


paddleocr_datas, paddleocr_binaries, paddleocr_hiddenimports = collect_all(
    "paddleocr"
)

paddle_datas, paddle_binaries, paddle_hiddenimports = collect_all(
    "paddle"
)


imageio_metadata = copy_metadata("imageio")

imgaug_metadata = copy_metadata("imgaug")


# =========================
# 项目资源文件
# =========================

project_datas = [
    ("models", "models"),
    ("icon.ico", "."),
]


a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=(
        paddleocr_binaries
        + paddle_binaries
    ),
    datas=(
        paddleocr_datas
        + paddle_datas
        + imageio_metadata
        + imgaug_metadata
        + project_datas
    ),
    hiddenimports=(
        paddleocr_hiddenimports
        + paddle_hiddenimports
        + [
            "paddleocr",
            "paddle",
            "cv2",
            "numpy",
        ]
    ),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)


pyz = PYZ(
    a.pure
)


exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="PaddleOCR-Offline",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,

    # Windows EXE 图标
    icon="icon.ico",
)


coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name="PaddleOCR-Offline",
)