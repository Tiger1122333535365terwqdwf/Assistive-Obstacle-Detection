# 续训脚本：从 train_rest_lr005 的最佳权重继续训练20轮
# 执行时机：等第20轮完成后运行

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "准备继续训练 rest 数据集（额外20轮）" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 检查前一轮训练是否完成
$bestWeight = "runs\detect\train_rest_lr005\weights\best.pt"
if (-not (Test-Path $bestWeight)) {
    Write-Host "错误: 前一轮训练的 best.pt 不存在" -ForegroundColor Red
    Write-Host "请等待当前训练完成后再运行此脚本" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n使用权重: $bestWeight" -ForegroundColor Green
Write-Host "目标轮数: 20 (总计40轮)" -ForegroundColor Green
Write-Host "学习率: 0.005 (重新schedule)" -ForegroundColor Green
Write-Host "`n按任意键开始训练..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# 配置环境
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = 'utf-8'
$env:ULTRALYTICS_EMOJI = 'False'

# 启动训练
& "C:/Users/18875/Downloads/computer vision project/.venv/Scripts/python.exe" `
    scripts/train_yolo.py `
    --data data/auto_coco_rest.yaml `
    --model runs/detect/train_rest_lr005/weights/best.pt `
    --epochs 20 `
    --imgsz 640 `
    --batch 32 `
    --cache false `
    --workers 2 `
    --name train_rest_lr005_ext `
    --device 0 `
    --lr0 0.005 `
    --warmup_epochs 5 `
    --exist-ok `
    2>&1 | Tee-Object -FilePath training_log_rest_ext.txt

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "续训完成！" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "最佳模型: runs\detect\train_rest_lr005_ext\weights\best.pt" -ForegroundColor Green
Write-Host "日志文件: training_log_rest_ext.txt" -ForegroundColor Green
