import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
# Utilisez ce port lors du démarrage de votre serveur