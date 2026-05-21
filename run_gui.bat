@echo off
chcp 65001 > nul
echo ========================================
echo   智能障碍物检测系统 - Tkinter GUI
echo ========================================
echo.
echo [启动] 正在启动桌面应用...
echo.

cd /d "%~dp0"

REM 检查虚拟环境
if not exist ".venv\Scripts\python.exe" (
    echo 错误: 虚拟环境不存在
    echo 请先运行: uv sync
    pause
    exit /b 1
)

REM 用正确的环境启动
.venv\Scripts\python.exe ui/gui_app.py

if errorlevel 1 (
    echo.
    echo [错误] GUI 启动失败
    echo.
    pause
    exit /b 1
)
