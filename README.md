# PaddleOCR Offline

English | [简体中文](README_zh.md)

A Windows offline OCR desktop application based on PaddleOCR.

This project integrates PaddleOCR, local OCR models, and a PySide6 graphical interface into a ready-to-run Windows desktop application.

End users do not need to install Python, PaddlePaddle, or PaddleOCR separately.

## Features

### OCR

* Windows desktop OCR application
* Chinese OCR
* CPU inference
* Fully local processing
* Offline OCR recognition
* Built-in local OCR models
* No internet connection required during OCR recognition
* Optional text direction classification
* Optional OCR confidence information

### Image Support

Supported image formats:

* PNG
* JPG
* JPEG
* BMP
* WEBP
* TIFF
* TIF

### Single and Batch OCR

The application supports both single-image and batch-image OCR.

The batch mode is controlled through the settings window.

* Minimum image count: 1
* Maximum image count: 100
* Default value: 1

When the maximum image count is set to `1`, the application works in single-image mode.

When the maximum image count is greater than `1`, batch image selection is enabled.

### Image Preview

The application provides:

* Image preview
* Drag and drop image loading
* Automatic image scaling
* Preview area that adapts to the application window

### Batch Task List

When batch mode is enabled, a task list is displayed on the left side of the main interface.

The task list supports:

* Multiple image tasks
* Vertical scrolling
* Horizontal scrolling
* Viewing long file names
* Selecting individual images
* Switching the image preview

### OCR Results

The OCR result panel is displayed on the right side of the main interface.

The application supports:

* Viewing OCR results
* Copying recognized text
* Saving OCR results
* Batch OCR result output

### Export Formats

The default export format can be configured in the settings window.

Supported formats:

* TXT
* Markdown

### Settings

The application provides a unified settings window.

Current settings include:

#### Batch Processing

* Maximum number of images that can be added at one time
* Adjustable range: 1 to 100
* Default value: 1

#### OCR

* Enable or disable direction classification
* Enable or disable OCR confidence information

#### Output

* Default export format
* TXT
* Markdown

Settings are applied after clicking `Confirm`.

The user can click `Cancel` to discard changes.

## Interface Layout

### Single Image Mode

When the maximum image count is set to `1`, the main interface displays:

```text
┌──────────────────────────────────────────────┐
│ PaddleOCR Offline                    [⚙]   │
│ Windows · CPU · Fully Offline OCR           │
├──────────────────────┬───────────────────────┤
│                      │                       │
│    Image Preview     │      OCR Result       │
│                      │                       │
│  Drag an image here  │                       │
│  or click Select     │                       │
│                      │                       │
├──────────────────────┴───────────────────────┤
│ Status: Ready                                │
│                                              │
│ [Select Image] [Start OCR] [Copy] [Save]     │
│                                      [Clear] │
└──────────────────────────────────────────────┘
```

### Batch Image Mode

When the maximum image count is greater than `1`, the task list is displayed.

```text
┌────────────────────────────────────────────────────┐
│ PaddleOCR Offline                          [⚙]    │
│ Windows · CPU · Fully Offline OCR                 │
├──────────────┬────────────────┬────────────────────┤
│              │                │                    │
│  Task List   │ Image Preview  │     OCR Result     │
│              │                │                    │
│  image1.png  │                │                    │
│  image2.jpg  │                │                    │
│  image3.png  │                │                    │
│              │                │                    │
├──────────────┴────────────────┴────────────────────┤
│ Status: Ready                                      │
│                                                    │
│ [Select Images] [Start OCR] [Copy] [Save] [Clear] │
└────────────────────────────────────────────────────┘
```

The task list supports vertical and horizontal scrolling to avoid long lists or long file names being truncated.

## Download

Please download the packaged Windows version from GitHub Releases.

Release package:

```text
PaddleOCR-Offline-Windows.zip
```

After extracting the ZIP file, run:

```text
PaddleOCR-Offline.exe
```

## Usage

### Single Image OCR

1. Download `PaddleOCR-Offline-Windows.zip`
2. Extract the ZIP file
3. Run `PaddleOCR-Offline.exe`
4. Click `Select Image`, or drag an image into the application
5. Click `Start OCR`
6. View the OCR result
7. Copy or save the recognized text

### Batch Image OCR

1. Click the `Settings` button
2. Set the maximum number of images to a value greater than `1`
3. Click `Confirm`
4. Return to the main interface
5. Click `Select Images`
6. Select multiple images
7. Click `Start OCR`
8. View individual tasks and OCR results
9. Export the OCR results when processing is complete

The maximum number of images selected in one operation is limited by the value configured in Settings.

The supported range is:

```text
1 - 100
```

## System Requirements

* Windows 10 or Windows 11
* 64-bit Windows
* CPU supported
* No dedicated GPU required
* No Python installation required
* No separate PaddleOCR installation required

## Technology Stack

This project primarily uses:

* Python
* PySide6
* PaddleOCR
* PaddlePaddle
* PyInstaller
* GitHub Actions

## Build

The project uses GitHub Actions to build the Windows application on a Windows runner.

The main build process is:

