@echo off
REM Anonymous Chat Bot - Quick Setup Script (Windows)

echo ==========================================
echo   Anonymous Chat Bot - Quick Setup
echo ==========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

python --version
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)
echo √ Dependencies installed
echo.

REM Check .env file
if not exist .env (
    echo ! .env file not found
    echo.
    echo Would you like to run the setup wizard? (Y/N^)
    set /p response=
    if /i "%response%"=="Y" (
        python setup.py
    ) else (
        echo.
        echo Please create a .env file manually using .env.example as a template
        echo Then run: python bot.py
        pause
        exit /b 0
    )
) else (
    echo √ .env file found
)
echo.

REM Run tests
echo Running tests...
python test.py
if errorlevel 1 (
    echo.
    echo ! Some tests failed. Please check the output above.
    echo.
    echo You can still try to run the bot with: python bot.py
    pause
    exit /b 0
)

echo.
echo ==========================================
echo   √ Setup Complete!
echo ==========================================
echo.
echo Your bot is ready to run!
echo.
echo To start the bot, run:
echo   python bot.py
echo.
echo Or run this script with 'start' argument:
echo   quicksetup.bat start
echo.

if "%1"=="start" (
    echo Starting the bot...
    echo.
    python bot.py
) else (
    pause
)
