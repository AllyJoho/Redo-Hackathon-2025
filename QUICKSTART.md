# Quick Start Guide

Get the BYU Major Advisor running in 5 minutes!

## Prerequisites

- Python 3.8+ (use `python3` command)
- Node.js 16+
- OpenAI API key (required for AI features)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/AllyJoho/Redo-Hackathon-2025.git
cd Redo-Hackathon-2025
```

### 2. Set Up Environment Variables
```bash
# Create .env file from the example
cp .env.example .env

# Edit .env and add your OpenAI API key
# The file should contain:
# OPENAI_API_KEY=sk-proj-your-actual-api-key-here
# FLASK_ENV=development
# PORT=5001
```

⚠️ **Important:** The app requires a valid OpenAI API key to function properly. Get one at https://platform.openai.com/api-keys

### 3. Install Backend Dependencies
```bash
pip3 install -r requirements.txt
```

This will install:
- Flask (3.0.0) - Web framework
- Flask-CORS (4.0.0) - Cross-origin resource sharing
- OpenAI (latest) - AI integration
- python-dotenv (1.0.0) - Environment variable management

### 4. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

## Running the Application

### Option 1: Full React Frontend (Recommended)

**Terminal 1 - Start Backend:**
```bash
python3 backend/app.py
```

You should see:
```
🚀 BYU Major Advisor API starting on port 5001
📚 Loaded 8 majors
✅ OpenAI integration enabled
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm start
```

Then open http://localhost:3000 in your browser

### Option 2: Simple Demo (HTML only)

```bash
# 1. Start the backend API
python3 backend/app.py

# 2. In another terminal, serve the demo
python3 -m http.server 8081

# 3. Open browser to http://localhost:8081/demo.html
```

### Option 3: Using the Start Script

```bash
# Make sure the script is executable
chmod +x start.sh

# Run both frontend and backend
./start.sh
```

## Using the Application

### First Steps

1. **Start a conversation**: Click on a suggested question or type your interests
2. **Explore majors**: Review the AI's recommendations with detailed information
3. **Generate schedule**: Click "Generate Schedule" to see an optimized first-year plan
4. **Keep exploring**: Ask follow-up questions to refine your major choice

### Example Questions

Try these to get started:
- "I love coding and solving complex problems"
- "I want to help people and work in healthcare"  
- "I'm interested in business and entrepreneurship"
- "Tell me about engineering majors at BYU"
- "What careers can I pursue with a psychology degree?"
- "I'm not sure what I want to do yet"

## Troubleshooting

### "Python command not found"
Use `python3` instead of `python`:
```bash
python3 backend/app.py
```

### "ModuleNotFoundError: No module named 'flask'"
Install dependencies:
```bash
pip3 install -r requirements.txt
```

### "Address already in use" (Port 5001)
Kill the existing process:
```bash
lsof -i :5001  # Find the process ID (PID)
kill -9 <PID>  # Replace <PID> with the actual process ID
```

Or change the port in `.env`:
```bash
PORT=5002  # Use any available port
```

### "TypeError: Client.__init__() got an unexpected keyword argument"
Update OpenAI library:
```bash
pip3 install --upgrade openai
```

### Agent says "Sorry, I encountered an error"
This usually means:
1. **Backend not running** - Check Terminal 1 for the backend server
2. **Missing API key** - Verify `.env` file exists with valid `OPENAI_API_KEY`
3. **Wrong port** - Backend should be on port 5001, frontend connects to http://localhost:5001/api
4. **Invalid API key** - Check your OpenAI API key is active and has credits

**Test the backend:**
```bash
curl http://localhost:5001/api/health
```

Should return:
```json
{"status":"healthy","service":"BYU Major Advisor API"}
```

### Frontend won't start
- Check Node version: `node --version` (need 16+)
- Clear npm cache: `npm cache clean --force`
- Reinstall: `cd frontend && rm -rf node_modules && npm install`

### CORS errors in browser console
Make sure:
1. Backend is running on port 5001
2. Flask-CORS is installed: `pip3 install flask-cors`
3. Both frontend and backend are running

## Verification Checklist

Before asking questions, make sure:
- ✅ `.env` file exists with valid OpenAI API key
- ✅ Backend running on port 5001 (check Terminal 1)
- ✅ Frontend running on port 3000 (check Terminal 2)
- ✅ Browser shows the application at http://localhost:3000
- ✅ No error messages in either terminal
- ✅ Health check passes: `curl http://localhost:5001/api/health`

## Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────┐
│  React Frontend │ ───────>│  Flask Backend   │ ───────>│   OpenAI    │
│   (Port 3000)   │         │   (Port 5001)    │         │     API     │
└─────────────────┘         └──────────────────┘         └─────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  majors.json     │
                            │  (8 BYU majors)  │
                            └──────────────────┘
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [API documentation](README.md#api-endpoints)
- Customize majors in `backend/data/majors.json`
- Check out [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Review [CONTRIBUTING.md](CONTRIBUTING.md) to add features

## Project Structure

```
Redo-Hackathon-2025/
├── backend/
│   ├── app.py              # Flask API server
│   ├── utils/
│   │   └── chatbot.py      # OpenAI integration
│   └── data/
│       └── majors.json     # BYU majors database
├── frontend/
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── components/     # UI components
│   │   └── services/
│   │       └── api.js      # API client (port 5001)
│   └── public/
├── .env                    # Your API keys (DO NOT COMMIT)
├── .env.example            # Template for .env
├── requirements.txt        # Python dependencies
└── package.json            # Node.js dependencies
```

## Support

Built for the BYU Homecoming 2025 Redo Hackathon by Team AMIRUS 🎓

**Need help?** Open an issue on GitHub or check the troubleshooting section above.
