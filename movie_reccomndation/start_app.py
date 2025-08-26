#!/usr/bin/env python3
"""
Simple script to start the Movie Recommendation System
"""
import os
import sys
import subprocess
import time

def main():
    print("=" * 50)
    print("🎬 Movie Recommendation System")
    print("=" * 50)
    
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
    
    # Check if requirements are installed
    try:
        import streamlit
        print("✅ Streamlit is installed!")
    except ImportError:
        print("❌ Streamlit not installed!")
        print("Run: pip install -r requirements.txt")
        input("Press Enter to exit...")
        return
    
    print("\n🚀 Starting the app...")
    print("The app will open in your browser at: http://localhost:8501")
    print("Press Ctrl+C to stop the app")
    print("=" * 50)
    
    try:
        # Start streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "0.0.0.0",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
