#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从现有最优权重继续训练 40 轮。
- 数据：data/auto_coco_merged.yaml
- 预训练权重：runs/detect/train_lr_restart/weights/best.pt（可按需替换）
- 输出目录：runs/detect/train_40ep_new
"""
import os
import multiprocessing
from pathlib import Path
from ultralytics import YOLO

if __name__ == "__main__":
    multiprocessing.freeze_support()
    os.chdir(r"d:\computer vision project")

    project = "runs/detect"
    name = "train_40ep_new"
    weights_path = Path("runs/detect/train_lr_restart/weights/best.pt")
    data_yaml = "data/auto_coco_merged.yaml"

    if not weights_path.exists():
        raise FileNotFoundError(f"预训练权重不存在: {weights_path}")

    print("=" * 80)
    print(f"[启动训练] {name}")
    print(f"权重: {weights_path}")
    print(f"数据: {data_yaml}")
    print("=" * 80)

    model = YOLO(str(weights_path))

    model.train(
        data=data_yaml,
        epochs=40,
        batch=32,
        device=0,
        workers=0,          # Windows 下多进程可能触发页面文件错误，使用单进程更稳
        resume=False,
        patience=50,
        save=True,
        exist_ok=True,
        plots=True,
        project=project,
        name=name,
    )

    print("\n" + "=" * 80)
    print("[完成] 40 轮训练结束")
    print(f"输出目录: {project}/{name}")
    print("=" * 80)
