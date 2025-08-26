@echo off
echo ========================================
echo Movie Recommendation System - Localhost
echo ========================================
echo.
echo Starting app on localhost...
echo The app will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo ========================================
streamlit run app.py --server.address localhost --server.port 8501
pause

