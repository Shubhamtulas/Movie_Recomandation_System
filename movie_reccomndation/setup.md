# Quick Setup Guide

## 🚀 Your Movie Recommendation System is Ready!

The app is now running successfully! Here's what you need to know:

### ✅ Current Status
- ✅ All dependencies installed
- ✅ App running on http://localhost:8501
- ✅ Movie data loaded successfully
- ⚠️ TMDB API key needed for movie posters

### 🎯 Next Steps

#### 1. **Get TMDB API Key (Optional but Recommended)**
- Visit: https://www.themoviedb.org/settings/api
- Create account and request API key
- Create `.env` file in the app directory:
  ```
  TMDB_API_KEY=your_actual_api_key_here
  ```

#### 2. **Test the App**
- Open your browser to: http://localhost:8501
- Select a movie from the dropdown
- Click "Get Recommendations"
- The app will work with or without the API key!

#### 3. **Debug Mode**
- Check the "🔧 Debug Mode" checkbox in the sidebar
- Test API connectivity if you have an API key
- View system information

### 🌐 Deployment Options

#### **Option 1: Streamlit Cloud (Easiest)**
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repository
4. Set `TMDB_API_KEY` in environment variables
5. Deploy!

#### **Option 2: Hugging Face Spaces**
1. Create new Space on Hugging Face
2. Choose Streamlit SDK
3. Upload files
4. Set `TMDB_API_KEY` secret

#### **Option 3: Heroku**
1. Use the provided `Procfile`
2. Set environment variables in Heroku dashboard
3. Deploy with Heroku CLI

### 🔧 Troubleshooting

- **App not loading**: Check if port 8501 is available
- **No recommendations**: Ensure `movie_data.pkl` is in the same directory
- **No posters**: Set up TMDB API key in `.env` file
- **Import errors**: Run `pip install -r requirements.txt`

### 📁 File Structure
```
movie_reccomndation/
├── app.py              # Main application
├── movie_data.pkl      # Pre-processed movie data
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment
├── runtime.txt        # Python version
├── README.md          # Documentation
└── .env               # API keys (create this)
```

### 🎉 You're All Set!
Your movie recommendation system is working! The app will show beautiful fallback cards even without the TMDB API key, and full movie posters when you add the API key.

Happy recommending! 🎬
