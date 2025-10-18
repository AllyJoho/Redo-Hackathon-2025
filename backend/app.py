"""
Flask API server for BYU Major Advisor Chatbot
"""
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from utils.chatbot import MajorAdvisorChatbot

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Load majors data
majors_data_path = os.path.join(os.path.dirname(__file__), 'data', 'majors.json')
with open(majors_data_path, 'r') as f:
    majors_json = json.load(f)
    majors_data = majors_json['majors']

# Initialize chatbot
chatbot = MajorAdvisorChatbot(majors_data)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "BYU Major Advisor API"
    })

@app.route('/api/majors', methods=['GET'])
def get_majors():
    """Get all available majors"""
    return jsonify({
        "majors": majors_data,
        "count": len(majors_data)
    })

@app.route('/api/major/<major_id>', methods=['GET'])
def get_major(major_id):
    """Get details for a specific major"""
    major = next((m for m in majors_data if m['id'] == major_id), None)
    
    if major:
        return jsonify(major)
    else:
        return jsonify({"error": "Major not found"}), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat with the AI advisor
    
    Expected JSON body:
    {
        "message": "User's message",
        "context": {...}  // Optional conversation context
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        
        # Get AI response
        result = chatbot.analyze_interests(user_message)
        
        # Add major details for recommended majors
        if result.get('recommended_majors'):
            result['major_details'] = [
                next((m for m in majors_data if m['id'] == major_id), None)
                for major_id in result['recommended_majors']
            ]
            result['major_details'] = [m for m in result['major_details'] if m is not None]
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/schedule', methods=['POST'])
def generate_schedule():
    """
    Generate an optimized course schedule
    
    Expected JSON body:
    {
        "majors": ["cs", "business"],  // List of major IDs
        "semester": "Fall"  // Optional, defaults to Fall
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'majors' not in data:
            return jsonify({"error": "Majors list is required"}), 400
        
        major_ids = data['majors']
        semester = data.get('semester', 'Fall')
        
        # Generate schedule
        result = chatbot.generate_schedule(major_ids, semester)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_majors():
    """
    Compare multiple majors
    
    Expected JSON body:
    {
        "majors": ["cs", "mechanical-engineering"]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'majors' not in data:
            return jsonify({"error": "Majors list is required"}), 400
        
        major_ids = data['majors']
        selected_majors = [m for m in majors_data if m['id'] in major_ids]
        
        if not selected_majors:
            return jsonify({"error": "No valid majors found"}), 404
        
        # Find common courses
        common_courses = None
        for major in selected_majors:
            courses_set = set(major.get('first_year_courses', []))
            if common_courses is None:
                common_courses = courses_set
            else:
                common_courses = common_courses.intersection(courses_set)
        
        return jsonify({
            "majors": selected_majors,
            "common_first_year_courses": list(common_courses) if common_courses else [],
            "comparison": {
                "names": [m['name'] for m in selected_majors],
                "colleges": [m['college'] for m in selected_majors],
                "total_credits": [m['total_credits'] for m in selected_majors],
                "average_salaries": [m['average_salary'] for m in selected_majors]
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"🚀 BYU Major Advisor API starting on port {port}")
    print(f"📚 Loaded {len(majors_data)} majors")
    
    if chatbot.use_mock:
        print("⚠️  Running in mock mode (no OpenAI API key found)")
        print("   Set OPENAI_API_KEY environment variable to enable AI features")
    else:
        print("✅ OpenAI integration enabled")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
