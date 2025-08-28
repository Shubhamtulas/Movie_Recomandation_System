import streamlit as st
import pandas as pd
import requests
import pickle
import os
import time
from pathlib import Path
from dotenv import load_dotenv

# Resolve base directory to the folder of this file (works on Streamlit Cloud)
BASE_DIR = Path(__file__).parent.resolve()

# Load environment variables from a local .env if present (optional locally)
load_dotenv(BASE_DIR / ".env")

# Helper: load TMDB API key from Streamlit secrets or environment
def get_tmdb_api_key():
    """Get TMDB API key from secrets or environment variables"""
    try:
        # First try Streamlit secrets (for hosted environments)
        if hasattr(st, "secrets") and "TMDB_API_KEY" in st.secrets:
            return st.secrets["TMDB_API_KEY"]
    except Exception:
        pass
    
    # Fallback to environment variables or .env file
    return os.getenv("TMDB_API_KEY")

# Check for API key and show setup instructions if missing
api_key = get_tmdb_api_key()
if not api_key:
    st.warning("⚠️ **TMDB API Key Not Found**")
    st.markdown("""
    To enable movie posters, you need to set up a TMDB API key:
    
    1. **Get API Key**: Visit [TMDB Settings](https://www.themoviedb.org/settings/api) and request an API key
    2. **Create .env file**: Add `TMDB_API_KEY=your_key_here` to a `.env` file in this directory
    3. **Restart the app**: The app will work without posters until you set up the API key
    
    The app will still work for recommendations, but without movie posters.
    """)
    st.markdown("---")

