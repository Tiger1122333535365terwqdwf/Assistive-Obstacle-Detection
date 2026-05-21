@echo off
chcp 65001 > nul
echo ========================================
echo   智能障碍物检测系统 - Web UI
echo ========================================
echo.
echo [启动] 正在启动 Web 服务器...
echo [信息] 启动后请在浏览器访问: http://localhost:7860
echo.
echo [提示] 按 Ctrl+C 停止服务器
echo ========================================
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
.venv\Scripts\python.exe ui/web_app.py

pause
