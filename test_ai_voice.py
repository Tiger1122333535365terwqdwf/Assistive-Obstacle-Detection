"""测试AI语音生成模块"""
import os
from config.ai_voice import AIVoiceGenerator
from config.user_profile import UserProfile


def test_ai_voice():
    """测试AI语音生成功能"""
    print("=" * 80)
    print("DeepSeek AI 语音生成模块测试")
    print("=" * 80)
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("\n⚠️  未设置 DEEPSEEK_API_KEY 环境变量")
        print("请先设置：$env:DEEPSEEK_API_KEY='your-api-key'")
        print("\n将使用固定模板进行测试...\n")
    else:
        print(f"\n✓ 已检测到 API 密钥: {api_key[:8]}...")
    
    # 初始化生成器
    generator = AIVoiceGenerator(api_key=api_key)
    
    # 测试场景
    test_profiles = ["elderly", "child", "blind", "standard"]
    test_detections = [
        {
            "label": "汽车",
            "distance": 3.5,
            "proximity": "较近",
            "confidence": 0.92
        }
    ]
    
    print("\n" + "=" * 80)
    print("测试1: 欢迎语生成")
    print("=" * 80)
    for profile in test_profiles:
        up = UserProfile(profile)
        print(f"\n【{up.name}】")
        greeting = generator.generate_greeting(profile, use_ai=bool(api_key))
        print(f"  {greeting}")
    
    print("\n" + "=" * 80)
    print("测试2: 障碍物警告生成")
    print("=" * 80)
    for profile in test_profiles:
        up = UserProfile(profile)
        print(f"\n【{up.name}】")
        alert = generator.generate_alert(profile, test_detections, use_ai=bool(api_key))
        print(f"  {alert}")
    
    print("\n" + "=" * 80)
    print("测试3: 告别语生成")
    print("=" * 80)
    for profile in test_profiles:
        up = UserProfile(profile)
        print(f"\n【{up.name}】")
        farewell = generator.generate_farewell(profile, use_ai=bool(api_key))
        print(f"  {farewell}")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    
    if not api_key:
        print("\n提示：若要测试真实AI生成，请设置环境变量：")
        print("  PowerShell: $env:DEEPSEEK_API_KEY='sk-your-key'")
        print("  然后重新运行此脚本")


if __name__ == "__main__":
    test_ai_voice()
