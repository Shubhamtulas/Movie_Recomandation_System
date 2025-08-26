#!/usr/bin/env python3
"""
Start Movie Recommendation System on localhost
"""
import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("🎬 Movie Recommendation System - Localhost")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found!")
        print("Make sure you're running this from the movie_reccomndation directory")
        input("Press Enter to exit...")
        return
    
    print("✅ app.py found!")
    
    # Check if movie_data.pkl exists
    if not os.path.exists('movie_data.pkl'):
        print("❌ Error: movie_data.pkl not found!")
        print("This file is required for the app to work")
        input("Press Enter to exit...")
        return
    
    print("✅ movie_data.pkl found!")
    
    print("\n🚀 Starting the app on localhost...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("🌐 You can also access it at: http://127.0.0.1:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("=" * 60)
    
    try:
        # Start streamlit with localhost settings
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()

