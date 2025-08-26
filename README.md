# Movie Recommendation System

A beautiful movie recommendation system built with Streamlit that suggests similar movies based on content-based filtering.

## Features

- 🎬 Content-based movie recommendations
- 🖼️ Movie posters from TMDB API
- 🎨 Beautiful UI with responsive design
- 🔧 Debug mode for troubleshooting
- 📱 Mobile-friendly interface

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get TMDB API Key

1. Go to [TMDB](https://www.themoviedb.org/settings/api)
2. Create an account and request an API key
3. Copy your API key

### 3. Set Environment Variables

Create a `.env` file in the project directory:

```bash
# Create .env file
echo "TMDB_API_KEY=your_actual_api_key_here" > .env
```

Replace `your_actual_api_key_here` with your TMDB API key.

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Local Development

- **Debug Mode**: Check the "🔧 Debug Mode" checkbox in the sidebar to test API connectivity
- **Data Files**: Ensure `movie_data.pkl` is in the same directory as `app.py`

## Deployment

### Option 1: Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set the environment variable `TMDB_API_KEY` in the Streamlit Cloud dashboard
5. Deploy!

### Option 2: Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Choose Streamlit as the SDK
3. Upload your files
4. Set the `TMDB_API_KEY` secret in the Space settings

### Option 3: Heroku

1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Set environment variables in Heroku dashboard
3. Deploy using Heroku CLI

## Troubleshooting

- **"movie_data.pkl file not found"**: Ensure the pickle file is in the same directory as app.py
- **"API Key: None"**: Check your .env file and TMDB API key
- **No posters showing**: Verify your TMDB API key is valid and has proper permissions

## Data Sources

- Movie data: TMDB 5000 Movies Dataset
- Posters: TMDB API
- Similarity matrix: Pre-computed using cosine similarity

---

*Powered by TMDB API and Streamlit*
