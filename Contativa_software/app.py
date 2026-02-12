# Rodar o arquivo 'criar_banco.py' uma vez para que crie o banco de dados

from flask import Flask
from routes import routes_bp

app = Flask(__name__)
app.secret_key = 'Alexandre Strechar do Nascimento'  # Adicione isso no seu arquivo principal
app.register_blueprint(routes_bp, app=app)

if __name__ == '__main__':
    app.run(debug=True)
