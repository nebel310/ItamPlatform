import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from events.routes import events_blueprint
from auth.routes import auth_blueprint
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

# Используем переменные окружения для настройки базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:12345@localhost:5432/itam_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

app.register_blueprint(events_blueprint, url_prefix='/api/events')
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

# Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "ITAM API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True, port=5001)