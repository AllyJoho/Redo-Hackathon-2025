# Architecture Documentation

## System Overview

BYU Major Advisor is a full-stack web application that uses AI to help students explore academic majors and optimize their course schedules.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │           React Application (Port 3000)             │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │   App    │  │Components│  │  Services (API)  │  │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                      HTTP/REST API
                           │
┌─────────────────────────────────────────────────────────────┐
│                      Backend API                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │         Flask Server (Port 5000)                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │  Routes  │  │ Chatbot  │  │   Major Data     │  │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                    (Optional: OpenAI API)
                           │
┌─────────────────────────────────────────────────────────────┐
│              External Services (Optional)                   │
│                    OpenAI GPT-3.5                          │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Architecture

#### Technology Stack
- **React 18**: Modern UI framework
- **Axios**: HTTP client for API calls
- **CSS3**: Styling with BYU branding

#### Key Components

1. **App.js** (Main Container)
   - Manages application state
   - Handles chat conversation flow
   - Coordinates major recommendations and schedule generation

2. **ChatMessage.js**
   - Displays individual chat messages
   - Differentiates between user and AI messages
   - Formats text appropriately

3. **MajorCard.js**
   - Renders major information cards
   - Shows career paths, salary, and requirements
   - Interactive hover effects

4. **ScheduleDisplay.js**
   - Displays optimized course schedules
   - Shows reasoning for course selection
   - Lists applicable majors

#### State Management
```javascript
- messages: Array of conversation history
- inputMessage: Current user input
- isLoading: Loading state indicator
- recommendedMajors: Array of major IDs
- majorDetails: Detailed major information
- schedule: Generated schedule data
```

### Backend Architecture

#### Technology Stack
- **Flask 3.0**: Python web framework
- **Flask-CORS**: Cross-origin resource sharing
- **OpenAI API**: AI-powered responses (optional)
- **Python-dotenv**: Environment configuration

#### Key Modules

1. **app.py** (API Server)
   - RESTful API endpoints
   - Request validation
   - Error handling
   - CORS configuration

2. **utils/chatbot.py** (AI Logic)
   - MajorAdvisorChatbot class
   - Interest analysis algorithm
   - Schedule optimization logic
   - Mock mode for offline operation

3. **data/majors.json** (Data Store)
   - Major definitions
   - Course requirements
   - Career information
   - Prerequisite data

#### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Health check |
| `/api/majors` | GET | List all majors |
| `/api/major/<id>` | GET | Get specific major |
| `/api/chat` | POST | Send chat message |
| `/api/schedule` | POST | Generate schedule |
| `/api/compare` | POST | Compare majors |

## Data Flow

### Chat Flow
```
1. User sends message
   ↓
2. Frontend sends POST to /api/chat
   ↓
3. Backend analyzes interests
   ↓
4. Chatbot matches with majors
   ↓
5. Response with recommendations
   ↓
6. Frontend displays results
```

### Schedule Generation Flow
```
1. User selects majors
   ↓
2. Frontend sends POST to /api/schedule
   ↓
3. Backend analyzes requirements
   ↓
4. Algorithm finds common courses
   ↓
5. Prioritizes multi-major courses
   ↓
6. Returns optimized schedule
   ↓
7. Frontend displays with reasoning
```

## Algorithms

### Interest Matching Algorithm

**AI Mode (OpenAI):**
```python
1. Create context with all majors
2. Send user message + context to GPT-3.5
3. AI generates personalized response
4. Extract mentioned majors from response
5. Return recommendations with details
```

**Mock Mode (Keyword-based):**
```python
1. Convert message to lowercase
2. Check for interest keywords
3. Map keywords to major IDs
4. Generate template response
5. Return top 3 matches
```

### Schedule Optimization Algorithm

```python
def generate_schedule(major_ids):
    1. Get selected majors
    2. Collect all first-year courses
    3. Count occurrences across majors
    4. Sort by frequency (most common first)
    5. Select top 5 courses (15 credits)
    6. Generate reasoning for each course
    7. Return schedule + explanation
```

**Optimization Goals:**
- Maximize courses shared across majors
- Include essential GE requirements
- Balance course load (15 credits)
- Minimize wasted credits if major changes

## Major Data Structure

```json
{
  "id": "unique-identifier",
  "name": "Major Name",
  "college": "College Name",
  "description": "Brief description",
  "interests": ["keyword1", "keyword2"],
  "prerequisites": ["Course1", "Course2"],
  "core_courses": ["Course3", "Course4"],
  "total_credits": 120,
  "career_paths": ["Career1", "Career2"],
  "average_salary": 70000,
  "first_year_courses": ["Course1", "Course2"]
}
```

## Deployment Considerations

### Development
- Backend: Flask development server
- Frontend: React development server with hot reload
- Database: JSON file (suitable for hackathon scale)

### Production Recommendations
- **Backend**: Gunicorn or uWSGI WSGI server
- **Frontend**: Build and serve static files via Nginx
- **Database**: PostgreSQL or MongoDB for scale
- **Caching**: Redis for API response caching
- **Load Balancing**: Nginx or AWS ALB
- **Monitoring**: Application performance monitoring
- **Security**: HTTPS, API rate limiting, input validation

## Security Considerations

1. **API Key Protection**
   - Store in environment variables
   - Never commit to git
   - Use .env files

2. **Input Validation**
   - Validate all user inputs
   - Sanitize data before processing
   - Limit message lengths

3. **CORS Configuration**
   - Currently allows all origins (dev mode)
   - Restrict to specific domains in production

4. **Rate Limiting**
   - Not implemented (add for production)
   - Prevent API abuse
   - Use Flask-Limiter

## Performance Optimization

### Current Implementation
- Lightweight JSON data store
- Efficient keyword matching
- Minimal external dependencies

### Future Improvements
- Implement caching layer
- Database indexing for majors
- Lazy loading for frontend
- API response compression
- CDN for static assets

## Testing Strategy

### Unit Tests (Future)
- Chatbot interest matching
- Schedule optimization algorithm
- API endpoint responses

### Integration Tests (Future)
- Frontend-backend communication
- API error handling
- Data validation

### E2E Tests (Future)
- Complete user workflows
- Chat conversations
- Schedule generation

## Scalability

### Current Limitations
- In-memory data storage
- No database
- Single-instance server
- No caching

### Scaling Path
1. Add database (PostgreSQL)
2. Implement Redis caching
3. Containerize with Docker
4. Deploy to cloud (AWS/GCP/Azure)
5. Add load balancing
6. Implement microservices if needed

## Technology Choices Rationale

- **React**: Popular, excellent ecosystem, component reusability
- **Flask**: Lightweight, Python-based, easy to prototype
- **OpenAI**: State-of-the-art NLP, easy integration
- **JSON**: Simple, sufficient for prototype scale
- **Mock Mode**: Ensures functionality without external dependencies

## Future Enhancements

1. **Data Persistence**
   - User accounts and saved preferences
   - Conversation history
   - Schedule bookmarking

2. **Enhanced Features**
   - 4-year degree planning
   - Course prerequisite visualization
   - Integration with BYU course catalog
   - Mobile application

3. **AI Improvements**
   - Fine-tuned models for BYU specifics
   - Context-aware conversations
   - Personality matching with majors

4. **Analytics**
   - Usage tracking
   - Popular major trends
   - Conversion metrics
