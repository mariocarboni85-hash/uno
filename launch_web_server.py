"""
Launcher web server Flask per SuperAgent
Avvia un server web semplice su http://127.0.0.1:5000
"""

from flask import Flask, render_template_string, request, jsonify
import sys
import os

app = Flask(__name__)
MESSAGES = []

# HTML template moderno
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>SuperAgent Chat</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background: #f5f5f5;
        }
        .chat-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        .messages {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            margin: 20px 0;
            background: #fafafa;
            border-radius: 5px;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
        }
        .user { background: #e3f2fd; }
        .agent { background: #f1f8e9; }
        form {
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #45a049; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>🤖 SuperAgent Chat Interface</h1>
        <div class="messages" id="messages">
            {% for m in messages %}
            <div class="message {{ 'user' if 'Tu:' in m else 'agent' }}">{{ m }}</div>
            {% endfor %}
        </div>
        <form method="post">
            <input type="text" name="msg" placeholder="Scrivi un messaggio..." autofocus required>
            <button type="submit">Invia</button>
        </form>
    </div>
    <script>
        // Auto-scroll messaggi
        var messages = document.getElementById('messages');
        messages.scrollTop = messages.scrollHeight;
    </script>
</body>
</html>
'''

# Prova import SuperAgent con fallback
try:
    from core.brain import SuperAgent
    agent = SuperAgent(name="WebChatAgent", skills=["chat", "apprendimento", "risposta"])
    agent_available = True
    print("✓ SuperAgent caricato correttamente")
except Exception as e:
    print(f"⚠ SuperAgent non disponibile: {e}")
    print("  Server avviato in modalità demo")
    agent_available = False
    agent = None

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_msg = request.form.get('msg', '').strip()
        if user_msg:
            MESSAGES.append(f"Tu: {user_msg}")
            
            # Risposta agent
            if agent_available and agent:
                try:
                    agent.learn_from_chat(user_msg)
                    risposta = agent.propose_solution(user_msg, ambito="informatica")
                except Exception as e:
                    risposta = f"Errore nell'elaborazione: {e}"
            else:
                # Risposta demo
                risposta = f"Echo: {user_msg} (SuperAgent in modalità demo)"
            
            MESSAGES.append(f"SuperAgent: {risposta}")
    
    return render_template_string(HTML, messages=MESSAGES)

@app.route('/health')
def health():
    return jsonify({
        'status': 'running',
        'agent_available': agent_available,
        'messages_count': len(MESSAGES)
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 SuperAgent Web Server")
    print("="*60)
    print(f"📍 URL: http://127.0.0.1:5000")
    print(f"🤖 Agent Status: {'Available' if agent_available else 'Demo Mode'}")
    print("="*60 + "\n")
    
    app.run(host='127.0.0.1', port=5000, debug=False)
