"""
GUI 按钮功能测试脚本 - 不需要摄像头
模拟按钮点击并查看日志输出
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

import tkinter as tk
from ui.gui_app import DetectorGUI
import time

def test_button_click():
    """测试启动按钮"""
    root = tk.Tk()
    app = DetectorGUI(root)
    
    # 给 UI 一点初始化时间
    root.update()
    time.sleep(0.5)
    
    print("\n" + "="*60)
    print("GUI 按钮功能测试")
    print("="*60)
    
    print("\n[测试1] 检查按钮初始状态...")
    start_state = app.start_button.cget('state')
    stop_state = app.stop_button.cget('state')
    print(f"  启动按钮状态: {start_state}")
    print(f"  停止按钮状态: {stop_state}")
    
    print("\n[测试2] 点击启动按钮...")
    try:
        app.start_button.invoke()
        print("  按钮点击成功")
    except Exception as e:
        print(f"  错误: {e}")
    
    # 等待一些日志输出
    print("\n[测试3] 等待日志输出...")
    for i in range(5):
        root.update()
        time.sleep(0.2)
    
    print("\n[测试4] 检查日志输出...")
    log_content = app.log_text.get("1.0", tk.END)
    print(f"  日志行数: {len(log_content.splitlines())}")
    print("\n最后10行日志：")
    lines = log_content.strip().split('\n')
    for line in lines[-10:]:
        print(f"    {line}")
    
    print("\n[测试5] 检查按钮状态变化...")
    new_start_state = app.start_button.cget('state')
    new_stop_state = app.stop_button.cget('state')
    print(f"  启动按钮状态: {new_start_state} (期望: disabled)")
    print(f"  停止按钮状态: {new_stop_state} (期望: normal)")
    
    print("\n[测试6] 检查运行状态...")
    print(f"  is_running: {app.is_running} (期望: True)")
    
    if app.is_running:
        print("\n[测试成功] 按钮可以响应，检测线程已启动！")
    else:
        print("\n[测试失败] 检测线程未启动")
    
    print("\n[清理] 关闭窗口...")
    if app.is_running:
        app.stop_detection()
    
    root.quit()
    print("\n测试完成\n")

if __name__ == "__main__":
    test_button_click()
