
# ✂️ Anime Image Segmentation Tool (二次元图像部位分割工具)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![YOLOv8](https://img.shields.io/badge/Model-YOLOv8-green.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey)


> **一个基于 YOLOv8 的本地化 GUI 工具，用于批量识别并提取二次元角色的头部、躯干或腿部。**  
> 专为数据集制作、素材收集和二次元图像处理设计。
![img](https://github.com/wangyff-code/anime_Image_segmentation/blob/main/example/20260103184447.png)

![img](https://github.com/wangyff-code/anime_Image_segmentation/blob/main/example/20260103184456.png)

![img](https://github.com/wangyff-code/anime_Image_segmentation/blob/main/example/20260103184501.png)
---

## ✨ 主要功能 (Features)

*   **📺 可视化操作界面**：基于 Tkinter 构建，无需编写代码，小白也能轻松上手。
*   **🤖 强大的识别模型**：内置 YOLOv8 逻辑，支持高精度的二次元角色部位检测。
*   **📂 批量处理**：支持递归扫描文件夹，保持原有的目录结构输出，适合大规模数据集清洗。
*   **📐 智能边缘扩充**：
    *   支持自定义**顶部、底部、左右**的扩充比例（默认为 0.2），防止切头去尾，保留完整发型和肢体。
*   **🏷️ 纯净文件名逻辑**：
    *   **单人图**：直接保存为 `文件名_后缀.jpg`（如 `image_head.jpg`）。
    *   **多人图**：自动添加序号（如 `image_head_2.jpg`），避免文件覆盖。
*   **🎯 多部位支持**：一键切换提取 **头部 (Head)**、**躯干 (Torso)** 或 **腿部 (Legs)**。
*   **👀 实时预览**：处理过程中可实时查看裁剪出的图像预览。

---


## 🛠️ 安装与使用 (Installation & Usage)

### 1. 环境准备

确保你的电脑已安装 Python 3.8 或以上版本。

```bash
# 克隆仓库
git clone https://github.com/wangyff-code/anime_Image_segmentation.git
cd anime_Image_segmentation

# 安装依赖库
pip install ultralytics pillow
# 注意：tkinter 通常是 Python 内置的，无需额外安装
```

### 2. 模型准备
best.pt   在
https://huggingface.co/laowanglaowang/yolov11m_anime_Image_segmentation

本工具需要加载训练好的 YOLO 模型文件（`.pt`）。
*   请确保将你的模型文件重命名为 **`best.pt`**。
*   将 `best.pt` 放入项目根目录下。


### 3. 运行程序

```bash
python anime_gui_packed.py
```

---

## ⚙️ 参数说明 (Settings)

在软件界面中，你可以调整以下参数以获得最佳效果：

| 参数区域 | 选项 | 说明 |
| :--- | :--- | :--- |
| **提取设置** | 头部 / 躯干 / 腿部 | 选择你要提取的目标部位。 |
| **自定义后缀** | 如 `_head` | 输出文件的后缀名。支持自定义，如改为 `_face`。 |
| **边缘扩充** | 顶部 (Top) | 向上扩展裁剪框的比例。建议设为 `0.2` 以保留头顶发饰。 |
| **边缘扩充** | 底部 (Bottom) | 向下扩展比例。提取头像时可适当减小。 |
| **边缘扩充** | 左右 (Side) | 向左右两侧扩展的比例。 |

---


## 📝 目录结构 (Directory Structure)

```text
anime_Image_segmentation/
├── anime_gui_packed.py   # 主程序源码
├── best.pt               # YOLO 模型权重文件 (需自行准备)
├── requirements.txt      # (可选) 依赖列表
└── README.md             # 说明文档
```
best.pt   在
https://huggingface.co/laowanglaowang/yolov11m_anime_Image_segmentation

训练的数据集在
https://huggingface.co/datasets/laowanglaowang/anime_head_body_leg

基于 DanbooRegion2020 后续又进行了添加
## 📄 开源协议 (License)

本项目遵循 MIT 协议开源。详细信息请参阅 LICENSE 文件。





