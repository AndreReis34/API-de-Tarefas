from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.post("/register")
def register():
	data = request.get_json(silent=True) or {}
	username = (data.get("username") or "").strip()
	password = data.get("password") or ""

	if not username or not password:
		return jsonify({"error": "Username a password são obrigatorios!"}), 400

	if User.query.filter_by(username=username).first():
		return jsonify({"error": "Username já existe!"}), 409

	user = User(username=username)
	user.set_password(password)
	db.session.add(user)
	db.session.commit()

	return jsonify({"id": user.id, "username": user.username}), 201


@auth_bp.post("/login")
def login():
	data = request.get_json(silent=True) or {}
	username = (data.get("username") or "").strip()
	password = data.get("password") or ""


	user = User.query.filter_by(username=username).first()
	if not user or not user.check_password(password):
		return jsonify({"error": "Credencias Inválidas!"}), 401

	token = create_access_token(identity=str(user.id))
	return jsonify({"access_token": token})