# PaddleOCR Offline

[English](README.md) | 简体中文

一个基于 PaddleOCR 的 Windows 离线 OCR 桌面应用。

本项目将 PaddleOCR、本地 OCR 模型和 PySide6 图形界面整合为一个可以直接运行的 Windows 桌面程序，无需最终用户单独安装 Python、PaddlePaddle 或 PaddleOCR。

## 功能

### OCR

* Windows 桌面 OCR
* 中文 OCR
* CPU 推理
* 完全本地运行
* 支持离线 OCR 识别
* 内置本地 OCR 模型
* OCR 识别过程中无需联网
* 可选文字方向分类
* 可选保留 OCR 识别置信度

### 图片支持

支持以下图片格式：

* PNG
* JPG
* JPEG
* BMP
* WEBP
* TIFF
* TIF

### 单张与批量 OCR

程序支持单张图片 OCR 和批量图片 OCR。

批量模式通过设置窗口进行控制。

* 最少添加图片数量：1 张
* 最多添加图片数量：100 张
* 默认值：1 张

当一次最多添加图片数量设置为 `1` 时，程序处于单张 OCR 模式。

当一次最多添加图片数量设置为大于 `1` 的数值时，程序启用批量图片添加和批量 OCR 功能。

### 图片预览

程序提供：

* 图片预览
* 拖拽添加图片
* 自动缩放图片
* 图片预览区域随窗口大小自适应

### 批量任务列表

当启用批量模式时，主界面左侧会显示图片任务列表。

任务列表支持：

* 显示多张图片任务
* 上下滚动
* 左右滚动
* 查看较长的图片文件名
* 选择单个图片任务
* 切换当前图片预览

### OCR 结果

OCR 结果区域位于主界面右侧。

支持：

* 查看 OCR 识别结果
* 复制识别文字
* 保存 OCR 结果
* 批量 OCR 结果输出

### 导出格式

默认导出格式可以在设置窗口中进行配置。

目前支持：

* TXT
* Markdown

### 设置

程序提供统一的设置窗口。

当前设置包括：

#### 批量处理

* 一次最多添加图片数量
* 可调整范围：1 至 100
* 默认值：1

#### OCR

* 启用或关闭方向分类
* 启用或关闭 OCR 识别置信度

#### 输出

* 默认导出格式
* TXT
* Markdown

修改设置后点击 `确认` 才会保存并应用设置。

点击 `取消` 则放弃本次修改。

## 界面布局

### 单张图片模式

当一次最多添加图片数量设置为 `1` 时，主界面为：

```text
┌──────────────────────────────────────────────┐
│ PaddleOCR Offline                    [设置 ⚙] │
│ Windows · CPU · 完全本地离线 OCR             │
├──────────────────────┬───────────────────────┤
│                      │                       │
│      图片预览        │       OCR 结果        │
│                      │                       │
│   将图片拖到这里     │                       │
│   或点击选择图片     │                       │
│                      │                       │
├──────────────────────┴───────────────────────┤
│ 状态：就绪                                  │
│                                              │
│ [选择图片] [开始识别] [复制文字] [保存] [清空] │
└──────────────────────────────────────────────┘
```

### 批量图片模式

当一次最多添加图片数量设置为大于 `1` 时，主界面会显示任务列表。

```text
┌────────────────────────────────────────────────────┐
│ PaddleOCR Offline                          [设置 ⚙] │
│ Windows · CPU · 完全本地离线 OCR                    │
├──────────────┬────────────────┬────────────────────┤
│              │                │                    │
│   任务列表   │   图片预览     │      OCR 结果      │
│              │                │                    │
│   image1.png │                │                    │
│   image2.jpg │                │                    │
│   image3.png │                │                    │
│              │                │                    │
├──────────────┴────────────────┴────────────────────┤
│ 状态：就绪                                          │
│                                                    │
│ [选择图片] [开始识别] [复制文字] [保存] [清空]      │
└────────────────────────────────────────────────────┘
```

任务列表支持上下滚动和左右滚动，避免因为图片数量较多或文件名较长而无法完整查看任务内容。

## 下载

请前往 GitHub Releases 下载已经打包好的 Windows 版本。

发布包：

```text
PaddleOCR-Offline-Windows.zip
```

解压 ZIP 文件后运行：

```text
PaddleOCR-Offline.exe
```

## 使用方法

### 单张图片 OCR

1. 下载 `PaddleOCR-Offline-Windows.zip`
2. 解压 ZIP 文件
3. 运行 `PaddleOCR-Offline.exe`
4. 点击「选择图片」，或者直接将图片拖入程序
5. 点击「开始识别」
6. 在 OCR 结果区域查看识别结果
7. 可以复制或保存识别出的文字

### 批量图片 OCR

1. 点击主界面的「设置」
2. 将「一次最多添加图片」设置为大于 `1` 的数值
3. 点击「确认」
4. 返回主界面
5. 点击「选择图片」
6. 一次选择多张图片
7. 点击「开始识别」
8. 查看任务列表和 OCR 结果
9. OCR 完成后导出识别结果

一次可以选择的最大图片数量由设置中的数值决定。

可设置范围：

```text
1 - 100
```

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

