# ✂️ Anime Image Segmentation Tool (二次元图像部位分割工具)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![YOLO](https://img.shields.io/badge/Model-YOLO-green.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## 🚀 立即下载 / Download Now (Windows EXE)

> **不想配置 Python 环境？** 直接下载打包好的可执行文件，解压即用！
>
> **Don't want to set up Python?** Download the pre-packaged executable to run immediately!

本项目目前提供两个版本：
1. **Modern Edition (v3.0)**: 基于 PyWebView 的现代化界面，支持实时预览、更流畅的交互。
2. **Legacy Edition (TK)**: 基于 Tkinter 的经典版本，轻量级，兼容性强。

---

![img](https://github.com/wangyff-code/anime_Image_segmentation/blob/main/example/view.png)

### Modern Edition (v3.0)

- **全新 UI 设计**: 采用磨砂玻璃质感 (Glassmorphism) 界面，操作直观。
- **可视化参数**: 修改裁剪参数时，通过动画实时演示裁剪范围的变化。
- **实时预览**: 处理过程中实时展示识别到的部位预览图。
- **智能日志**: 底部状态栏实时显示处理进度和日志信息。

📥 **[点击下载 / Download via Google Drive](https://drive.google.com/file/d/19itiBcay0OSv6va1-d7c-Rhl4cqLi2FG/view?usp=drive_link)**

---

### Legacy Edition (TK)
- **纯原生体验**: 无需浏览器内核依赖，极低内存占用。
- **稳定可靠**: 经过长时间验证的经典逻辑。

📥 **[点击下载 / Download via Google Drive](https://drive.google.com/file/d/1RZLEMv5nYtTNErFrQc_938RjyhiMBUdl/view?usp=drive_link)**

---

> **一个基于 YOLO 的本地化 GUI 工具，用于批量识别并提取二次元角色的头部、躯干或腿部。**
>
> **A local GUI tool based on YOLO for batch recognition and extraction of anime character heads, torsos, or legs.**

专为数据集制作、素材收集和二次元图像处理设计。
Designed for dataset creation, material collection, and anime image processing.

![img](https://github.com/wangyff-code/anime_Image_segmentation/blob/main/example/20260103184447.png)

<details>
<summary>👀 Click to view more examples (点击查看更多示例)</summary>

![img](https://github.com/wangyff-code/anime_Image_segmentation/blob/main/example/20260103184456.png)
![img](https://github.com/wangyff-code/anime_Image_segmentation/blob/main/example/20260103184501.png)

</details>

---

## ✨ 主要功能 (Features)

*   **📺 可视化操作界面 / Visual Interface**
    *   基于 Tkinter 构建，无需编写代码，小白也能轻松上手。
    *   Built with Tkinter. No coding required, easy for beginners.

*   **🤖 强大的识别模型 / Powerful Model**
    *   内置 YOLO 逻辑，支持高精度的二次元角色部位检测。
    *   Built-in YOLO logic supporting high-precision detection of anime character parts.

*   **📂 批量处理 / Batch Processing**
    *   支持递归扫描文件夹，保持原有的目录结构输出，适合大规模数据集清洗。
    *   Supports recursive folder scanning and preserves the original directory structure. Ideal for large-scale dataset cleaning.

*   **📐 智能边缘扩充 / Smart Padding**
    *   支持自定义**顶部、底部、左右**的扩充比例（默认为 0.2），防止切头去尾，保留完整发型和肢体。
    *   Supports custom expansion ratios for **Top, Bottom, and Sides** (default 0.2) to prevent cropping off heads or limbs.

*   **🏷️ 纯净文件名逻辑 / Clean Filename Logic**
    *   **单人图 (Single)**：直接保存为 `文件名_后缀.jpg`（如 `image_head.jpg`）。
    *   **多人图 (Multiple)**：自动添加序号（如 `image_head_2.jpg`），避免文件覆盖。

*   **🎯 多部位支持 / Multi-Part Support**
    *   一键切换提取 **头部 (Head)**、**躯干 (Torso)** 或 **腿部 (Legs)**。
    *   One-click switching to extract specific parts.

*   **👀 实时预览 / Real-time Preview**
    *   处理过程中可实时查看裁剪出的图像预览。
    *   View cropped images instantly during processing.

---

## 🛠️ 源码安装与使用 (Installation from Source)

如果您想通过源码运行或进行修改，请参考以下步骤。如果您已下载 EXE，请跳过此步。
If you want to run from source code or modify it, follow these steps. If you downloaded the EXE, skip this section.

### 1. 环境准备 (Prerequisites)

确保你的电脑已安装 Python 3.8 或以上版本。
Ensure you have Python 3.8 or higher installed.

```bash
# 克隆项目
git clone https://github.com/wangyff-code/anime_Image_segmentation.git
cd anime_Image_segmentation

# 安装依赖
pip install -r requirements.txt
```

### 2. 模型准备 (Model Preparation)

本工具需要加载训练好的 YOLO 模型文件（`.pt`）。
This tool requires a pre-trained YOLO model file (`.pt`).

*   **Model Download Link (模型下载):** [HuggingFace - yolov11m_anime_Image_segmentation](https://huggingface.co/laowanglaowang/yolov11m_anime_Image_segmentation)
*   请确保将你的模型文件重命名为 **`best.pt`**。
*   将 `best.pt` 放入models。
*   *Please rename the downloaded model to **`best.pt`** and place it in the project models directory.*

### 3. 运行程序 (Run)

```bash
python app_modern.py
```

---

## ⚙️ 参数说明 (Settings)

在软件界面中，你可以调整以下参数以获得最佳效果：
Adjust the following parameters in the GUI for best results:

| 参数区域 (Area) | 选项 (Option) | 说明 (Description) |
| :--- | :--- | :--- |
| **提取设置**<br>Extraction | 头部 / 躯干 / 腿部<br>Head / Torso / Legs | 选择你要提取的目标部位。<br>Select the target part to extract. |
| **自定义后缀**<br>Suffix | 如 `_head`<br>e.g. `_head` | 输出文件的后缀名。支持自定义。<br>Output file suffix. Customizable (e.g., `_face`). |
| **边缘扩充**<br>Padding | 顶部 (Top) | 向上扩展裁剪框的比例。建议设为 `0.2` 以保留头顶发饰。<br>Expand upwards. `0.2` is recommended to keep hair accessories. |
| **边缘扩充**<br>Padding | 底部 (Bottom) | 向下扩展比例。提取头像时可适当减小。<br>Expand downwards. Can be reduced for headshots. |
| **边缘扩充**<br>Padding | 左右 (Side) | 向左右两侧扩展的比例。<br>Expand horizontally. |

---

## 📝 目录结构 (Directory Structure)

```text
anime_Image_segmentation/
├── assets/                 # 存放前端资源
│   └── index.html          # 新版 UI 文件
├── models/                 # 存放模型文件
│   └── best.pt             # YOLO 模型权重
├── legacy/                 # 旧版归档
│   └── app_tk.py           # (原版) Tkinter 版本的主程序
├── app_modern.py           # (新版) PyWebView 版本的主程序 (原 main.py)
├── requirements.txt        # 依赖列表
├── README.md               # 项目说明文档
└── .gitignore              # Git 忽略文件
```

## 📚 数据集与模型来源 (Dataset & Model Source)

*   **Model Weights (模型权重):**
    *   [HuggingFace Link](https://huggingface.co/laowanglaowang/yolov11m_anime_Image_segmentation)

*   **Training Dataset (训练数据集):**
    *   [HuggingFace Dataset Link](https://huggingface.co/datasets/laowanglaowang/anime_head_body_leg)
    *   基于 `DanbooRegion2020` 后续又进行了添加。
    *   *Based on `DanbooRegion2020` with subsequent additions.*

## 📄 开源协议 (License)

本项目遵循 MIT 协议开源。详细信息请参阅 LICENSE 文件。
This project is licensed under the MIT License. See the LICENSE file for details.
