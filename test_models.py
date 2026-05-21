"""
障碍物检测系统 - 快速功能测试
不使用 GUI，直接测试检测逻辑
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from config.user_profile import UserProfile
from app.detector import ObstacleDetector

def test_model_loading():
    """测试模型加载"""
    print("\n" + "="*60)
    print("模型加载测试")
    print("="*60)
    
    # 测试 PyTorch
    print("\n[测试1] PyTorch 后端...")
    pytorch_model = "runs/detect/train_lr_restart/weights/best.pt"
    
    if not Path(pytorch_model).exists():
        print(f"  错误: 模型文件不存在 {pytorch_model}")
        return False
    
    try:
        detector_pt = ObstacleDetector(
            model_path=pytorch_model,
            camera_index=0,
            conf=0.35,
            audio_only=True,  # 不播放音频
            device="cpu",
            backend="ultra",
            user_profile=UserProfile("standard")
        )
        detector_pt.load_model()
        print("  成功: PyTorch 模型加载完成")
    except Exception as e:
        print(f"  失败: {str(e)}")
        return False
    
    # 测试 ONNX FP16
    print("\n[测试2] ONNX FP16 后端...")
    onnx_model = "runs/optimized/best_fp16.onnx"
    
    if not Path(onnx_model).exists():
        print(f"  错误: 模型文件不存在 {onnx_model}")
        return False
    
    try:
        detector_onnx = ObstacleDetector(
            model_path=onnx_model,
            camera_index=0,
            conf=0.35,
            audio_only=True,
            device="cpu",
            backend="onnx",
            user_profile=UserProfile("standard")
        )
        detector_onnx.load_model()
        print("  成功: ONNX FP16 模型加载完成")
    except Exception as e:
        print(f"  失败: {str(e)}")
        return False
    
    print("\n" + "="*60)
    print("所有模型加载测试通过!")
    print("="*60)
    return True

def test_user_profiles():
    """测试用户配置"""
    print("\n" + "="*60)
    print("用户配置测试")
    print("="*60)
    
    profiles = ["elderly", "child", "blind", "standard"]
    
    for profile_key in profiles:
        print(f"\n[{profile_key.upper()}]")
        try:
            profile = UserProfile(profile_key)
            print(f"  名称: {profile.name}")
            print(f"  问候: {profile.get_greeting()}")
            print(f"  告别: {profile.get_farewell()}")
            
            # 测试警告消息
            msg = profile.get_alert_message("人", 2.5, "很近")
            print(f"  警告示例: {msg}")
        except Exception as e:
            print(f"  失败: {str(e)}")
            return False
    
    print("\n" + "="*60)
    print("所有用户配置测试通过!")
    print("="*60)
    return True

def main():
    print("\n")
    print("*" * 60)
    print("*" + " "*58 + "*")
    print("*" + "  障碍物检测系统 - 快速功能测试".center(58) + "*")
    print("*" + " "*58 + "*")
    print("*" * 60)
    
    success = True
    
    # 测试用户配置
    if not test_user_profiles():
        success = False
    
    # 测试模型加载
    if not test_model_loading():
        success = False
    
    if success:
        print("\n" + "="*60)
        print("所有测试通过! 系统已准备好使用")
        print("="*60)
        print("\n下一步：")
        print("  1. 运行: python ui/gui_app.py")
        print("  2. 或者运行: run_gui.bat")
        print("\n")
    else:
        print("\n" + "="*60)
        print("部分测试失败，请检查上面的错误信息")
        print("="*60 + "\n")

if __name__ == "__main__":
    main()
