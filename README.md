
  <h1>🎵 YouTube Liked Videos MP3 Downloader (Flask App)</h1>

  <p>This Flask app allows you to:</p>
  <ul>
    <li>Authenticate with your <strong>Google account</strong></li>
    <li>Access your <strong>YouTube "Liked Videos"</strong></li>
    <li>Save video titles to a CSV</li>
    <li>Download videos as <strong>MP3s</strong> into your Downloads folder</li>
  </ul>

  <h2>🚀 Features</h2>
  <ul>
    <li>🔐 OAuth 2.0 login with Google</li>
    <li>📄 Exports liked videos to <code>songs.csv</code></li>
    <li>🎧 Downloads each video as MP3</li>
    <li>📁 Files saved to <code>~/Downloads/songs/</code></li>
  </ul>

  <h2>🛠 Requirements</h2>
  <ul>
    <li>Python 3.8+</li>
    <li><code>ffmpeg</code> installed and accessible</li>
    <li>Google Cloud project with OAuth 2.0 credentials</li>
  </ul>

  <h2>📦 Setup Instructions</h2>

  <h3>1. Clone this repo</h3>
  <pre><code>git clone https://github.com/yourusername/youtube-mp3-downloader.git
cd youtube-mp3-downloader</code></pre>

  <h3>2. Install dependencies</h3>
  <pre><code>pip install -r requirements.txt</code></pre>

  <h3>3. Add <code>client_secrets.json</code></h3>
  <ol>
    <li>Go to <a href="https://console.cloud.google.com/apis/credentials" target="_blank">Google Cloud Console</a></li>
    <li>Create OAuth 2.0 credentials</li>
    <li>Add redirect URI: <code>http://127.0.0.1:5000/redirect</code></li>
    <li>Download the JSON, rename to <code>client_secrets.json</code>, and place in project root</li>
  </ol>

  <h3>4. Run the Flask app</h3>
  <pre><code>python app.py</code></pre>

  <p>Then open: <code>http://127.0.0.1:5000/</code></p>

  <h2>✅ What Happens After Login?</h2>
  <ol>
    <li>Fetches your liked videos</li>
    <li>Saves to <code>Downloads/songs.csv</code></li>
    <li>Uses <code>yt-dlp</code> to download MP3s</li>
    <li>Saves to: <code>~/Downloads/songs/</code></li>
  </ol>


  <h2>🧠 Credits</h2>
  <ul>
    <li>Flask – Web framework</li>
    <li>yt-dlp – YouTube downloader</li>
    <li>YouTube Data API – Liked video fetch</li>
    <li>pandas – CSV writing</li>
    <li>youtubesearchpython – Video search</li>
  </ul>

  <h2>⚠️ Legal</h2>
  <p>This tool is for <strong>educational and personal use only</strong>. Respect copyright laws and YouTube’s terms of service.</p>


</body>
</html>
