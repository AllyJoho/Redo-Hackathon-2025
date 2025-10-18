# BYU Major Advisor - AI-Powered Chatbot 🎓

This is the repository that the AMIRUS team is using for our project in the BYU Homecoming 2025 Redo Hackathon.

## Overview

BYU Major Advisor is an AI-powered chatbot designed to help BYU students explore and choose majors intelligently. The system analyzes student interests, compares them with BYU majors, class data, and requirements, then generates optimized schedules that keep multiple academic paths open—helping freshmen avoid wasted time, money, and credits while discovering the right major.

## Features

- 🤖 **AI-Powered Chat Interface**: Natural language conversation to understand student interests
- 📚 **Major Database**: Comprehensive information about BYU majors including requirements, courses, and career paths
- 🔍 **Interest Analysis**: Matches student interests with suitable majors
- 📅 **Smart Schedule Generation**: Creates optimized first-year schedules that keep multiple major options open
- 💰 **Cost & Time Optimization**: Helps avoid wasted credits and unnecessary coursework
- 📊 **Major Comparison**: Compare multiple majors side-by-side
- 🎯 **Career Path Insights**: Information about career opportunities and average salaries

## Technology Stack

### Backend
- **Python 3.x** with Flask
- **OpenAI API** for intelligent chat responses (with fallback mock mode)
- **Flask-CORS** for API communication
- JSON-based major database

### Frontend
- **React 18** for UI
- **Axios** for API calls
- Modern CSS with BYU branding

## Project Structure

```
.
├── backend/
│   ├── app.py                 # Flask API server
│   ├── data/
│   │   └── majors.json        # BYU majors database
│   └── utils/
│       └── chatbot.py         # AI chatbot logic
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API service layer
│   │   ├── styles/            # CSS stylesheets
│   │   ├── App.js            # Main React app
│   │   └── index.js          # React entry point
│   └── package.json
├── requirements.txt           # Python dependencies
├── package.json              # Node.js scripts
└── README.md

```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### 1. Clone the Repository

```bash
git clone https://github.com/AllyJoho/Redo-Hackathon-2025.git
cd Redo-Hackathon-2025
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Optional: Set up OpenAI API key for enhanced AI features
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Frontend Setup

```bash
# Install frontend dependencies
cd frontend
npm install
cd ..
```

## Running the Application

### Option 1: Run Backend and Frontend Separately

**Terminal 1 - Backend:**
```bash
python backend/app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Option 2: Run Both Simultaneously

```bash
# Install concurrently (if not already installed)
npm install

# Start both servers
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## API Endpoints

### Health Check
```
GET /api/health
```

### Get All Majors
```
GET /api/majors
```

### Get Specific Major
```
GET /api/major/{major_id}
```

### Chat with AI Advisor
```
POST /api/chat
Body: {
  "message": "I love coding and problem-solving",
  "context": {}
}
```

### Generate Optimized Schedule
```
POST /api/schedule
Body: {
  "majors": ["cs", "business"],
  "semester": "Fall"
}
```

### Compare Majors
```
POST /api/compare
Body: {
  "majors": ["cs", "mechanical-engineering"]
}
```

## Usage Examples

1. **Explore Interests**: Start a conversation about your interests
   - "I love coding and solving complex problems"
   - "I want to help people and work in healthcare"

2. **Get Recommendations**: The AI will analyze your interests and recommend matching majors

3. **View Major Details**: Browse detailed information about recommended majors

4. **Generate Schedule**: Click "Generate Schedule" to create an optimized first-year course plan

5. **Keep Options Open**: The schedule prioritizes courses that satisfy requirements for multiple majors

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI API Configuration (optional - runs in mock mode without it)
OPENAI_API_KEY=your-openai-api-key-here

# Flask Configuration
FLASK_ENV=development
PORT=5000
```

### Mock Mode

The application runs in **mock mode** by default if no OpenAI API key is provided. Mock mode uses keyword-based matching to provide recommendations, making the app fully functional without external API dependencies.

## Major Database

The `backend/data/majors.json` file contains information about BYU majors:
- Major name and ID
- College affiliation
- Description
- Interest keywords
- Prerequisites and core courses
- Career paths
- Average salary information
- First-year course recommendations

Currently includes 8 majors:
- Computer Science
- Business Management
- Psychology
- Mechanical Engineering
- Nursing
- English
- Biology
- Accounting

## Development

### Adding New Majors

Edit `backend/data/majors.json` and add a new major object:

```json
{
  "id": "new-major",
  "name": "Major Name",
  "college": "College Name",
  "description": "Description",
  "interests": ["keyword1", "keyword2"],
  "prerequisites": ["Course1", "Course2"],
  "core_courses": ["Course3", "Course4"],
  "total_credits": 120,
  "career_paths": ["Career1", "Career2"],
  "average_salary": 70000,
  "first_year_courses": ["Course1", "Course2", "GE electives"]
}
```

### Testing API Endpoints

```bash
# Test health check
curl http://localhost:5000/api/health

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I love programming"}'

# Test schedule generation
curl -X POST http://localhost:5000/api/schedule \
  -H "Content-Type: application/json" \
  -d '{"majors": ["cs", "business"], "semester": "Fall"}'
```

## Key Features Explained

### Smart Schedule Optimization

The schedule generator:
1. Analyzes requirements across multiple selected majors
2. Prioritizes courses that satisfy multiple major requirements
3. Includes essential GE courses that all students need
4. Balances course load for a typical 15-credit semester
5. Provides reasoning for each course selection

### Interest Matching Algorithm

The system matches student interests through:
- Natural language processing (OpenAI mode)
- Keyword matching (mock mode)
- Interest alignment with major profiles
- Career path consideration

## Contributing

This project was developed for the BYU Homecoming 2025 Redo Hackathon by the AMIRUS team.

## License

MIT License - See LICENSE file for details

## Team AMIRUS

Developed with ❤️ for BYU students

## Future Enhancements

Potential improvements:
- Course scheduling across all 4 years
- Real-time BYU course catalog integration
- Student progress tracking
- Advisor appointment scheduling
- Mobile app version
- Multi-language support
- Graduate program exploration
