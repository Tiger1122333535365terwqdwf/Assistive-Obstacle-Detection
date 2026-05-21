#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建新训练目录 train_merged_80ep_v3，继承前5轮数据，继续训练57轮
"""
import os
import shutil
from pathlib import Path
from ultralytics import YOLO
import multiprocessing

# 必须保护主程序
if __name__ == '__main__':
    multiprocessing.freeze_support()
    os.chdir("d:\\computer vision project")

    print("=" * 80)
    print("[STEP 1] 准备新训练目录: train_merged_80ep_v3")
    print("=" * 80)

    # 源目录和目标目录
    source_dir = Path("runs/detect/train_merged_80ep_v2_continue")
    target_dir = Path("runs/detect/train_merged_80ep_v3")

    # 创建目标目录（如果不存在）
    target_dir.mkdir(parents=True, exist_ok=True)
    weights_dir = target_dir / "weights"
    weights_dir.mkdir(exist_ok=True)

    print(f"✓ 目录结构已准备: {target_dir}")

    # 复制前5轮的 results.csv 数据
    print("\n[STEP 2] 继承前5轮的数据...")
    source_csv = source_dir / "results.csv"
    target_csv = target_dir / "results.csv"

    if source_csv.exists():
        shutil.copy(source_csv, target_csv)
        with open(target_csv, 'r') as f:
            lines = f.readlines()
        epoch_count = len(lines) - 1
        print(f"✓ 已复制 results.csv (包含 {epoch_count} 轮数据)")
    else:
        print(f"✗ 警告: 找不到源 CSV 文件")

    # 复制权重文件
    print("\n[STEP 3] 复制权重文件...")
    source_pt = source_dir / "weights" / "last.pt"
    target_pt = weights_dir / "last.pt"

    if source_pt.exists():
        shutil.copy(source_pt, target_pt)
        print(f"✓ 已复制 last.pt ({target_pt})")
    else:
        print(f"✗ 错误: 找不到权重文件")
        exit(1)

    # 复制其他配置文件
    print("\n[STEP 4] 复制配置文件...")
    for file_pattern in ["args.yaml", "labels.jpg", "*.jpg"]:
        source_files = source_dir.glob(file_pattern)
        for src_file in source_files:
            if src_file.is_file() and src_file.name != "results.csv":
                dst_file = target_dir / src_file.name
                shutil.copy(src_file, dst_file)
                print(f"  ✓ {src_file.name}")

    print("\n" + "=" * 80)
    print("[STEP 5] 开始训练: 57 轮 (epoch 6-62)")
    print("=" * 80)

    # 使用复制的权重进行新训练
    model = YOLO(str(target_pt))

    print("\n[INFO] 启动训练...")
    results = model.train(
        data="data/auto_coco_merged.yaml",
        epochs=57,  # 只训练 57 轮，加上继承的 5 轮 = 总共 62 轮
        batch=32,
        device=0,
        resume=True,  # 启用 resume，保留进度
        patience=50,
        save=True,
        exist_ok=True,
        plots=True,
        project="runs/detect",
        name="train_merged_80ep_v3"
    )

    print("\n" + "=" * 80)
    print("[SUCCESS] 训练完成!")
    print("=" * 80)

    # 验证最终结果
    final_csv = Path("runs/detect/train_merged_80ep_v3/results.csv")
    if final_csv.exists():
        with open(final_csv, 'r') as f:
            final_lines = f.readlines()
        final_epochs = len(final_lines) - 1
        print(f"\n✓ 最终数据统计:")
        print(f"  训练目录: runs/detect/train_merged_80ep_v3")
        print(f"  总轮数: {final_epochs}")
        print(f"  CSV 文件: {final_csv}")
    else:
        print(f"\n✗ 错误: 找不到最终的 results.csv")
