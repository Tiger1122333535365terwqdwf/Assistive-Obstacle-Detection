# 障碍物识别原型（老人、儿童、残障人士友好）

这是一个最小可运行的原型，演示如何使用摄像头 + YOLO 模型检测障碍物，并通过声音或语音提醒用户。适合作为智能眼镜或带语音提示的可穿戴设备原型的起点。

快速开始

1. 建议在 Windows 或 Linux 上使用 Python 3.8+。
2. 安装依赖：

```powershell
uv sync
```

或手动：

```powershell
pip install -r requirements.txt
```

3. **推荐：使用图形化界面（最简单）**

**方式一：桌面 GUI（Tkinter）**
```powershell
# 双击运行
run_gui.bat

# 或命令行
uv run python ui/gui_app.py
```

**方式二：Web 界面（Gradio）**
```powershell
# 双击运行
run_web.bat

# 或命令行
uv run python ui/web_app.py
# 然后在浏览器打开 http://localhost:7860
```

**方式三：命令行向导**
```powershell
uv run python main.py --mode detector
```

向导会引导你选择：身份（老人/儿童/盲人/标准）→ 设备（CPU/GPU）→ 后端（PT/ONNX-FP32/FP16）

4. **快速运行（跳过向导）**

```powershell
# 老人模式，ONNX FP16，CPU [推荐]
uv run python main.py --mode detector --user-profile elderly --backend onnx --model runs/optimized/best_fp16.onnx --device cpu

# 儿童模式，PT half 精度，CUDA
uv run python main.py --mode detector --user-profile child --backend ultra --device cuda:0 --half

# 视障人士，ONNX FP16，CPU（平衡性能和精度）
uv run python main.py --mode detector --user-profile blind --backend onnx --model runs/optimized/best_fp16.onnx --device cpu

# 仅语音/声音提醒（无 GUI）
uv run python main.py --mode detector --user-profile elderly --audio-only
```

**注意**：INT8 静态量化有 ONNX opset 兼容性问题。推荐使用 **FP16**（12.2 MB → 6.2 MB，50% 压缩，完全兼容 CPU）。

说明

- `detector.py`：摄像头采集、YOLO 推理、简单基于目标在画面中高度的距离估计、语音提醒（自适配用户身份）。
- 默认使用 `yolov8n.pt` 预训练权重（Ultralytics）。首次运行若没有本地权重会尝试下载。

**用户身份与语音自适配**

系统提供 4 种预设身份，每种对应不同的语速、措辞风格：

| 身份 | 语速 | 描述 | 示例消息 |
|------|------|------|---------|
| 老人 | 100 | 缓慢清晰，措辞谨慎 | "警告，前方有 person，距离 2.5 米。请小心。" |
| 儿童 | 120 | 正常速度，措辞简单活泼 | "小心！前面有个 person，大约在 2.5 米外。请靠一靠！" |
| 视障人士 | 130 | 清晰准确，提供方位和详细距离 | "警告。前方检测到 person。估计距离 2.5 米。请谨慎前行。" |
| 标准 | 130 | 中速，通用格式 | "检测到 person，距离约 2.5 米。" |

启动时可通过以下方式选择身份：
1. **交互向导**（推荐）：`uv run python main.py` 自动启动菜单
2. **命令行参数**：`--user-profile elderly/child/blind/standard`

可视化界面

系统提供 **三种使用方式**：

### 1. 🎨 桌面 GUI（Tkinter）- 推荐本地使用
```powershell
.\run_gui.bat
# 或
uv run python ui/gui_app.py
```

**特点**：
- ✅ 启动快速（1秒）
- ✅ 响应灵敏
- ✅ 实时视频显示
- ✅ 检测日志记录
- ✅ 无需浏览器

### 2. 🌐 Web UI（Gradio）- 推荐演示/远程访问
```powershell
.\run_web.bat
# 或
uv run python ui/web_app.py
# 浏览器访问 http://localhost:7860
```