本项目使用 GitHub Actions 在 Windows Runner 上进行构建。

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
        ├── 安装应用依赖
        ├── PyInstaller 打包
        ├── 复制本地 OCR 模型
        └── 生成 Windows ZIP
        │
        ▼
PaddleOCR-Offline-Windows.zip
```

## Python 依赖

当前主要依赖版本：

```text
paddlepaddle==2.6.2
paddleocr==2.9.1
PySide6==6.7.3
pyinstaller==6.11.1
```

PaddleOCR 及其相关组件可能会自动安装其他依赖。

## 离线运行

本项目的目标是让最终用户在安装完成后无需访问互联网即可进行 OCR。

OCR 模型在 GitHub Actions 构建阶段下载，并复制到最终发行包中。

最终应用程序包含本地 OCR 模型：

```text
models/
├── det/
├── rec/
└── cls/
```

程序运行时直接加载这些本地模型。

因此，最终用户无需再次下载 OCR 模型。

在下载并解压完整应用程序发行包后，可以在没有互联网连接的情况下进行 OCR 识别。

## 项目许可证

本项目自行编写的源代码采用：

**MIT License**

完整许可证内容请参见仓库根目录的：

[`LICENSE`](LICENSE)

MIT License 仅适用于本项目作者拥有并授权的原创项目代码及相关原创内容。

本项目使用了多个第三方开源组件。

第三方组件不因本项目采用 MIT License 而自动变更其原有许可证。

## 第三方组件与许可证

### PaddleOCR

本项目使用 PaddleOCR 作为 OCR 引擎。

PaddleOCR 项目采用：

**Apache License 2.0**

PaddleOCR 官方项目：

[PaddleOCR GitHub 仓库](https://github.com/PaddlePaddle/PaddleOCR?utm_source=chatgpt.com)

PaddleOCR 的许可证及版权声明适用于 PaddleOCR 本身及其相关代码。

### PaddlePaddle

本项目使用 PaddlePaddle 作为深度学习推理框架。

PaddlePaddle 采用：

**Apache License 2.0**

PaddlePaddle 官方项目：

[PaddlePaddle GitHub 仓库](https://github.com/PaddlePaddle/Paddle?utm_source=chatgpt.com)

PaddlePaddle 的许可证及版权声明适用于 PaddlePaddle 本身。

### PySide6 / Qt for Python

本项目使用 PySide6 构建 Windows 图形界面。

Qt for Python / PySide6 的开源版本涉及：

* GNU Lesser General Public License v3 (LGPLv3)
* GNU General Public License v3 (GPLv3)

Qt 也提供商业许可证。

具体许可证以及第三方组件说明请以 Qt 官方许可证页面为准：

[Qt for Python 官方许可证说明](https://doc.qt.io/qtforpython-6/licensing.html?utm_source=chatgpt.com)

如果重新分发本项目的 Windows 可执行文件或其他发行包，请注意其中包含的 Qt、PySide6 及相关组件所适用的许可证及相应义务。

### PyInstaller

本项目使用 PyInstaller 将 Python 应用程序打包为 Windows 可执行程序。

PyInstaller 及其相关组件分别遵循其各自适用的开源许可证。

项目地址：

[PyInstaller GitHub 仓库](https://github.com/pyinstaller/pyinstaller?utm_source=chatgpt.com)

### OCR 模型

本项目的 Windows 发布包包含通过 PaddleOCR 官方模型分发地址获取的 OCR 推理模型，包括：

* PP-OCRv4 中文文本检测模型
* PP-OCRv4 中文文本识别模型
* PaddleOCR mobile 方向分类模型

这些 OCR 模型不是本项目原创内容。

模型及相关文件应遵循其原始发布项目、模型提供方及分发来源所适用的许可证、版权声明和其他使用条款。

本项目不会将第三方 OCR 模型重新声明为本项目原创内容。

## 第三方许可证说明

本项目是一个对多个开源组件进行集成和打包的应用程序。

本项目采用的 MIT License：

**不取代、不修改、不扩大第三方组件原有的许可证授权范围。**

对于本项目发行包中包含或使用的第三方软件、运行库、OCR 模型或其他材料，应分别遵守其各自适用的许可证及版权要求。

如果你重新分发、修改或商业使用本项目，请同时检查相关第三方组件的许可证要求。

## 免责声明

本软件按“现状”提供，不提供任何明示或暗示的保证。

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

用户选择的图片默认直接在本地计算机上进行处理。

OCR 识别过程不要求将图片上传到本项目作者提供的服务器。

本项目本身不提供云端 OCR 服务。

但是，用户使用的操作系统、网络环境、杀毒软件或其他第三方软件可能具有独立的数据处理行为。

这些行为不属于本项目控制范围。

## 项目状态

当前版本：

**v1.1.0**

v1.1.0 在最初的单张图片 OCR 功能基础上，增加了批量图片 OCR、可配置的批量图片数量、统一设置窗口、可滚动任务列表、可选 OCR 设置以及 TXT / Markdown 导出等功能。

## Development Note

This project was developed with assistance from ChatGPT.

## License

Copyright (c) 2026 Jekeer

This project is licensed under the MIT License.

See the [`LICENSE`](LICENSE) file for details.

Third-party components included in or used by this project are subject to their respective licenses.
