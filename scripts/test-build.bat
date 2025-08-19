@echo off
REM Comprehensive build and test script for Bryan Howard Website
REM Tests all functionality before deployment

echo.
echo ===============================================
echo     Bryan Howard Website - Build Test
echo ===============================================
echo.

REM Activate virtual environment
echo [1/7] Activating virtual environment...
call pelican-env\Scripts\activate.bat
if errorlevel 1 goto :error

echo [2/7] Checking Pelican configuration...
python -c "import pelicanconf; print('Configuration loaded successfully')"
if errorlevel 1 goto :error

echo [3/7] Running clean build...
pelican content -s pelicanconf.py --delete-output-directory
if errorlevel 1 goto :error

echo [4/7] Testing local server...
start /b pelican --listen --port 8000 --bind 127.0.0.1
timeout /t 3 /nobreak > nul

echo [5/7] Running basic site tests...
python -c "
import requests
import sys
try:
    response = requests.get('http://localhost:8000', timeout=5)
    if response.status_code == 200:
        print('✓ Site is accessible')
        if 'Bryan Howard' in response.text:
            print('✓ Site content loaded')
        else:
            print('✗ Site content missing')
            sys.exit(1)
    else:
        print(f'✗ Site returned status {response.status_code}')
        sys.exit(1)
except Exception as e:
    print(f'✗ Site test failed: {e}')
    sys.exit(1)
"
if errorlevel 1 goto :error

echo [6/7] Checking file structure...
if not exist "output\index.html" (
    echo ✗ index.html not found
    goto :error
)
if not exist "output\theme\css\base.css" (
    echo ✗ CSS files not found
    goto :error
)
if not exist "output\theme\js\main.js" (
    echo ✗ JavaScript files not found
    goto :error
)
echo ✓ File structure looks good

echo [7/7] Stopping test server...
taskkill /f /im pelican.exe 2>nul
taskkill /f /im python.exe /fi "WINDOWTITLE eq *pelican*" 2>nul

echo.
echo ===============================================
echo          BUILD TEST COMPLETED ✓
echo ===============================================
echo.
echo Ready for deployment!
echo.
goto :end

:error
echo.
echo ===============================================
echo          BUILD TEST FAILED ✗
echo ===============================================
echo.
echo Please check the errors above and try again.
echo.
taskkill /f /im pelican.exe 2>nul
taskkill /f /im python.exe /fi "WINDOWTITLE eq *pelican*" 2>nul
exit /b 1

:end