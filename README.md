# PaddleOCR Offline

一个基于 PaddleOCR 的 Windows 离线 OCR 桌面应用。

本项目将 PaddleOCR、OCR 模型和 PySide6 图形界面整合为一个可以直接运行的 Windows 桌面程序，无需用户单独安装 Python、PaddlePaddle 或 PaddleOCR。

## 功能

* Windows 桌面 OCR
* 中文 OCR
* CPU 推理
* 完全本地运行
* 支持 PNG、JPG、JPEG、BMP、WEBP、TIFF
* 支持拖拽图片
* 支持图片预览
* OCR 文字复制
* OCR 结果保存为 TXT
* 内置本地 OCR 模型
* 无需联网即可进行 OCR 识别

## 下载

请前往 GitHub Releases 下载已经打包好的 Windows 版本。

下载：

`PaddleOCR-Offline-Windows.zip`

解压后运行：

`PaddleOCR-Offline.exe`

## 使用方法

1. 下载 `PaddleOCR-Offline-Windows.zip`
2. 解压 ZIP 文件
3. 运行 `PaddleOCR-Offline.exe`
4. 点击「选择图片」，或者直接将图片拖入程序
5. 点击「开始识别」
6. 在右侧查看 OCR 结果
7. 可以复制识别结果或保存为 TXT 文件

## 系统要求

* Windows 10 / Windows 11
* 64 位 Windows
* CPU 即可运行
* 无需独立 GPU
* 无需安装 Python
* 无需单独安装 PaddleOCR

## 技术栈

本项目主要使用：

* Python
* PySide6
* PaddleOCR
* PaddlePaddle
* PyInstaller
* GitHub Actions

## 构建

本项目使用 GitHub Actions 在 Windows runner 上进行构建。

主要构建流程：

```text
GitHub Repository
        │
        ▼
GitHub Actions
        │
        ├── 安装 Python
        ├── 安装 PaddlePaddle
        ├── 安装 PaddleOCR
        ├── 下载 OCR 模型
        ├── PyInstaller 打包
        └── 生成 Windows ZIP
        │
        ▼
PaddleOCR-Offline-Windows.zip
```

### Python 依赖

当前主要依赖版本：

```text
paddlepaddle==2.6.2
paddleocr==2.9.1
PySide6==6.7.3
pyinstaller==6.11.1
```

## 离线运行

本项目的目标是让最终用户在安装完成后无需访问互联网即可进行 OCR。

OCR 模型在构建阶段由 GitHub Actions 下载，并被复制到最终发行包中的：

```text
models/
├── det/
├── rec/
└── cls/
```

程序运行时直接使用本地模型。

因此，最终用户不需要再次下载 OCR 模型。

## 项目许可证

本项目自行编写的源代码采用：

**MIT License**

完整许可证内容请参见仓库根目录的 [`LICENSE`](LICENSE) 文件。

MIT License 仅适用于本项目作者所拥有并授权的项目代码及相关原创内容。

本项目使用了多个第三方开源组件。第三方组件不因本项目采用 MIT License 而自动变更其原有许可证。

## 第三方组件与许可证

### PaddleOCR

本项目使用 PaddleOCR 作为 OCR 引擎。

PaddleOCR 项目采用：

**Apache License 2.0**

PaddleOCR 官方项目：

https://github.com/PaddlePaddle/PaddleOCR

PaddleOCR 的许可证及版权声明适用于 PaddleOCR 本身及其相关代码。

### PaddlePaddle

本项目使用 PaddlePaddle 作为深度学习推理框架。

PaddlePaddle 采用：

**Apache License 2.0**

PaddlePaddle 官方项目：

https://github.com/PaddlePaddle/Paddle

PaddlePaddle 的许可证及版权声明适用于 PaddlePaddle 本身。

### PySide6 / Qt for Python

本项目使用 PySide6 构建 Windows 图形界面。

Qt for Python / PySide6 的开源版本涉及：

* GNU Lesser General Public License v3 (LGPLv3)
* GNU General Public License v3 (GPLv3)

Qt 也提供商业许可证。

具体许可证以及第三方组件说明请以 Qt 官方许可证页面为准：

https://doc.qt.io/qtforpython-6/licensing.html

如果重新分发本项目的 Windows 可执行文件，请注意其中包含的 Qt / PySide6 相关组件所适用的许可证及其相应义务。

### PyInstaller

本项目使用 PyInstaller 将 Python 应用程序打包为 Windows 可执行程序。

PyInstaller 及其包含的相关组件分别遵循其各自适用的开源许可证。

项目地址：

https://github.com/pyinstaller/pyinstaller

### OCR 模型

本项目的 Windows 发布包包含通过 PaddleOCR 官方模型下载地址获取的 OCR 推理模型，包括：

* PP-OCRv4 中文文本检测模型
* PP-OCRv4 中文文本识别模型
* PP-OCR mobile 方向分类模型

这些模型不是本项目原创内容。

模型及其相关文件应遵循其原始发布项目及模型提供方所适用的许可证、版权声明和其他使用条款。

本项目不会将第三方 OCR 模型重新声明为本项目原创内容。

## 第三方许可证说明

本项目是一个对多个开源组件进行集成和打包的应用程序。

本项目的 MIT License：

**不取代、不修改、不扩大第三方组件原有的许可证授权范围。**

对于本项目发行包中包含的第三方软件、运行库、模型或其他材料，应分别遵守其各自适用的许可证及版权要求。

如果你重新分发、修改或商业使用本项目，请同时检查相关第三方组件的许可证要求。

## 免责声明

本软件按「现状」提供，不提供任何明示或暗示的保证。

本项目作者不保证：

* OCR 识别结果始终准确
* 软件始终能够正常运行
* 软件适用于所有图片或使用场景
* 软件不会出现错误、崩溃或其他问题
* OCR 结果适用于医疗、法律、金融或其他高风险决策

由于 OCR 本身可能产生识别错误，用户应当根据实际使用场景对 OCR 结果进行人工核验。

对于因使用或无法使用本软件而产生的任何直接或间接损失，本项目作者在适用法律允许的最大范围内不承担责任。

## 隐私

本项目设计目标为本地 OCR。

用户选择的图片默认直接在本地计算机上进行处理，OCR 识别过程不要求将图片上传到本项目作者提供的服务器。

本项目本身不提供云端 OCR 服务。

但是，用户使用的操作系统、网络环境或其他第三方软件可能具有独立的数据处理行为，其隐私政策不属于本项目控制范围。

## 项目状态

当前版本：

**v1.0.0**

这是项目的首个可用版本。

## License

Copyright (c) 2026 Jekeer

This project is licensed under the MIT License.

See the `LICENSE` file for details.

Third-party components included in or used by this project are subject to their respective licenses.
