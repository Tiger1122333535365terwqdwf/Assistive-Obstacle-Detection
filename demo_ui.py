"""
快速演示 - 测试 UI 功能（无摄像头模拟）
"""
import numpy as np
import cv2
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.user_profile import UserProfile


def create_demo_frame():
    """创建演示画面"""
    # 创建一个简单的测试图像
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    frame[:] = (50, 50, 50)  # 深灰色背景
    
    # 绘制一些模拟的"障碍物"
    # 模拟人（矩形）
    cv2.rectangle(frame, (200, 150), (350, 400), (100, 150, 200), -1)
    cv2.putText(frame, "Person", (220, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # 模拟椅子（矩形）
    cv2.rectangle(frame, (400, 250), (500, 350), (150, 100, 100), -1)
    cv2.putText(frame, "Chair", (415, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # 添加标题
    cv2.putText(frame, "Demo Mode - No Camera", (150, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    
    return frame


def test_profiles():
    """测试不同用户配置文件"""
    print("=" * 60)
    print("用户配置文件测试")
    print("=" * 60)
    
    profiles = ["elderly", "child", "blind", "standard"]
    
    for profile_key in profiles:
        profile = UserProfile(profile_key)
        print(f"\n【{profile.name}】")
        print(f"  语速: {profile.rate} WPM")
        print(f"  音量: {profile.volume}")
        
        # 模拟检测消息
        message = profile.get_alert_message("人", 2.5, "非常近")
        print(f"  示例消息: {message}")
        
        # 测试问候语
        print(f"  开始问候: {profile.get_greeting()}")
        print(f"  结束问候: {profile.get_farewell()}")


def test_ui_config():
    """测试 UI 配置选项"""
    print("\n" + "=" * 60)
    print("UI 配置选项")
    print("=" * 60)
    
    configs = {
        "用户身份": ["老人模式", "儿童模式", "视障人士", "标准模式"],
        "计算设备": ["CPU", "GPU (cuda:0)", "自动选择"],
        "推理后端": ["PyTorch", "ONNX FP32", "ONNX FP16"]
    }
    
    for category, options in configs.items():
        print(f"\n{category}:")
        for i, option in enumerate(options, 1):
            marker = "●" if i == 3 else "○"  # 默认选第3个
            print(f"  {marker} {option}")


def simulate_detection():
    """模拟检测流程"""
    print("\n" + "=" * 60)
    print("模拟检测流程")
    print("=" * 60)
    
    frame = create_demo_frame()
    
    # 模拟检测结果
    detections = [
        {"label": "人", "conf": 0.95, "box": (200, 150, 350, 400), "dist": 2.5},
        {"label": "椅子", "conf": 0.87, "box": (400, 250, 500, 350), "dist": 4.2}
    ]
    
    profile = UserProfile("blind")
    
    print(f"\n{profile.get_greeting()}\n")
    print("开始检测...\n")
    
    for det in detections:
        # 在画面上绘制
        x1, y1, x2, y2 = det["box"]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{det['label']} {det['conf']:.2f}", 
                   (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # 估算接近程度
        box_height = y2 - y1
        if box_height > 200:
            prox = "极近"
        elif box_height > 100:
            prox = "非常近"
        else:
            prox = "中等"
        
        # 生成消息
        message = profile.get_alert_message(det["label"], det["dist"], prox)
        print(f"[检测] {message}\n")
    
    # 显示结果画面
    print(f"{profile.get_farewell()}\n")
    print("检测完成！")
    
    # 保存演示图片
    output_path = Path(__file__).parent.parent / "demo_output.jpg"
    cv2.imwrite(str(output_path), frame)
    print(f"\n演示图片已保存到: {output_path}")


def main():
    print("\n" + "█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "    智能障碍物检测系统 - UI 功能演示".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60 + "\n")
    
    # 1. 测试用户配置
    test_profiles()
    
    # 2. 测试 UI 选项
    test_ui_config()
    
    # 3. 模拟检测流程
    simulate_detection()
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成！")
    print("=" * 60)
    print("\n提示：运行以下命令启动真实 UI：")
    print("  桌面 GUI: uv run python ui/gui_app.py")
    print("  Web UI:   uv run python ui/web_app.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
