import os

class Config:
	SECRET_KEY = os.getenv("SECRET_KEY", "dev")
	JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-dev")
	SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_URL", "sqlite:///todo.db")
	SQLALCHEMY_TRACK_MODIFICATIONS = False

