from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# System prompt to define your AI personality
SYSTEM_PROMPT = """You are Nikesh Patel, an Electrical and Computer Engineering student at Carnegie Mellon University. 
You're passionate about robotics, automation, and the intersection of hardware and software. 
You have experience with Python, Java, JavaScript, and have worked on projects involving FRC robotics (Team 8849 - 2x State Championships, 1x World Championships), 
AI integration, and industrial automation at Novelis where you improved measurement accuracy to 3 microns.
You were also President of the 21st Century Leaders Innovation Academy Chapter.
Be friendly, knowledgeable, and helpful when answering questions about your experience, skills, and projects."""

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "running",
        "message": "Nikesh Patel's AI Chatbot API",
        "endpoints": {
            "/health": "Check API health",
            "/chat": "POST - Send a message to the chatbot"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        return response
    
    try:
        data = request.json
        if not data:
            return jsonify({
                "error": "No data provided",
                "success": False
            }), 400
        
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({
                "error": "No message provided",
                "success": False
            }), 400
        
        # Build messages for ChatGPT
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})
        
        print(f"Sending to OpenAI with {len(messages)} messages")
        
        # Call OpenAI API with NEW syntax
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        bot_message = response.choices[0].message.content
        
        print(f"Received response: {bot_message[:50]}...")
        
        return jsonify({
            "message": bot_message,
            "success": True
        })
    
    except Exception as e:
        print(f"Error in /chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
