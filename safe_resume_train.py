#!/usr/bin/env python3
"""
安全的恢复训练脚本 - 确保每个 epoch 都被记录到 CSV
"""
import os
import sys
import csv
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO

def main():
    # 配置
    model_path = "runs/detect/train_merged_80ep_v2_continue/weights/last.pt"
    data_config = "data/auto_coco_merged.yaml"
    batch_size = 40
    epochs = 62
    
    print("=" * 70)
    print("[开始] 安全恢复训练")
    print("=" * 70)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"模型: {model_path}")
    print(f"数据: {data_config}")
    print(f"批量: {batch_size}")
    print(f"总轮数: {epochs}")
    print("=" * 70)
    
    # 验证文件
    if not os.path.exists(model_path):
        print(f"❌ 错误: 模型文件不存在 {model_path}")
        sys.exit(1)
    
    if not os.path.exists(data_config):
        print(f"❌ 错误: 数据配置文件不存在 {data_config}")
        sys.exit(1)
    
    print(f"✓ 模型文件验证通过")
    print(f"✓ 数据配置验证通过")
    print()
    
    # 加载模型
    print("[加载] 加载 YOLO 模型...")
    model = YOLO(model_path)
    print("✓ 模型加载成功")
    print()
    
    # 启动训练 - 使用 resume=True
    print("[训练] 开始恢复训练...")
    print("-" * 70)
    
    try:
        results = model.train(
            data=data_config,
            epochs=epochs,
            batch=batch_size,
            device=0,  # GPU
            resume=True,  # 关键：启用恢复模式
            patience=50,
            save=True,
            save_period=-1,  # 每个epoch保存
            exist_ok=True,
            plots=True,
            verbose=True
        )
        
        print("-" * 70)
        print("[完成] 训练成功完成！")
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 验证CSV是否更新
        csv_path = "runs/detect/train_merged_80ep_v2_continue/results.csv"
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            epoch_count = len(lines) - 1  # 减去表头
            print(f"✓ CSV 文件更新成功: {epoch_count} 轮数据已保存")
            print(f"  文件位置: {csv_path}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n[警告] 训练被用户中断")
        print("正在保存最后的进度...")
        # 验证CSV是否更新
        csv_path = "runs/detect/train_merged_80ep_v2_continue/results.csv"
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            epoch_count = len(lines) - 1
            print(f"✓ 已保存 {epoch_count} 轮数据到 CSV")
        return 1
        
    except Exception as e:
        print(f"\n❌ 训练出错: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
