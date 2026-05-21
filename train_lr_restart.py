#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重启学习率续训脚本
从 best.pt 开始，用中等学习率（0.003）训练 20 轮
"""
if __name__ == '__main__':
    from ultralytics import YOLO
    
    print("=" * 80)
    print("[重启学习率] 从 best.pt 开始，lr0=0.003，训练 50 轮（workers=0）")
    print("=" * 80)
    
    # 若已有中断进度，直接从 train_lr_restart/weights/last.pt 续训
    model = YOLO('runs/detect/train_lr_restart/weights/last.pt')

    model.train(
        data='data/auto_coco_merged.yaml',
        epochs=50,           # 目标总轮次
        batch=32,
        workers=0,           # Windows 避免多进程导致 pagefile/cufft64_11.dll 加载失败
        device=0,
        resume=True,         # 续训，保留当前优化器与学习率进度
        lr0=0.003,           # （仅首次有效）新学习率
        lrf=0.01,
        warmup_epochs=2,
        patience=50,
        save=True,
        exist_ok=True,       # 允许在同目录续写
        plots=True,
        project='runs/detect',
        name='train_lr_restart'
    )
    
    print("\n" + "=" * 80)
    print("[完成] 重启学习率训练结束")
    print("权重保存在：runs/detect/train_lr_restart/weights/")
    print("=" * 80)
