
# ✂️ Anime Image Segmentation Tool (二次元图像部位分割工具)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![YOLO](https://img.shields.io/badge/Model-YOLO-green.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

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

## 🛠️ 安装与使用 (Installation & Usage)

### 1. 环境准备 (Prerequisites)

确保你的电脑已安装 Python 3.8 或以上版本。
Ensure you have Python 3.8 or higher installed.

```bash
# 克隆仓库 / Clone the repository
git clone https://github.com/wangyff-code/anime_Image_segmentation.git
cd anime_Image_segmentation

# 安装依赖库 / Install dependencies
pip install ultralytics pillow
# Note: tkinter is usually built-in with Python.
```

### 2. 模型准备 (Model Preparation)

本工具需要加载训练好的 YOLO 模型文件（`.pt`）。
This tool requires a pre-trained YOLO model file (`.pt`).

*   **Model Download Link (模型下载):** [HuggingFace - yolov11m_anime_Image_segmentation](https://huggingface.co/laowanglaowang/yolov11m_anime_Image_segmentation)
*   请确保将你的模型文件重命名为 **`best.pt`**。
*   将 `best.pt` 放入项目根目录下。
*   *Please rename the downloaded model to **`best.pt`** and place it in the project root directory.*

### 3. 运行程序 (Run)

```bash
python anime_gui_packed.py
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
├── anime_gui_packed.py   # 主程序源码 (Main source code)
├── best.pt               # YOLO 模型权重 (Model weights - Download separately)
├── requirements.txt      # (可选) 依赖列表 (Optional dependencies)
└── README.md             # 说明文档 (Documentation)
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
