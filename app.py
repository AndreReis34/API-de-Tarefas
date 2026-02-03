from flask import Flask, jsonify
from flask_migrate import Migrate 
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from models import db
from auth import auth_bp
from tasks import tasks_bp

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	Migrate(app, db)
	JWTManager(app)
	CORS(app, resources={r"/*": {"origins": "gerente-de-tarefas-front-end-production.up.railway.app:8080"}})

	app.register_blueprint(auth_bp)
	app.register_blueprint(tasks_bp)


	@app.get("/health")
	def health():
		return jsonify({"status": "ok"})

	return app

