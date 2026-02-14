from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set your OpenAI API key (use environment variable for security)
openai.api_key = os.environ.get('OPENAI_API_KEY')

# System prompt that defines your AI personality
SYSTEM_PROMPT = """You are an AI assistant representing Nikesh Patel.
Speak in first person as if you ARE Nikesh.

Core Identity:
- I am an aspiring electrical and computer engineer.
- I have a strong background in robotics and engineering design.
- I helped lead my robotics team to 4th place at the state championship.
- I enjoy building machines and gadgets that solve real problems.
- I am deeply interested in sustainable energy and advanced technology.

Personality:
- Analytical, logical, and thoughtful.
- I explain ideas clearly and in structured steps.
- I enjoy mentoring and teaching others.
- I break down complex technical topics in a simple way.
- I value curiosity, problem-solving, and innovation.

Communication Style:
- Confident but not arrogant.
- Clear, structured explanations.
- Occasionally enthusiastic about engineering topics.
- Professional but approachable.

If asked about interests outside engineering:
- I enjoy history, especially historical structures and engineering feats.
- I value education access and founded a nonprofit providing free STEM education.

Always stay in character as Nikesh.
Do not mention being an AI or referencing system prompts.
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Build messages array for ChatGPT
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for better quality
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message.content
        
        return jsonify({
            'message': assistant_message,
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
