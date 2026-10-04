@echo off
echo ===============================================
echo    BUILD AUTOMATIC OPERATION TO EXE
echo ===============================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    echo Vui long cai dat Python tu: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Cai dat cac thu vien can thiet...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo [2/3] Build file EXE (GUI)...
pyinstaller --onefile --noconsole --icon=NONE ^
    --add-data "config.json;." ^
    --name AutomaticOperation ^
    AutomaticOperation_GUI.py

echo.
echo [3/3] Hoan thanh!
echo.
echo ===============================================
echo File EXE: dist\AutomaticOperation.exe
echo ===============================================
echo.
pause
