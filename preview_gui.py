"""
GUI 界面预览 - 演示按钮布局
"""
import tkinter as tk
from tkinter import ttk


def preview_gui():
    """预览 GUI 布局"""
    root = tk.Tk()
    root.title("GUI 预览 - 检查按钮可见性")
    root.geometry("1000x650")
    root.configure(bg="#f0f0f0")
    
    # 标题
    title_frame = tk.Frame(root, bg="#2c3e50", height=60)
    title_frame.pack(fill=tk.X, padx=0, pady=0)
    title_frame.pack_propagate(False)
    
    title_label = tk.Label(
        title_frame,
        text="🦯 智能障碍物检测系统",
        font=("微软雅黑", 20, "bold"),
        fg="white",
        bg="#2c3e50"
    )
    title_label.pack(pady=15)
    
    # 主内容
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    # 左侧：配置面板（固定宽度）
    left_frame = tk.Frame(main_frame, bg="white", relief=tk.RAISED, borderwidth=2, width=280)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=0)
    left_frame.pack_propagate(False)
    
    # 可滚动内容
    canvas = tk.Canvas(left_frame, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # 配置内容
    config_label = tk.Label(
        scrollable_frame,
        text="⚙️ 系统配置",
        font=("微软雅黑", 14, "bold"),
        bg="white",
        fg="#2c3e50"
    )
    config_label.pack(pady=12, padx=10)
    
    # 创建变量来存储选择
    profile_var = tk.StringVar(value="standard")
    device_var = tk.StringVar(value="cpu")
    backend_var = tk.StringVar(value="onnx_fp16")
    audio_var = tk.BooleanVar(value=False)
    
    # 用户身份
    profile_frame = tk.LabelFrame(
        scrollable_frame,
        text="👤 用户身份",
        font=("微软雅黑", 11, "bold"),
        bg="white",
        padx=15,
        pady=10
    )
    profile_frame.pack(fill=tk.X, padx=10, pady=8)
    
    profiles = [("老人模式", "elderly"), ("儿童模式", "child"), ("视障人士", "blind"), ("标准模式", "standard")]
    for text, value in profiles:
        rb = tk.Radiobutton(profile_frame, text=text, variable=profile_var, value=value, font=("微软雅黑", 10), bg="white")
        rb.pack(anchor=tk.W, pady=2)
    
    # 设备
    device_frame = tk.LabelFrame(
        scrollable_frame,
        text="🖥️ 计算设备",
        font=("微软雅黑", 11, "bold"),
        bg="white",
        padx=15,
        pady=10
    )
    device_frame.pack(fill=tk.X, padx=10, pady=8)
    
    devices = [("CPU", "cpu"), ("GPU", "cuda:0"), ("自动", "auto")]
    for text, value in devices:
        rb = tk.Radiobutton(device_frame, text=text, variable=device_var, value=value, font=("微软雅黑", 10), bg="white")
        rb.pack(anchor=tk.W, pady=2)
    
    # 后端
    backend_frame = tk.LabelFrame(
        scrollable_frame,
        text="⚡ 推理后端",
        font=("微软雅黑", 11, "bold"),
        bg="white",
        padx=15,
        pady=10
    )
    backend_frame.pack(fill=tk.X, padx=10, pady=8)
    
    backends = [("PyTorch", "pytorch"), ("ONNX FP32", "onnx_fp32"), ("ONNX FP16", "onnx_fp16")]
    for text, value in backends:
        rb = tk.Radiobutton(backend_frame, text=text, variable=backend_var, value=value, font=("微软雅黑", 10), bg="white")
        rb.pack(anchor=tk.W, pady=2)
    
    # 选项
    option_frame = tk.LabelFrame(
        scrollable_frame,
        text="🔧 选项",
        font=("微软雅黑", 11, "bold"),
        bg="white",
        padx=15,
        pady=10
    )
    option_frame.pack(fill=tk.X, padx=10, pady=8)
    
    cb = tk.Checkbutton(option_frame, text="仅语音模式", variable=audio_var, font=("微软雅黑", 10), bg="white")
    cb.pack(anchor=tk.W, pady=2)
    
    # ===== 关键：按钮区域 =====
    button_frame = tk.Frame(scrollable_frame, bg="white")
    button_frame.pack(fill=tk.X, padx=10, pady=15)
    
    # 显示当前选择
    info_frame = tk.Frame(scrollable_frame, bg="#ecf0f1")
    info_frame.pack(fill=tk.X, padx=10, pady=10)
    
    info_text = tk.StringVar()
    def update_info():
        info_text.set(f"当前选择: {profile_var.get()} | {device_var.get()} | {backend_var.get()}")
    
    info_label = tk.Label(info_frame, textvariable=info_text, font=("微软雅黑", 9), bg="#ecf0f1", fg="#2c3e50")
    info_label.pack(fill=tk.X, pady=5, padx=5)
    
    # 监听选择变化
    profile_var.trace("w", lambda *args: update_info())
    device_var.trace("w", lambda *args: update_info())
    backend_var.trace("w", lambda *args: update_info())
    
    # 初始化
    update_info()
    
    # 这些按钮应该清晰可见！
    start_button = tk.Button(
        button_frame,
        text="▶️  启动检测",
        font=("微软雅黑", 13, "bold"),
        bg="#27ae60",
        fg="white",
        relief=tk.RAISED,
        borderwidth=2,
        padx=15,
        pady=12,
        cursor="hand2"
    )
    start_button.pack(fill=tk.X, pady=6)
    
    stop_button = tk.Button(
        button_frame,
        text="⏹️  停止检测",
        font=("微软雅黑", 13, "bold"),
        bg="#e74c3c",
        fg="white",
        relief=tk.RAISED,
        borderwidth=2,
        padx=15,
        pady=12,
        cursor="hand2",
        state=tk.DISABLED
    )
    stop_button.pack(fill=tk.X, pady=6)
    
    # 状态
    status_frame = tk.Frame(scrollable_frame, bg="white")
    status_frame.pack(fill=tk.X, padx=10, pady=10)
    
    status_label = tk.Label(
        status_frame,
        text="⚪ 就绪",
        font=("微软雅黑", 11, "bold"),
        bg="white",
        fg="#95a5a6"
    )
    status_label.pack(fill=tk.X, pady=5)
    
    # 右侧：视频和日志
    right_frame = tk.Frame(main_frame, bg="#f0f0f0")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # 视频面板
    video_frame = tk.LabelFrame(
        right_frame,
        text="📹 实时视频",
        font=("微软雅黑", 12, "bold"),
        bg="white",
        padx=10,
        pady=10
    )
    video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
    
    video_label = tk.Label(video_frame, bg="black", text="摄像头画面显示区域", fg="white")
    video_label.pack(fill=tk.BOTH, expand=True)
    
    # 日志面板
    log_frame = tk.LabelFrame(
        right_frame,
        text="📋 检测日志",
        font=("微软雅黑", 12, "bold"),
        bg="white",
        padx=10,
        pady=10,
        height=150
    )
    log_frame.pack(fill=tk.BOTH, expand=False)
    log_frame.pack_propagate(False)  # 固定高度
    
    log_text = tk.Text(log_frame, height=8, font=("Consolas", 10), bg="#2c3e50", fg="#ecf0f1")
    log_text.pack(fill=tk.BOTH, expand=True)
    log_text.insert(tk.END, "系统已启动\n提示：点击左侧【▶️ 启动检测】按钮开始使用\n")
    log_text.config(state=tk.DISABLED)
    
    root.mainloop()


if __name__ == "__main__":
    print("=" * 60)
    print("GUI 布局预览")
    print("=" * 60)
    print("\n点击窗口看你能否清楚地看到：")
    print("  ✓ 【▶️ 启动检测】 按钮 (绿色)")
    print("  ✓ 【⏹️ 停止检测】 按钮 (红色，初始禁用)")
    print("\n如果你能看到这两个明显的按钮，说明布局已修复！")
    print("\n" + "=" * 60 + "\n")
    
    preview_gui()