# Debug section - test API connectivity
with st.sidebar:
    if st.checkbox("🔧 Debug Mode"):
        st.header("Debug Information")
        key_preview = api_key[:10] + '...' if api_key else 'None'
        key_source = "env"
        try:
            if hasattr(st, "secrets"):
                try:
                    secret_val = st.secrets["TMDB_API_KEY"]
                    if secret_val:
                        key_source = "secrets"
                except Exception:
                    pass
        except Exception:
            pass
        st.write(f"API Key: {key_preview} (source: {key_source})")
        
        if api_key and st.button("Test API Connection"):
            try:
                test_url = "https://api.themoviedb.org/3/movie/19995"
                st.info("🔄 Testing connection to TMDB API...")
                response = requests.get(f"{test_url}?api_key={api_key}", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    poster_path = data.get('poster_path')
                    if poster_path:
                        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                        st.success("✅ API Connection Successful!")
                        st.write(f"Movie: {data.get('title')}")
                        st.write(f"Poster Path: {poster_path}")
                        st.image(poster_url, width=100)
                    else:
                        st.warning("⚠️ No poster path found")
                else:
                    st.error(f"❌ API Error: {response.status_code}")
            except requests.exceptions.Timeout:
                st.error("❌ Connection Timeout: The request to TMDB API timed out. This might be due to network issues or firewall settings.")
                st.info("💡 Try again later or check your internet connection.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Unable to connect to TMDB API. Check your internet connection.")
                st.info("💡 This might be due to network restrictions or firewall settings.")
            except Exception as e:
                st.error(f"❌ Unexpected Error: {str(e)}")
                st.info("💡 The app will still work without movie posters.")
        elif not api_key:
            st.error("❌ No API key configured")

# Load the processed data and similarity matrix
try:
    data_path = BASE_DIR / 'movie_data.pkl'
    with open(data_path, 'rb') as file:
        movies, cosine_sim = pickle.load(file)
except FileNotFoundError:
    st.error("movie_data.pkl file not found. Please ensure the file exists in the current directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading movie data: {str(e)}")
    st.stop()

# Function to get movie recommendations (optimized for speed)
def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        # Find the movie index (optimized search)
        movie_indices = movies[movies['title'] == title].index
        if len(movie_indices) == 0:
            return None
        
        idx = movie_indices[0]
        # Get similarity scores and sort efficiently
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Get top 10 similar movies
        movie_indices = [i[0] for i in sim_scores]
        
        # Return only necessary columns for better performance
        result = movies[['title', 'movie_id']].iloc[movie_indices].copy()
        return result
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return None

# Fetch movie poster from TMDB API with better error handling and debugging
def fetch_poster(movie_id):
    api_key = get_tmdb_api_key()
    if not api_key:
        return None
    
    try:
        # Use the movie_id directly since it's already the TMDB ID
        movie_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
        # Add shorter timeout and better error handling
        movie_response = requests.get(movie_url, timeout=10)
        
        if movie_response.status_code != 200:
            return None
            
        movie_data = movie_response.json()
        
        # Check if we got an error response from TMDB
        if 'status_code' in movie_data and movie_data['status_code'] != 200:
            return None
        
        poster_path = movie_data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_path
        
        return None
        
    except requests.exceptions.Timeout:
        # Handle timeout specifically
        return None
    except requests.exceptions.ConnectionError:
        # Handle connection errors
        return None
    except Exception:
        # Silent fail to avoid spam errors
        return None

# Batch fetch posters for multiple movies
def fetch_posters_batch(movie_ids, max_batch_size=2):
    """Fetch posters for multiple movies in batches to avoid rate limiting"""
    posters = {}
    api_key = get_tmdb_api_key()
    
    if not api_key:
        return posters
    
    # Process in smaller batches with better error handling
    for i in range(0, len(movie_ids), max_batch_size):
        batch = movie_ids[i:i + max_batch_size]
        
        for movie_id in batch:
            try:
                poster_url = fetch_poster(movie_id)
                if poster_url:
                    posters[movie_id] = poster_url
                # Small delay to avoid rate limiting
                import time
                time.sleep(0.3)  # Reduced delay for faster performance
            except Exception:
                continue
    
    return posters

# Function to create a beautiful movie card with fallback
def create_movie_card(movie_title, movie_id, poster_url=None):
    if poster_url:
        # Display with poster
        try:
            st.image(poster_url, caption=movie_title, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to display image: {str(e)}")
            create_fallback_card(movie_title, movie_id)
    else:
        # Create a beautiful fallback card
        create_fallback_card(movie_title, movie_id)

def create_fallback_card(movie_title, movie_id):
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin: 10px 0;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 2px solid rgba(255,255,255,0.1);
    ">
        <div style="font-size: 3rem; margin-bottom: 10px;">🎬</div>
        <div style="font-size: 0.9rem; font-weight: bold; line-height: 1.3; margin-bottom: 5px;">
            {movie_title}
        </div>
        <div style="font-size: 0.7rem; opacity: 0.8;">
            ID: {movie_id}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Streamlit UI
st.title("Movie Recommendation System")
st.markdown("---")

# Add some styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .movie-card {
        padding: 1rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Movie selection
selected_movie = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values,
    index=0,
    help="Choose a movie from the dropdown to see similar recommendations"
)

if st.button('🎯 Get Recommendations', type='primary'):
    if selected_movie:
        # Show progress for recommendations
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Finding similar movies...")
        progress_bar.progress(25)
        
        recommendations = get_recommendations(selected_movie)
        progress_bar.progress(50)
        
        if recommendations is not None and len(recommendations) > 0:
            status_text.text("Processing recommendations...")
            progress_bar.progress(75)
            
            st.success(f"Found {len(recommendations)} recommendations for '{selected_movie}'")
            st.markdown("---")
            
            # Extract movie IDs for batch poster fetching
            movie_ids = recommendations['movie_id'].tolist()
            
            # Fetch all posters in batch (only if API key is available)
            if api_key:
                status_text.text("Fetching movie posters...")
                progress_bar.progress(85)
                
                # Add option to skip poster fetching for faster performance
                if st.checkbox("🚀 Fast Mode (Skip posters for faster loading)", value=False):
                    st.info("⚡ Fast mode enabled - skipping poster fetch")
                    posters = {}
                else:
                    with st.spinner("Connecting to TMDB API..."):
                        posters = fetch_posters_batch(movie_ids, max_batch_size=2)
                    
                    # Show poster fetch results
                    if posters:
                        st.success(f"✅ Successfully fetched {len(posters)}/{len(movie_ids)} posters")
                    else:
                        st.warning("⚠️ No posters could be fetched due to network issues.")
                        st.info("💡 The app will display beautiful fallback cards instead.")
            else:
                st.info("ℹ️ Skipping poster fetch - no TMDB API key configured")
                posters = {}
            
            progress_bar.progress(100)
            status_text.text("Complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            st.markdown("---")
            
            # Create a responsive grid layout
            cols_per_row = 5
            for i in range(0, len(recommendations), cols_per_row):
                row_movies = recommendations.iloc[i:i+cols_per_row]
                cols = st.columns(cols_per_row)
                
                for col_idx, (_, movie) in enumerate(row_movies.iterrows()):
                    with cols[col_idx]:
                        movie_title = movie['title']
                        movie_id = movie['movie_id']
                        
                        # Get poster URL from batch results
                        poster_url = posters.get(movie_id)
                        
                        create_movie_card(movie_title, movie_id, poster_url)
            
            # Show final status
            if posters:
                st.success(f"🎬 Displayed {len(recommendations)} movie recommendations with {len(posters)} posters")
            else:
                st.info("All movies are displayed with beautiful fallback cards")
        else:
            st.error("No recommendations found for the selected movie.")
    else:
        st.warning("Please select a movie first.")

# Add footer
st.markdown("---")
st.markdown("*Powered by TMDB API and Streamlit*")