```text
GitHub Repository
        │
        ▼
GitHub Actions
        │
        ├── Install Python
        ├── Install PaddlePaddle
        ├── Install PaddleOCR
        ├── Download OCR models
        ├── Install application dependencies
        ├── Build with PyInstaller
        ├── Copy local OCR models
        └── Create Windows ZIP package
        │
        ▼
PaddleOCR-Offline-Windows.zip
```

## Python Dependencies

The project currently uses the following primary dependencies:

```text
paddlepaddle==2.6.2
paddleocr==2.9.1
PySide6==6.7.3
pyinstaller==6.11.1
```

Additional dependencies may be installed automatically through PaddleOCR and related packages.

## Offline Operation

The goal of this project is to allow end users to perform OCR without requiring an internet connection.

OCR models are downloaded during the GitHub Actions build process and copied into the final distribution package.

The final application package contains local OCR models in:

```text
models/
├── det/
├── rec/
└── cls/
```

The application directly loads these local models during runtime.

Therefore, end users do not need to download OCR models again.

After the application package has been downloaded and extracted, OCR recognition can be performed locally without an internet connection.

## Project License

The original source code created specifically for this project is licensed under the:

**MIT License**

The complete license text is available in the repository root:

[`LICENSE`](LICENSE)

The MIT License applies only to the original project code and other original content owned and licensed by the project copyright holder.

This project uses multiple third-party open-source components.

The licenses of third-party components are not changed by the MIT License used for this project.

## Third-Party Components and Licenses

### PaddleOCR

This project uses PaddleOCR as its OCR engine.

PaddleOCR is licensed under:

**Apache License 2.0**

Official project:

[PaddleOCR GitHub repository](https://github.com/PaddlePaddle/PaddleOCR?utm_source=chatgpt.com)

The PaddleOCR license and copyright notices apply to PaddleOCR itself and its related code.

### PaddlePaddle

This project uses PaddlePaddle as the deep learning inference framework.

PaddlePaddle is licensed under:

**Apache License 2.0**

Official project:

[PaddlePaddle GitHub repository](https://github.com/PaddlePaddle/Paddle?utm_source=chatgpt.com)

The PaddlePaddle license and copyright notices apply to PaddlePaddle itself.

### PySide6 / Qt for Python

This project uses PySide6 to build the Windows graphical user interface.

The open-source version of Qt for Python / PySide6 involves licenses including:

* GNU Lesser General Public License v3 (LGPLv3)
* GNU General Public License v3 (GPLv3)

Qt also provides commercial licensing options.

For detailed licensing information, please refer to the official Qt for Python licensing documentation:

[Qt for Python licensing documentation](https://doc.qt.io/qtforpython-6/licensing.html?utm_source=chatgpt.com)

If you redistribute the Windows executable or other packaged distributions of this project, please review and comply with the applicable license requirements of Qt, PySide6, and related components.

### PyInstaller

This project uses PyInstaller to package the Python application into a Windows executable.

PyInstaller and its related components are subject to their respective open-source licenses.

Official project:

[PyInstaller GitHub repository](https://github.com/pyinstaller/pyinstaller?utm_source=chatgpt.com)

### OCR Models

The Windows release package includes OCR inference models obtained from official PaddleOCR model distribution sources.

These include:

* PP-OCRv4 Chinese text detection model
* PP-OCRv4 Chinese text recognition model
* PaddleOCR mobile text direction classification model

These OCR models are not original content created by this project.

The models and related files remain subject to the licenses, copyright notices, and terms of their original publishers and distribution sources.

This project does not claim third-party OCR models as original project content.

## Third-Party License Notice

This project integrates and packages multiple open-source components.

The MIT License used for this project:

**does not replace, modify, or expand the original license terms of third-party components.**

Software libraries, runtime components, OCR models, and other third-party materials included in or used by the project remain subject to their respective licenses.

If you redistribute, modify, or commercially use this project, please review the license requirements of all applicable third-party components.

## Disclaimer

This software is provided "as is", without warranties of any kind, either express or implied.

The project author does not guarantee that:

* OCR recognition results will always be accurate
* The software will always operate correctly
* The software will work with every image or use case
* The software will be free from errors, crashes, or other issues
* OCR results are suitable for medical, legal, financial, or other high-risk decisions

OCR systems may produce recognition errors.

Users should manually verify OCR results when accuracy is important.

To the maximum extent permitted by applicable law, the project author shall not be liable for direct or indirect losses resulting from the use of, or inability to use, this software.

## Privacy

This project is designed as a local OCR application.

Images selected by the user are processed locally on the user's computer.

The OCR recognition process does not require uploading images to a server operated by the project author.

This project does not provide a cloud OCR service.

However, the user's operating system, network environment, antivirus software, or other third-party software may have independent data processing behavior.

Such behavior is outside the control of this project.

## Project Status

Current version:

**v1.1.0**

Version 1.1.0 expands the initial single-image OCR application with batch OCR support, configurable batch image limits, a unified settings window, a scrollable task list, optional OCR settings, and TXT / Markdown export options.

## Development Note

This project was developed with assistance from ChatGPT.

## License

Copyright (c) 2026 Jekeer

This project is licensed under the MIT License.

See the [`LICENSE`](LICENSE) file for details.

Third-party components included in or used by this project are subject to their respective licenses.
