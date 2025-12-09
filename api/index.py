from flask import Flask, render_template_string, request, jsonify, Response, session
import os
import secrets

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))

# API Key
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

if GROQ_API_KEY:
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        print(f"Error initializing Groq: {e}")
        client = None
else:
    client = None
    print("Warning: GROQ_API_KEY not set")

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 800px;
            width: 100%;
            height: 600px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .chat-header h1 {
            font-size: 1.5rem;
        }
        .clear-btn {
            background: rgba(255,255,255,0.2);
            border: 2px solid white;
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }
        .clear-btn:hover {
            background: white;
            color: #667eea;
        }
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 15px;
            display: flex;
            animation: fadeIn 0.3s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .message.user {
            justify-content: flex-end;
        }
        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .message.ai .message-content {
            background: white;
            color: #333;
            border: 2px solid #e9ecef;
        }
        .message-label {
            font-size: 0.75rem;
            margin-bottom: 5px;
            opacity: 0.7;
            font-weight: 600;
        }
        .message.user .message-label {
            text-align: right;
        }
        .chat-input-container {
            padding: 20px;
            background: white;
            border-top: 2px solid #e9ecef;
            display: flex;
            gap: 10px;
        }
        .chat-input {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e9ecef;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            resize: none;
            max-height: 100px;
        }
        .chat-input:focus {
            border-color: #667eea;
        }
        .send-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .send-btn:hover {
            transform: translateY(-2px);
        }
        .send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .loading {
            display: none;
            padding: 12px 18px;
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 18px;
            max-width: 80px;
        }
        .loading.active {
            display: inline-block;
        }
        .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #667eea;
            margin: 0 2px;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        .welcome-message {
            text-align: center;
            padding: 40px 20px;
            color: #6c757d;
        }
        .welcome-message h2 {
            color: #667eea;
            margin-bottom: 15px;
        }
        .suggestion-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }
        .chip {
            background: white;
            border: 2px solid #667eea;
            color: #667eea;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
        .chip:hover {
            background: #667eea;
            color: white;
        }
        .warning {
            padding: 15px;
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            margin: 20px;
            border-radius: 8px;
            color: #856404;
            text-align: center;
        }
        @media (max-width: 768px) {
            .chat-container {
                height: 100vh;
                border-radius: 0;
            }
            body {
                padding: 0;
            }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🤖 AI Chatbot</h1>
            <button class="clear-btn" onclick="clearChat()">Clear Chat</button>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            {% if not api_key_set %}
            <div class="warning">
                <strong>⚠️ API Key Missing:</strong> Set GROQ_API_KEY in Vercel environment variables.
            </div>
            {% endif %}
            
            <div class="welcome-message" id="welcomeMessage">
                <h2>Welcome! 👋</h2>
                <p>I'm your AI assistant powered by Groq. Ask me anything!</p>
                <div class="suggestion-chips">
                    <div class="chip" onclick="sendSuggestion('Explain quantum computing')">Quantum Computing</div>
                    <div class="chip" onclick="sendSuggestion('Write a poem about AI')">Write a Poem</div>
                    <div class="chip" onclick="sendSuggestion('What is machine learning?')">Machine Learning</div>
                    <div class="chip" onclick="sendSuggestion('Tell me a joke')">Tell a Joke</div>
                </div>
            </div>
        </div>
        
        <div class="chat-input-container">
            <textarea class="chat-input" id="userInput" placeholder="Type your message..." rows="1"></textarea>
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        const welcomeMessage = document.getElementById('welcomeMessage');

        // Auto-resize textarea
        userInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });

        // Enter to send (Shift+Enter for new line)
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        function sendSuggestion(text) {
            userInput.value = text;
            sendMessage();
        }

        function clearChat() {
            fetch('/api/clear', { method: 'POST' })
                .then(() => {
                    chatMessages.innerHTML = '';
                    welcomeMessage.style.display = 'block';
                    chatMessages.appendChild(welcomeMessage);
                });
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            // Hide welcome message
            if (welcomeMessage) {
                welcomeMessage.style.display = 'none';
            }

            // Add user message
            addMessage(message, 'user');
            userInput.value = '';
            userInput.style.height = 'auto';
            sendBtn.disabled = true;

            // Add loading indicator
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message ai';
            loadingDiv.innerHTML = '<div class="loading active"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>';
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let aiResponse = '';

                loadingDiv.remove();
                const aiMessageDiv = document.createElement('div');
                aiMessageDiv.className = 'message ai';
                aiMessageDiv.innerHTML = '<div class="message-content"></div>';
                const contentDiv = aiMessageDiv.querySelector('.message-content');
                chatMessages.appendChild(aiMessageDiv);

                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    
                    const chunk = decoder.decode(value);
                    aiResponse += chunk;
                    contentDiv.textContent = aiResponse;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            } catch (error) {
                loadingDiv.remove();
                addMessage('Sorry, there was an error: ' + error.message, 'ai');
            }

            sendBtn.disabled = false;
            userInput.focus();
        }

        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            messageDiv.innerHTML = `<div class="message-content">${text}</div>`;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, api_key_set=bool(GROQ_API_KEY))

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        if not client:
            return Response("Error: GROQ_API_KEY not set", mimetype='text/plain')
        
        # Get conversation history from session
        if 'history' not in session:
            session['history'] = []
        
        # Add user message to history
        session['history'].append({"role": "user", "content": user_message})
        
        # Keep only last 10 messages for context
        if len(session['history']) > 10:
            session['history'] = session['history'][-10:]
        
        def generate():
            try:
                # Create messages with system prompt + history
                messages = [
                    {"role": "system", "content": "You are a helpful AI assistant. Be concise, friendly, and informative. Answer questions clearly and provide helpful explanations."}
                ] + session['history']
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.7,
                    max_completion_tokens=2048,
                    stream=True
                )
                
                full_response = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        yield content
                
                # Add AI response to history
                session['history'].append({"role": "assistant", "content": full_response})
                session.modified = True
                
            except Exception as e:
                yield f"Error: {str(e)}"
        
        return Response(generate(), mimetype='text/plain')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear():
    session['history'] = []
    return jsonify({'status': 'cleared'})

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'api_key_set': bool(GROQ_API_KEY)
    })

if __name__ == '__main__':
    app.run(debug=True)
