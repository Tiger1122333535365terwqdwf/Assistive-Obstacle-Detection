
"""项目入口：运行障碍物检测原型。

支持两种模式：
- `detector`：原有基于 `app.detector.ObstacleDetector` 的演示（默认）。
- `fusion`：调用 `app.pipeline.FusionDetector` 的融合检测演示，包含连续帧确认与三级风险分级。

支持用户身份选择（设置向导）与语音自适配。
"""

import argparse

from app.detector import ObstacleDetector
from app.pipeline import FusionDetector
from config.user_profile import UserProfile
from ui.setup_wizard import run_setup_wizard


def main():
	parser = argparse.ArgumentParser(description='障碍物识别原型入口')
	parser.add_argument('--mode', choices=['detector', 'fusion'], default='detector', help='运行模式')
	parser.add_argument('--model', help='模型路径（.pt/.onnx），默认会由向导或参数指定', default=None)
	parser.add_argument('--camera', type=int, default=0, help='摄像头索引')
	parser.add_argument('--conf', type=float, default=0.35, help='置信度阈值')
	parser.add_argument('--audio-only', action='store_true', help='仅语音/声音提醒（不显示窗口）')
	parser.add_argument('--focal', type=float, default=1000.0, help='相机近似焦距（像素），用于单目测距（别名：--focal-px）')
	parser.add_argument('--focal-px', type=float, default=None, help='相机近似焦距（像素），用于单目测距，与 --focal 等价，若提供则覆盖 --focal')
	parser.add_argument('--device', default=None, help='推理设备，例如 cpu 或 cuda:0')
	parser.add_argument('--half', action='store_true', help='半精度推理（仅CUDA）')
	parser.add_argument('--backend', choices=['auto', 'ultra', 'onnx'], default='auto', help='推理后端')
	parser.add_argument('--imgsz', type=int, default=640, help='推理输入尺寸')
	parser.add_argument('--refine-edges', action='store_true', help='启用检测框边缘细化')
	parser.add_argument('--calib-k', type=float, default=1.6, help='测距系数')
	parser.add_argument('--calib-min', type=float, default=0.4, help='测距下限（米）')
	parser.add_argument('--calib-max', type=float, default=12.0, help='测距上限（米）')
	parser.add_argument('--user-profile', choices=['elderly', 'child', 'blind', 'standard'], default=None, help='用户身份预设')
	parser.add_argument('--skip-wizard', action='store_true', help='跳过设置向导')
	parser.add_argument('--use-depth-net', action='store_true', help='启用轻量单目深度网络辅助测距（MiDaS small）')
	parser.add_argument('--distance-engine', choices=['classic', 'advanced'], default='advanced', help='距离估计引擎选择')
	args = parser.parse_args()

	# 处理 focal 参数别名
	focal_px = args.focal_px if args.focal_px is not None else args.focal

	# 用户身份与设置
	if args.user_profile:
		user_profile = UserProfile(args.user_profile)
		device = args.device or "cpu"
		model = args.model
		backend = args.backend
	elif args.skip_wizard:
		user_profile = UserProfile("standard")
		device = args.device or "cpu"
		model = args.model or "yolov8n.pt"
		backend = args.backend
	else:
		# 运行设置向导
		config = run_setup_wizard()
		user_profile = config["user_profile"]
		device = config["device"] if config["device"] != "auto" else (args.device or "cpu")
		model = config["model"]
		backend = config["backend"]

	if args.mode == 'detector':
		detector = ObstacleDetector(
			model_path=model,
			camera_index=args.camera,
			conf=args.conf,
			audio_only=args.audio_only,
			device=device,
			half=args.half,
			backend=backend,
			imgsz=args.imgsz,
			refine_edges=args.refine_edges,
			calib_k=args.calib_k,
			calib_min=args.calib_min,
			calib_max=args.calib_max,
			user_profile=user_profile,
			focal_px=focal_px,
			use_depth_net=args.use_depth_net,
			distance_engine=args.distance_engine,
		)
		detector.run()
	else:
		def _speak(text: str):
			try:
				import winsound
				winsound.Beep(1500, 120)
			except Exception:
				pass
			try:
				import pyttsx3
				engine = pyttsx3.init()
				engine.setProperty('rate', user_profile.rate)
				engine.setProperty('volume', user_profile.volume)
				engine.say(text)
				engine.runAndWait()
			except Exception:
				print('[ALERT]', text)

		fd = FusionDetector(model_path=model or 'yolov8n.pt', focal_px=focal_px, conf=args.conf, device=device or 'cpu')
		audio_fn = _speak
		fd.run_camera(cam_index=args.camera, audio_fn=audio_fn)


if __name__ == '__main__':
	main()
