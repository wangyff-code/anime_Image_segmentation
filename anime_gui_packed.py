import os
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
from ultralytics import YOLO
import threading

def resource_path(relative_path):
    """ 获取资源的绝对路径，用于 PyInstaller 打包 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AnimePartExtractorFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("二次元部位提取工具 (纯净文件名版)")
        self.root.geometry("900x700")

        # --- 硬编码模型 ---
        self.model_filename = "best.pt" 
        self.model_path = resource_path(self.model_filename)

        # --- 变量 ---
        self.src_dir = tk.StringVar()
        self.dst_dir = tk.StringVar()
        
        self.var_exp_top = tk.DoubleVar(value=0.2) 
        self.var_exp_bottom = tk.DoubleVar(value=0.2)
        self.var_exp_side = tk.DoubleVar(value=0.2)
        
        self.target_class = tk.IntVar(value=0) 
        self.var_suffix = tk.StringVar(value="_head") # 默认后缀

        self.is_paused = False
        self.is_running = False

        self.create_widgets()
        self.check_model()

    def check_model(self):
        if not os.path.exists(self.model_path):
            messagebox.showerror("错误", f"内置模型丢失！\n请确保 {self.model_filename} 在同一目录下。")
            self.btn_start.config(state='disabled')
        else:
            self.log(f"系统就绪。")

    def on_target_change(self):
        t_id = self.target_class.get()
        # 这里你可以修改默认的建议后缀
        if t_id == 0: self.var_suffix.set("_head")
        elif t_id == 1: self.var_suffix.set("_torso")
        elif t_id == 2: self.var_suffix.set("_legs")

    def create_widgets(self):
        left_panel = tk.Frame(self.root)
        left_panel.pack(side='left', fill='y', padx=10, pady=10)

        # 1. 文件夹
        group_path = tk.LabelFrame(left_panel, text="工作区", padx=10, pady=5)
        group_path.pack(fill='x', pady=5)
        tk.Label(group_path, text="输入文件夹:").pack(anchor='w')
        tk.Entry(group_path, textvariable=self.src_dir).pack(fill='x')
        tk.Button(group_path, text="📂 选择", command=self.select_src).pack(anchor='e')
        tk.Label(group_path, text="输出文件夹:").pack(anchor='w')
        tk.Entry(group_path, textvariable=self.dst_dir).pack(fill='x')
        tk.Button(group_path, text="📂 选择", command=self.select_dst).pack(anchor='e')

        # 2. 提取设置
        group_target = tk.LabelFrame(left_panel, text="提取设置", padx=10, pady=5, fg="blue")
        group_target.pack(fill='x', pady=10)
        
        frame_radio = tk.Frame(group_target)
        frame_radio.pack(fill='x', pady=2)
        tk.Radiobutton(frame_radio, text="头部", variable=self.target_class, value=0, command=self.on_target_change).pack(side='left')
        tk.Radiobutton(frame_radio, text="躯干", variable=self.target_class, value=1, command=self.on_target_change).pack(side='left')
        tk.Radiobutton(frame_radio, text="腿部", variable=self.target_class, value=2, command=self.on_target_change).pack(side='left')

        tk.Label(group_target, text="自定义后缀:", font=("Arial", 9, "bold")).pack(anchor='w', pady=(5,0))
        tk.Entry(group_target, textvariable=self.var_suffix, bg="#FFF8DC").pack(fill='x', pady=2)
        tk.Label(group_target, text="结果示例: ABC.jpg -> ABC_head.jpg", fg="gray", font=("Arial", 8)).pack(anchor='w')

        # 3. 参数
        group_param = tk.LabelFrame(left_panel, text="边缘扩充 (0.2=20%)", padx=10, pady=5)
        group_param.pack(fill='x', pady=10)
        self.create_param_entry(group_param, "顶部:", self.var_exp_top)
        self.create_param_entry(group_param, "底部:", self.var_exp_bottom)
        self.create_param_entry(group_param, "左右:", self.var_exp_side)

        # 4. 按钮
        btn_frame = tk.Frame(left_panel)
        btn_frame.pack(fill='x', pady=10)
        self.btn_start = tk.Button(btn_frame, text="▶ 开始运行", command=self.start_thread, bg="#4CAF50", fg="white", height=2)
        self.btn_start.pack(side='left', fill='x', expand=True, padx=2)
        self.btn_pause = tk.Button(btn_frame, text="⏸ 暂停", command=self.toggle_pause, bg="#FF9800", fg="white", height=2, state='disabled')
        self.btn_pause.pack(side='left', fill='x', expand=True, padx=2)

        # 5. 日志
        self.log_text = scrolledtext.ScrolledText(left_panel, height=10)
        self.log_text.pack(fill='both', expand=True)

        # 预览
        right_panel = tk.Frame(self.root, bg="#EEE", width=400)
        right_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        right_panel.pack_propagate(False)
        self.lbl_preview = tk.Label(right_panel, text="预览区域", bg="#DDD")
        self.lbl_preview.pack(expand=True, fill='both', padx=5, pady=5)

    def create_param_entry(self, parent, text, var):
        f = tk.Frame(parent)
        f.pack(fill='x')
        tk.Label(f, text=text, width=8).pack(side='left')
        tk.Entry(f, textvariable=var, width=8).pack(side='right')

    def select_src(self):
        p = filedialog.askdirectory()
        if p: self.src_dir.set(p)
    def select_dst(self):
        p = filedialog.askdirectory()
        if p: self.dst_dir.set(p)
    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def update_preview(self, pil_img):
        w, h = pil_img.size
        ratio = min(380/w, 380/h)
        new_size = (int(w*ratio), int(h*ratio))
        img = pil_img.copy().resize(new_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.lbl_preview.config(image=photo, text="")
        self.lbl_preview.image = photo

    def start_thread(self):
        t = threading.Thread(target=self.process_images)
        t.daemon = True
        t.start()

    def toggle_pause(self):
        if not self.is_running: return
        self.is_paused = not self.is_paused
        self.btn_pause.config(text="▶ 继续" if self.is_paused else "⏸ 暂停")
        self.log(">>> 暂停..." if self.is_paused else ">>> 继续...")

    def process_images(self):
        src, dst = self.src_dir.get(), self.dst_dir.get()
        t_id = self.target_class.get()
        user_suffix = self.var_suffix.get()
        
        if not src or not dst:
            messagebox.showwarning("提示", "请选择路径")
            return

        self.is_running = True
        self.is_paused = False
        self.btn_start.config(state='disabled')
        self.btn_pause.config(state='normal')

        try:
            model = YOLO(self.model_path)
            params = (self.var_exp_top.get(), self.var_exp_bottom.get(), self.var_exp_side.get())
            supported = ('.jpg', '.png', '.jpeg', '.webp')

            count = 0
            for root_path, dirs, files in os.walk(src):
                if os.path.abspath(dst).startswith(os.path.abspath(root_path)): continue
                rel = os.path.relpath(root_path, src)
                target_dir = os.path.join(dst, rel)
                if not os.path.exists(target_dir): os.makedirs(target_dir)

                for file in files:
                    while self.is_paused: time.sleep(0.1)
                    if not self.is_running: break

                    if file.lower().endswith(supported):
                        self.detect_and_save(model, os.path.join(root_path, file), target_dir, file, params, t_id, user_suffix)
                        count += 1
            
            messagebox.showinfo("完成", f"全部结束！共处理 {count} 张。")

        except Exception as e:
            messagebox.showerror("错误", str(e))
        finally:
            self.is_running = False
            self.btn_start.config(state='normal')
            self.btn_pause.config(state='disabled')

    def detect_and_save(self, model, src_path, target_dir, filename, params, target_id, user_suffix):
        e_top, e_btm, e_side = params
        try:
            with Image.open(src_path) as raw_img:
                if raw_img.mode != 'RGB': raw_img = raw_img.convert('RGB')
                
                results = model.predict(raw_img, conf=0.4, iou=0.5, verbose=False)
                
                obj_count = 0 
                
                for box in results[0].boxes:
                    if int(box.cls[0]) != target_id: continue
                    obj_count += 1
                    
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    w, h = x2-x1, y2-y1
                    
                    cy1 = max(0, y1 - h * e_top)
                    cy2 = min(raw_img.height, y2 + h * e_btm)
                    cx1 = max(0, x1 - w * e_side)
                    cx2 = min(raw_img.width, x2 + w * e_side)
                    
                    crop = raw_img.crop((cx1, cy1, cx2, cy2))
                    self.update_preview(crop)
                    
                    # 🔥🔥🔥 文件名核心逻辑修改 🔥🔥🔥
                    name_base = os.path.splitext(filename)[0]
                    ext = os.path.splitext(filename)[1]
                    
                    # 只有当这是检测到的第2个及以上的人时，才加序号
                    # 如果只有1个人，就保持纯净文件名
                    if obj_count == 1:
                         new_name = f"{name_base}{user_suffix}{ext}"
                    else:
                         new_name = f"{name_base}{user_suffix}_{obj_count}{ext}"
                    
                    save_path = os.path.join(target_dir, new_name)
                    crop.save(save_path)
                    self.log(f"保存: {new_name}")

        except Exception as e:
            self.log(f"Err: {filename} - {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimePartExtractorFinal(root)
    root.mainloop()