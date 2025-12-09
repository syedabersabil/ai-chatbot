# 🤖 AI Chatbot

A simple, beautiful AI chatbot with conversation history and real-time streaming responses powered by Groq's Llama 3.3 70B.

## Features

- **Streaming Responses**: See AI responses appear in real-time
- **Conversation History**: Maintains context across messages
- **Beautiful UI**: Modern chat interface with gradient design
- **Suggestion Chips**: Quick-start conversation prompts
- **Mobile Responsive**: Works perfectly on all devices
- **Lightweight**: Only 2 dependencies, <20MB
- **Serverless**: Deploys on Vercel

## Tech Stack

- **Backend**: Python Flask with session management
- **AI Model**: Groq Llama 3.3 70B (fast inference)
- **Deployment**: Vercel serverless functions

## Local Setup

1. Clone the repository:
```bash
git clone https://github.com/syedabersabil/ai-chatbot.git
cd ai-chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variable:
```bash
export GROQ_API_KEY="your_groq_api_key"
```

4. Run the app:
```bash
python api/index.py
```

5. Open http://localhost:5000

## Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New Project"**
3. Import **syedabersabil/ai-chatbot**
4. Add environment variables:
   - `GROQ_API_KEY` = your Groq API key
   - `SECRET_KEY` = any random string (for session encryption)
5. Click **Deploy**

## Features Explained

### Conversation History
The chatbot remembers the last 10 messages in your conversation, allowing it to maintain context and have more natural conversations.

### Streaming Responses
See the AI's response appear word-by-word in real-time, just like ChatGPT.

### Suggestion Chips
Click on pre-made prompts to quickly start a conversation:
- Quantum Computing
- Write a Poem
- Machine Learning
- Tell a Joke

### Clear Chat
Reset the conversation at any time with the "Clear Chat" button.

## Example Conversations

**You:** Explain quantum computing  
**AI:** Quantum computing is a type of computing that uses quantum-mechanical phenomena...

**You:** Write a poem about AI  
**AI:** *Generates a creative poem*

**You:** Tell me a joke  
**AI:** *Shares a funny joke*

## API Endpoints

- `GET /` - Chat interface
- `POST /api/chat` - Send message, get streamed response
  - Body: `{"message": "your message"}`
- `POST /api/clear` - Clear conversation history
- `GET /api/health` - Health check

## Customization

You can customize the system prompt in `api/index.py`:

```python
{"role": "system", "content": "You are a helpful AI assistant..."}
```

Change it to create different personalities or specialized assistants!

## License

MIT
