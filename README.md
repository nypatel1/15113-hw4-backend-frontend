# AI Chatbot Backend

Flask backend that powers an AI chatbot using OpenAI's ChatGPT API.

## Endpoints
`GET /`- Service info and health status  
`GET /health` - Health check  
`POST /chat` - Send message, get AI response

### POST /chat
**Request:**
```json
{
  "message": "question here",
  "history": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
}
```

**Response:**
```json
{
  "message": "AI response here",
  "success": true
}
```



## Frontend-Backend Communication
1. User types message in frontend chat interface
2. Frontend sends POST request to `/chat` with message and conversation history
3. Backend calls OpenAI API with full conversation context
4. Backend returns AI response to frontend
5. Frontend displays response and updates conversation history



## Setup

# Set environment variable
export OPENAI_API_KEY="your_key_here"
# Run
python app.py
```
### Deployment (Render.com)
1. Connect GitHub repo to Render
2. Set environment variables:
   - `OPENAI_API_KEY` - OpenAI API key
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app:app`



### Security
The API keys are stored on backend only, the OpenAI API key is stored as an environment variable. (`OPENAI_API_KEY`) on the server, never sent to the frontend
There are no keys in source code, and the CORS is enabled which allows frontend to make requests from different domain