**特点**：
- ✅ 界面美观现代
- ✅ 支持图片上传
- ✅ 支持实时摄像头
- ✅ 可调节置信度
- ✅ 可远程访问（手机/平板）

### 3. ⌨️ 命令行向导
```powershell
uv run python main.py --mode detector
```

**详细使用指南**：请查看 [docs/UI_GUIDE.md](docs/UI_GUIDE.md)

---

下一步建议

- 采集并标注 ~500 张居家/社区场景图像，补足 COCO/KITTI 中的缺失视角与小目标样本。
- 在目标边缘设备上测试 ONNX 或 TFLite 量化模型并记录延迟与误报率。
- 根据不同用户实际反馈调整语音措辞、提醒频率、置信度阈值。
- 扩展 UI 功能：录制视频、检测历史回放、统计报告等。

新增脚本与模块（已完成）

- `scripts/prepare_data.py`：数据整理与 data.yaml 生成。
- `scripts/train_yolov8.py`：训练。
- `scripts/quantize_yolo.py`：导出 ONNX（FP32/FP16）与 INT8（动态/静态量化），输出到 `runs/optimized/`。
- `scripts/prune_yolo.py`：掩码式剪枝（支持结构化通道掩码/非结构化），输出到 `runs/pruned/`。
- `scripts/benchmark.py`：快速吞吐测试（PT/ONNX/INT8）。
- `app/pipeline.py`：融合检测 + 连续帧验证 + 三级风险分级。
- `app/detector.py`：实时检测/语音；支持 PT/ONNX 后端、half 精度、边缘细化、简易测距校准。

相机标定与焦距（快速指南）

1. 简单标定方法：选一个已知高度的物体（例如 1.7m 的成人），在已知距离（例如 2m）处拍照，测量边界框的像素高度 `h_px`，则焦距（像素）可估计为：

	focal_px = (h_px * distance_m) / real_height_m

2. 将估计到的 `focal_px` 填入 `app/pipeline.py` 或在调用处传入。

快速试验（示例命令，建议使用 uv 运行）

```powershell
# 导出 ONNX（FP32/FP16）
uv run python scripts/quantize_yolo.py --weights runs/detect/train9/weights/best.pt --outdir runs/optimized --imgsz 640 --opset 12 --half

# 动态 INT8 量化
uv run python scripts/quantize_yolo.py --weights runs/detect/train9/weights/best.pt --outdir runs/optimized --imgsz 640 --opset 12 --int8

# 剪枝（掩码式结构化 20%）
uv run python scripts/prune_yolo.py --weights runs/detect/train9/weights/best.pt --output runs/pruned --amount 0.2 --structured --device cpu

# 吞吐基准（示例跑 ONNX FP16）
uv run python scripts/benchmark.py --model runs/optimized/best_fp16.onnx --source data/custom/val/images --device cpu --runs 30 --warmup 3 --imgsz 640

# 实时检测（PT half 精度，CUDA）
uv run python main.py --mode detector --model runs/detect/train9/weights/best.pt --backend ultra --device cuda:0 --half --conf 0.35

# 实时检测（ONNX 后端）
uv run python main.py --mode detector --model runs/optimized/best_fp32.onnx --backend onnx --imgsz 640 --conf 0.35 --device cpu

# 融合演示
uv run python -c "from app.pipeline import FusionDetector; FusionDetector(model_path='runs/detect/train9/weights/best.pt', conf=0.35).run_camera(cam_index=0)"
```

推理后端与优化选项
- PT（ultra）：支持 `--device`、`--half`，适合 GPU。
- ONNX（onnxruntime）：`--backend onnx`，可跑 CPU/GPU，支持 FP32/FP16/INT8。
- 边缘细化：`--refine-edges` 对细长/大目标轻微扩张边界，减少截断。
- 简易测距校准：`--calib-k`/`--calib-min`/`--calib-max`，距离≈ k / sqrt(box_area_ratio)，区间裁剪。


