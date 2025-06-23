# Fichier : webapp.py
from flask import Flask, request, jsonify, render_template_string
from chatbot import OrientationChatbot

app = Flask(__name__)
# Un seul contexte pour la session Web
bot = OrientationChatbot()
context_id = bot.create_context()

# Interface HTML basique
HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Chatbot Orientation Post-Bac</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 2em auto; }
        #chatbox { border: 1px solid #ccc; padding: 1em; height: 300px; overflow-y: scroll; }
        .user { color: blue; margin: 0.5em 0; }
        .bot { color: green; margin: 0.5em 0; }
        input { width: 80%; padding: 0.5em; }
        button { padding: 0.5em 1em; }
    </style>
</head>
<body>
    <h1>Conseiller d'Orientation Post-Bac</h1>
    <div id="chatbox">
        <div class="bot">Bot: Bonjour ! Quels sont tes centres d’intérêt ?</div>
    </div>
    <input id="input" type="text" placeholder="Écris ta réponse..." autofocus>
    <button onclick="send()">Envoyer</button>

    <script>
        if (!sessionStorage.getItem('context_id')) {
            sessionStorage.setItem('context_id', Math.random().toString(36).substring(2));
        }
        async function send() {
            const input = document.getElementById('input');
            const message = input.value;
            if (!message) return;
            const chat = document.getElementById('chatbox');
            chat.innerHTML += `<div class='user'>Moi: ${message}</div>`;
            input.value = '';

            const context_id = sessionStorage.getItem('context_id');
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, context_id })
            });
            const data = await res.json();
            sessionStorage.setItem('context_id', data.context_id); // Au cas où le serveur en crée un nouveau
            chat.innerHTML += `<div class='bot'>Bot: ${data.response}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    client_context_id = data.get('context_id')

    # Crée un contexte si le client n’en a pas encore
    if not client_context_id or client_context_id not in bot.contexts:
        client_context_id = bot.create_context()

    response = bot.process_message(client_context_id, message)
    return jsonify({'response': response, 'context_id': client_context_id})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    # Bind to 0.0.0.0 so Render can detect the open port
    app.run(debug=True, host='0.0.0.0', port=port)
