import os
import sys
import threading
import base64
import time
from io import BytesIO
import webview
from PIL import Image, ImageDraw
from ultralytics import YOLO

# 1️⃣ 把 resource_path 提出来作为全局函数，方便各处调用
def resource_path(relative_path):
    """ 获取资源的绝对路径，兼容开发环境和 PyInstaller 打包环境 """
    try:
        # PyInstaller 会创建临时文件夹，路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AnimeApi:
    def __init__(self):
        self._stop_flag = False
        self._thread = None
        # 2️⃣ 这里调用全局的 resource_path
        self.model_path = resource_path(os.path.join("models", "best.pt"))

    # (之前的 resource_path 方法可以删掉了，因为用了全局的)

    def select_folder(self):
        window = webview.windows[0]
        result = window.create_file_dialog(webview.FOLDER_DIALOG)
        return result[0] if result else None

    def start_process(self, config):
        if self._thread and self._thread.is_alive():
            return
        
        self._stop_flag = False
        self._thread = threading.Thread(target=self._process_logic, args=(config,))
        self._thread.daemon = True
        self._thread.start()

    def stop_process(self):
        self._stop_flag = True

    def _process_logic(self, config):
        window = webview.windows[0]
        
        if not os.path.exists(self.model_path):
            window.evaluate_js("app.log('❌ 错误: 模型文件 best.pt 丢失！', 'error')")
            window.evaluate_js("app.finishProcess('失败: 模型丢失')")
            return

        try:
            model = YOLO(self.model_path)
            src, dst = config['src'], config['dst']
            t_id = config['target_id']
            suffix = config['suffix']
            e_top, e_btm, e_side = config['params']
            supported = ('.jpg', '.png', '.jpeg', '.webp')

            # --- 阶段1：扫描 ---
            window.evaluate_js("app.setStatus('正在扫描文件...')")
            total_files = 0
            file_list = [] 
            
            for root_path, dirs, files in os.walk(src):
                if os.path.abspath(root_path).startswith(os.path.abspath(dst)):
                    continue
                for file in files:
                    if file.lower().endswith(supported):
                        total_files += 1
                        file_list.append((root_path, file))

            if total_files == 0:
                window.evaluate_js("app.finishProcess('未发现图片')")
                return

            window.evaluate_js(f"app.log('共发现 {total_files} 张图片，开始处理...', 'success')")
            window.evaluate_js("app.setStatus('处理中...')")

            # --- 阶段2：处理 ---
            processed_count = 0
            
            for i, (root_path, file) in enumerate(file_list):
                if self._stop_flag: break
                
                full_path = os.path.join(root_path, file)
                rel = os.path.relpath(root_path, src)
                target_dir = os.path.join(dst, rel)
                if not os.path.exists(target_dir): os.makedirs(target_dir)

                try:
                    with Image.open(full_path) as raw_img:
                        if raw_img.mode != 'RGB': raw_img = raw_img.convert('RGB')
                        
                        results = model.predict(raw_img, conf=0.4, iou=0.5, verbose=False)
                        obj_c = 0
                        
                        for box in results[0].boxes:
                            if int(box.cls[0]) != t_id: continue
                            obj_c += 1
                            
                            x1, y1, x2, y2 = box.xyxy[0].tolist()
                            w, h = x2-x1, y2-y1
                            
                            cy1 = max(0, y1 - h * e_top)
                            cy2 = min(raw_img.height, y2 + h * e_btm)
                            cx1 = max(0, x1 - w * e_side)
                            cx2 = min(raw_img.width, x2 + w * e_side)
                            
                            crop = raw_img.crop((cx1, cy1, cx2, cy2))
                            
                            if obj_c > 0:
                                preview_img = crop.copy()
                                draw = ImageDraw.Draw(preview_img)
                                
                                rel_x1 = x1 - cx1
                                rel_y1 = y1 - cy1
                                rel_x2 = x2 - cx1
                                rel_y2 = y2 - cy1
                                
                                draw.rectangle([rel_x1, rel_y1, rel_x2, rel_y2], outline="#00cec9", width=3)
                                
                                preview_img.thumbnail((400, 400))
                                buffered = BytesIO()
                                preview_img.save(buffered, format="JPEG")
                                b64_str = "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode()
                                window.evaluate_js(f"app.updatePreview('{b64_str}')")
                                
                                name_base, ext = os.path.splitext(file)
                                new_name = f"{name_base}{suffix}{ext}" if obj_c == 1 else f"{name_base}{suffix}_{obj_c}{ext}"
                                crop.save(os.path.join(target_dir, new_name))
                                window.evaluate_js(f"app.log('提取: {new_name}')")

                except Exception as e:
                    print(f"Err: {e}")

                processed_count += 1
                
                if processed_count % 2 == 0 or processed_count == total_files:
                    percent = (processed_count / total_files) * 100
                    window.evaluate_js(f"app.updateProgress({percent:.1f}, {processed_count}, {total_files})")

            msg = "已暂停" if self._stop_flag else "🎉 处理完成"
            window.evaluate_js(f"app.finishProcess('{msg}')")

        except Exception as e:
            window.evaluate_js(f"app.finishProcess('运行出错: {str(e)}')")

if __name__ == '__main__':
    api = AnimeApi()
    
    # 3️⃣ 关键修复点：这里也必须使用 resource_path 来找 HTML
    html_path = resource_path(os.path.join("assets", "index.html"))
    
    # 打印路径确认一下（调试用，打包后看不到）
    print(f"Loading HTML from: {html_path}")
    
    if not os.path.exists(html_path):
        # 这是一个保险措施，如果找不到文件，写一个临时的
        # 但如果 resource_path 工作正常，这里不会触发
        print("HTML not found via resource_path!")

    window = webview.create_window(
        title="Anime Extractor Elite",
        url=html_path,  # 这里传入处理过的路径
        js_api=api,
        width=1100,
        height=760,
        min_size=(900, 600),
        resizable=True
    )
    webview.start(debug=False)