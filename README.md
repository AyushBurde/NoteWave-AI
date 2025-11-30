NoteWave-AI - A meeting assistant for Indians 
💡 The Problem
Every remote team faces this:

😰 Someone forgets to record the meeting
📝 Nobody wants to take notes during discussions
🤦‍♂️ Existing tools butcher Indian names and accents
💸 Premium tools like Otter.ai are expensive
🗣️ They don't understand Hinglish (Hindi + English mix)

Real scenario:

"Rajesh ji, can you send the updated report to Priya by Friday? And Amit will coordinate with the Mumbai team, theek hai?"

Otter.ai transcribes:

"Roger G can you send the updated report to free by Friday and I meet will coordinate with the mom by team take high"

IndianMeet AI transcribes:

"Rajesh ji, can you send the updated report to Priya by Friday? And Amit will coordinate with the Mumbai team, theek hai?"

✨ Our Solution
NoteWave-AI is a meeting assistant specifically trained for Indian business contexts. It:
✅ Understands Indian English accents (Mumbai, Delhi, Bangalore, Hyderabad)
✅ Recognizes Hinglish (Hindi words mixed with English)
✅ Gets Indian names right (Rajesh, Priya, Amit, Sneha, Arjun)
✅ Completely FREE to use
✅ Privacy-first (your data, your control)
Features
🎙️ Real-Time Recording

One-click recording directly in browser
No need to remember to hit record
Live audio visualization

📤 Upload Past Meetings

Supports MP3, WAV, M4A, WebM
Up to 25MB file size
Batch processing ready

🤖 AI-Powered Processing

Smart meeting summaries
Action items with assigned owners
Participant identification
Key decisions tracking

📊 Export Options

Download as PDF
Export as text file
Copy to clipboard

🔌 Chrome Extension (Beta)

Auto-capture Google Meet/Zoom calls
No manual intervention needed
Instant post-meeting summaries

🚀 Tech Stack
Frontend

HTML5/CSS3/JavaScript - Clean, responsive UI
Vanilla JS - No framework bloat, fast loading
Web Audio API - Real-time recording
Modern CSS - Gradient backgrounds, animations

Backend

FastAPI - High-performance Python backend
Deepgram API - Speech-to-text (free tier: 45K min/month)
Groq + Llama 3.3 - AI processing (free, unlimited)
Python 3.9+ - Core logic

Chrome Extension

Manifest V3 - Latest Chrome extension format
Content Scripts - Inject into Google Meet/Zoom
Background Service - Handle audio capture

📦 Installation
Prerequisites

Python 3.9 or higher
pip package manager
Modern web browser

# 1. Clone the repository
git clone https://github.com/yourusername/NoteWave-ai.git
cd NoteWave-ai

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Set up environment variables
# Create .env file in root directory
# Add your API keys:
DEEPGRAM_API_KEY=your_deepgram_key_here
GROQ_API_KEY=your_groq_key_here

# 5. Start backend
cd backend
python main.py
# Backend runs on http://localhost:8000

# 6. Start frontend (new terminal)
cd frontend
python -m http.server 3000
# Frontend runs on http://localhost:3000

Get Free API Keys
Deepgram (Speech-to-Text)

Sign up: https://console.deepgram.com/signup
Get API key from dashboard
Free tier: 45,000 minutes/month

Groq (AI Processing)

Sign up: https://console.groq.com/
Create API key
Free tier: Unlimited requests (rate limited)

PROJECT STRUCTURE
indianmeet-ai/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── transcription.py     # Deepgram integration
│   ├── processing.py        # Groq AI processing
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Main UI
│   ├── style.css            # Styling
│   └── script.js            # Frontend logic
├── chrome-extension/
│   ├── manifest.json        # Extension config
│   ├── popup.html           # Extension popup
│   ├── popup.js             # Popup logic
│   └── content.js           # Inject into Meet/Zoom
├── uploads/                 # Temp audio storage
├── .env                     # API keys (not in repo)
└── README.md

👥 Team
Built with ❤️ for Hack This Fall 2025 - Milestone Edition
Developer: [Ayush Burde]
Contact: [workayu01@gmail.com]
GitHub: [github.com/AyushBurde]
LinkedIn: [https://www.linkedin.com/in/ayush-burde1/]

