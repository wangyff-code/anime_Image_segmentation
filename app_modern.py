import os
import sys
import threading
import base64
import numpy as np
import onnxruntime as ort
import webview
from io import BytesIO
from PIL import Image, ImageDraw

def resource_path(relative_path):
    """ 获取资源绝对路径 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AnimeApi:
    def __init__(self):
        self._stop_flag = False
        self._thread = None
        self.model_path = resource_path(os.path.join("models", "best.onnx"))
        self.session = None
        self.input_name = None
        self.input_shape = None

    def _init_model(self):
        """ 延迟加载模型，显式指定 CPU 运行 """
        if self.session is None:
            # 关键点：providers 参数
            # 强制指定 'CPUExecutionProvider'
            # 这样就算环境里有 GPU，它也会强制用 CPU，避免加载 CUDA 库
            self.session = ort.InferenceSession(
                self.model_path, 
                providers=['CPUExecutionProvider']
            )
            
            self.input_name = self.session.get_inputs()[0].name
            self.input_shape = self.session.get_inputs()[0].shape 
            
            # (可选) 打印确认一下正在使用的设备
            print(f"当前推理设备: {self.session.get_providers()}")

    def select_folder(self):
        window = webview.windows[0]
        result = window.create_file_dialog(webview.FOLDER_DIALOG)
        return result[0] if result else None

    def start_process(self, config):
        if self._thread and self._thread.is_alive(): return
        self._stop_flag = False
        self._thread = threading.Thread(target=self._process_logic, args=(config,))
        self._thread.daemon = True
        self._thread.start()

    def stop_process(self):
        self._stop_flag = True

    def _process_logic(self, config):
        window = webview.windows[0]
        if not os.path.exists(self.model_path):
            window.evaluate_js("app.finishProcess('失败: 模型丢失')")
            return

        try:
            self._init_model() # 加载 ONNX Runtime
            
            src, dst = config['src'], config['dst']
            t_id = config['target_id']
            suffix = config['suffix']
            e_top, e_btm, e_side = config['params']
            
            # 模型需要的输入宽高 (例如 640)
            model_h, model_w = self.input_shape[2], self.input_shape[3]

            # 1. 扫描文件
            window.evaluate_js("app.setStatus('正在扫描...')")
            files_to_process = []
            for root, _, files in os.walk(src):
                if os.path.abspath(root).startswith(os.path.abspath(dst)): continue
                for f in files:
                    if f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp')):
                        files_to_process.append((root, f))
            
            total = len(files_to_process)
            if total == 0:
                window.evaluate_js("app.finishProcess('未发现图片')")
                return
            
            window.evaluate_js(f"app.log('发现 {total} 张图片', 'success')")

            # 2. 处理循环
            processed = 0
            for root_path, file_name in files_to_process:
                if self._stop_flag: break
                
                full_path = os.path.join(root_path, file_name)
                rel_path = os.path.relpath(root_path, src)
                target_dir = os.path.join(dst, rel_path)
                if not os.path.exists(target_dir): os.makedirs(target_dir)

                try:
                    with Image.open(full_path) as raw_img:
                        if raw_img.mode != 'RGB': raw_img = raw_img.convert('RGB')
                        orig_w, orig_h = raw_img.size

                        # --- 极简预处理 (Pillow Resize + Numpy转换) ---
                        # 为了代码最简化，这里直接暴力 Resize 到 640x640
                        # 如果需要保持比例 Letterbox，代码会多几行，这里选最简方案
                        img_resized = raw_img.resize((model_w, model_h)) 
                        
                        # 归一化 (H,W,C) -> (1,C,H,W)
                        input_data = np.array(img_resized, dtype=np.float32) / 255.0
                        input_data = input_data.transpose(2, 0, 1) # HWC -> CHW
                        input_data = np.expand_dims(input_data, axis=0) # 增加 Batch 维度

                        # --- 推理 (ONNX Runtime) ---
                        # 输出 output 通常形状是 (1, N, 6) -> [batch, dets, (x1,y1,x2,y2,conf,cls)]
                        outputs = self.session.run(None, {self.input_name: input_data})
                        detections = outputs[0][0] # 取第一个 batch

                        obj_c = 0
                        for det in detections:
                            # det = [x1, y1, x2, y2, conf, cls]
                            # 大多数 nms=True 的导出，如果没检测到，或者是 padding 的行，conf 会是 0
                            score = det[4]
                            cls_id = int(det[5])
                            
                            if score < 0.4 or cls_id != t_id:
                                continue

                            obj_c += 1
                            
                            # 坐标还原 (因为我们前面是暴力 resize，这里直接按比例还原)
                            x1 = det[0] * (orig_w / model_w)
                            y1 = det[1] * (orig_h / model_h)
                            x2 = det[2] * (orig_w / model_w)
                            y2 = det[3] * (orig_h / model_h)
                            
                            # 计算扩展裁切
                            w_box, h_box = x2 - x1, y2 - y1
                            cy1 = max(0, y1 - h_box * e_top)
                            cy2 = min(orig_h, y2 + h_box * e_btm)
                            cx1 = max(0, x1 - w_box * e_side)
                            cx2 = min(orig_w, x2 + w_box * e_side)

                            # 裁切与保存
                            crop = raw_img.crop((cx1, cy1, cx2, cy2))
                            
                            # 生成预览 (仅第一张)
                            if obj_c > 0:
                                preview = crop.copy()
                                pd = ImageDraw.Draw(preview)
                                # 在预览图上画出原始框 (相对坐标)
                                pd.rectangle([x1-cx1, y1-cy1, x2-cx1, y2-cy1], outline="#00cec9", width=3)
                                preview.thumbnail((300, 300))
                                bio = BytesIO()
                                preview.save(bio, format="JPEG")
                                b64 = base64.b64encode(bio.getvalue()).decode()
                                window.evaluate_js(f"app.updatePreview('data:image/jpeg;base64,{b64}')")

                                # 保存文件
                                name, ext = os.path.splitext(file_name)
                                save_name = f"{name}{suffix}_{obj_c}{ext}" if obj_c > 1 else f"{name}{suffix}{ext}"
                                crop.save(os.path.join(target_dir, save_name))
                                window.evaluate_js(f"app.log('提取: {save_name}')")

                except Exception as e:
                    print(f"Error: {e}")

                processed += 1
                if processed % 5 == 0 or processed == total:
                    pct = (processed / total) * 100
                    window.evaluate_js(f"app.updateProgress({pct:.1f}, {processed}, {total})")

            window.evaluate_js(f"app.finishProcess('{('已暂停' if self._stop_flag else '完成')}')")

        except Exception as e:
            window.evaluate_js(f"app.finishProcess('系统错误: {str(e)}')")

if __name__ == '__main__':
    api = AnimeApi()
    html_path = resource_path(os.path.join("assets", "index.html"))
    window = webview.create_window(
        title="Anime Extractor (ONNX E2E)",
        url=html_path,
        js_api=api,
        width=1000, height=700
    )
    webview.start()