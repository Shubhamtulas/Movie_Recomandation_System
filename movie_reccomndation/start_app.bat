@echo off
echo ========================================
echo Starting Movie Recommendation System
echo ========================================
echo.
echo Make sure you're in the correct directory...
cd /d "%~dp0"
echo Current directory: %CD%
echo.
echo Checking if app.py exists...
if exist app.py (
    echo ✅ app.py found!
) else (
    echo ❌ app.py not found!
    pause
    exit /b 1
)
echo.
echo Starting Streamlit app...
echo The app will open in your browser at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo ========================================
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
pause
