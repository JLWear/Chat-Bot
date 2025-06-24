from flask import Flask, request, jsonify, render_template_string
from chatbot import OrientationChatbot

app = Flask(__name__)
bot = OrientationChatbot()

HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Chatbot Orientation Post-Bac</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f6fa;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        header {
            background-color: #25D366;
            color: white;
            width: 100%;
            padding: 1em;
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
            position: fixed;
            top: 0;
        }
        header .verified {
            font-size: 0.8em;
            background: white;
            color: #25D366;
            border-radius: 5px;
            padding: 0.2em 0.5em;
            margin-left: 0.5em;
        }
        #chatbox {
            background: #fff;
            margin-top: 80px;
            border: 1px solid #ccc;
            padding: 1em;
            width: 90%;
            max-width: 600px;
            height: 400px;
            overflow-y: scroll;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .user, .bot {
            padding: 0.6em 1em;
            margin: 0.5em 0;
            border-radius: 15px;
            max-width: 70%;
            clear: both;
        }
        .user {
            background-color: #dcf8c6;
            align-self: flex-end;
            float: right;
        }
        .bot {
            background-color: #fff;
            border: 1px solid #ccc;
            float: left;
        }
        #input-area {
            margin-top: 1em;
            width: 90%;
            max-width: 600px;
            display: flex;
            gap: 0.5em;
        }
        input {
            flex: 1;
            padding: 0.5em;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        button {
            padding: 0.5em 1em;
            border: none;
            background-color: #25D366;
            color: white;
            border-radius: 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <header>
        Chatbot Orientation Post-Bac
    </header>
    <div id="chatbox">
        <div class="bot">Bot: Bonjour ! Quels sont tes centres d’intérêt ?</div>
    </div>
    <div id="input-area">
        <input id="input" type="text" placeholder="Écris ta réponse..." autofocus>
        <button onclick="send()">Envoyer</button>
    </div>

    <script>
        if (!sessionStorage.getItem('context_id')) {
            sessionStorage.setItem('context_id', Math.random().toString(36).substring(2));
        }

        async function send() {
            const input = document.getElementById('input');
            const message = input.value.trim();
            if (!message) return;
            const chat = document.getElementById('chatbox');
            chat.innerHTML += `<div class='user'>${message}</div>`;
            input.value = '';

            const context_id = sessionStorage.getItem('context_id');
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, context_id })
            });
            const data = await res.json();
            sessionStorage.setItem('context_id', data.context_id);
            chat.innerHTML += `<div class='bot'>${linkify(data.response)}</div>`;
            chat.scrollTop = chat.scrollHeight;
        }

        function linkify(text) {
            return text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
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

    if not client_context_id or client_context_id not in bot.contexts:
        client_context_id = bot.create_context()

    response = bot.process_message(client_context_id, message)
    return jsonify({'response': response, 'context_id': client_context_id})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
