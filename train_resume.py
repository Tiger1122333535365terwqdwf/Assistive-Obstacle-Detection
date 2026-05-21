#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接的恢复训练脚本
"""
import os
import sys
from ultralytics import YOLO

if __name__ == '__main__':
    os.chdir("d:\\computer vision project")

    print("=" * 80)
    print("[START] 恢复训练 - train_merged_80ep_v3 (从第 48 轮继续)")
    print("=" * 80)

    model = YOLO("runs/detect/train_merged_80ep_v3/weights/last.pt")

    print("\n[INFO] 开始训练...")
    results = model.train(
        data="data/auto_coco_merged.yaml",
        epochs=57,
        batch=32,
        workers=6,        # 折中配置
        device=0,
        resume=True,      # 从第 48 轮继续，CSV 会追加
        patience=50,
        save=True,
        exist_ok=True,
        plots=True,
        project='runs/detect',
        name='train_merged_80ep_v3'
    )

    print("\n" + "=" * 80)
    print("[SUCCESS] 训练完成")
    print("=" * 80)

    # 验证 CSV
    import csv
    csv_file = "runs/detect/train_merged_80ep_v3/results.csv"
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            rows = len([line for line in f]) - 1
        print(f"✓ CSV 文件: {csv_file}")
        print(f"✓ 训练轮数: {rows}")
