# Quick Start Guide

Get the BYU Major Advisor running in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/AllyJoho/Redo-Hackathon-2025.git
cd Redo-Hackathon-2025

# 2. Install backend dependencies
pip install -r requirements.txt

# 3. Install frontend dependencies
cd frontend
npm install
cd ..
```

## Running the Application

### Option 1: Simple Demo (HTML only)

The fastest way to see the app in action:

```bash
# 1. Start the backend API
python backend/app.py

# 2. In another terminal, serve the demo
python -m http.server 8080

# 3. Open browser to http://localhost:8080/demo.html
```

### Option 2: Full React Frontend

For the complete experience:

**Terminal 1 - Backend:**
```bash
python backend/app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Then open http://localhost:3000

### Option 3: Both with one command

```bash
npm install  # Install concurrently
npm run dev  # Starts both backend and frontend
```

## First Steps

1. **Start a conversation**: Click on a suggested question or type your interests
2. **Explore majors**: Review the AI's recommendations with detailed information
3. **Generate schedule**: Click "Generate Schedule" to see an optimized first-year plan
4. **Keep exploring**: Ask follow-up questions to refine your major choice

## Example Questions

- "I love coding and solving complex problems"
- "I want to help people and work in healthcare"  
- "I'm interested in business and entrepreneurship"
- "Tell me about engineering majors at BYU"
- "What careers can I pursue with a psychology degree?"

## Optional: Enable AI Features

For enhanced AI responses using OpenAI:

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your-api-key-here
```

**Note:** The app works great in mock mode without an API key!

## Troubleshooting

**Backend won't start?**
- Check Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt`

**Frontend won't start?**
- Check Node version: `node --version` (need 16+)
- Clear npm cache: `npm cache clean --force`
- Reinstall: `rm -rf node_modules && npm install`

**API errors?**
- Backend must be running on port 5000
- Check firewall settings
- Verify with: `curl http://localhost:5000/api/health`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [API documentation](README.md#api-endpoints)
- Customize majors in `backend/data/majors.json`
- Contribute improvements!

## Support

Built for the BYU Homecoming 2025 Redo Hackathon by Team AMIRUS 🎓
