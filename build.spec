# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

paddleocr_datas, paddleocr_binaries, paddleocr_hiddenimports = (
collect_all("paddleocr")
)

paddle_datas, paddle_binaries, paddle_hiddenimports = (
collect_all("paddle")
)

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
```

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

```
name="PaddleOCR-Offline",

debug=False,
bootloader_ignore_signals=False,
strip=False,
upx=False,
console=False,
```

)

coll = COLLECT(
exe,
a.binaries,
a.zipfiles,
a.datas,

```
strip=False,
upx=False,

name="PaddleOCR-Offline",
```

)
