# Fichier : webapp.py
from flask import Flask, request, jsonify, render_template_string
from chatbot import OrientationChatbot

app = Flask(__name__)
# Un seul contexte pour la session Web
bot = OrientationChatbot()
context_id = bot.create_context()

# HTML simplifié pour l'interface
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
        async function send() {
            const input = document.getElementById('input');
            const message = input.value;
            if (!message) return;
            // afficher le message utilisateur
            const chat = document.getElementById('chatbox');
            chat.innerHTML += `<div class='user'>Moi: ${message}</div>`;
            input.value = '';
            // requête au serveur
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });
            const data = await res.json();
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
    response = bot.process_message(context_id, message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
