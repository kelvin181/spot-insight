<h1 align="center">Welcome to SpotInsight</h1>
<p>
</p>

> This is an application that connects with Spotify to provide users with their listening habits and data.

## Features

- **Top Played Tracks Analysis:**
  - View your top played tracks over different periods of time.
  
- **Playlist Exploration:**
  - Explore the songs within your playlists.

## Install

### Step 1: Set Up Environment
Ensure you have Python installed on your machine.

### Step 2: Clone the Repository
```sh
git clone https://github.com/kelvin181/SpotInsight.git
cd your-repository
```

### Step 3: Install Dependencies
```sh
pip install -r requirements.txt
```

### Step 4: Set Up Spotify API Credentials
Create a Spotify Developer account and register a new application to obtain your `CLIENT_ID`, `CLIENT_SECRET`, and set `REDIRECT_URI` in your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) to "http://localhost:5000/callback".

Create a `.env` file in the project root directory and add your Spotify API credentials:

```env
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REDIRECT_URI="http://localhost:5000/callback"
Replace your_client_id and your_client_secret with the corresponding values from your Spotify Developer Dashboard. Keep this information confidential and do not share it publicly.
```

### Step 5: Run the Application
```sh
python main.py
```

### Step 6: Access the Application
Open your web browser and navigate to http://localhost:5000/ to access the SpotInsight application.

### Note:
The application uses Flask as a web framework, so make sure to have it installed using the pip install Flask command if you don't have it already.

## Author

**Kelvin Chen**

* Github: [@kelvin181](https://github.com/kelvin181)
<<<<<<< HEAD
* LinkedIn: [@Kelvin Chen](https://linkedin.com/in/kelvin-chen8)
=======
* LinkedIn: [@kelvin-chen8](https://linkedin.com/in/kelvin-chen-7a5444279)
>>>>>>> e8ca48bce5124ce833d025d0a489eff067966b33
