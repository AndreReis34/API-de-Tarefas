from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_

from models import db, Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

VALID_STATUS = {"pendente", "concluida"}

def current_user_id()-> int:
	return int(get_jwt_identity())

@tasks_bp.post("")
@jwt_required()
def create_task():
	data = request.get_json(silent=True) or {}
	title = (data.get("title") or "").strip()
	description = data.get("description")
	status = (data.get("status") or "pendente").strip().lower()

	if not title:
		return jsonify({"error": "title é obrigatório!"}), 400
	if status not in VALID_STATUS:
		return jsonify({"error": "staus invalido(user pendente ou concluida)"}), 400

	task = Task(
		title = title,
		description = description,
		status = status,
		user_id = current_user_id()
	)
	db.session.add(task)
	db.session.commit()

	return jsonify(task.to_dict()), 201

@tasks_bp.get("")
@jwt_required()
def list_tasks():
	user_id = current_user_id()

	status = (request.args.get("status") or "").strip().lower()
	q = (request.args.get("q") or "").strip()

	sort = 	(request.args.get("sort") or "created_at").strip()
	order = (request.args.get("order") or "desc").strip().lower()

	page = request.args.get("page", default=1, type=int)
	per_page = request.args.get("per_page", default=10, type=int)
	per_page = max(1, min(per_page, 100))

	query = Task.query.filter_by(user_id=user_id)

	if status:
		if status not in VALID_STATUS:
			return jsonify({"error": "status invalido(use pendente ou concluida)"}), 400
		query = query.filter(Task.status == status)

	if q:
		like = f"%{q}%"
		query = query.filter(or_(Task.title.ilike(like), 
			Task.description.ilike(like)))

	sort_map = {
		"created_at": Task.created_at,
		"updated_at": Task.updated_at,
		"title": Task.title,
		"status": Task.status,
		"id": Task.id,
	}			
	
	sort_col = sort_map.get(sort)
	if not sort_col:
		return jsonify({"error": "Sort Invalido!"}), 400

	if order == "asc":
		query = query.order_by(sort_col.asc())
	elif order == "desc":
		query = query.order_by(sort_col.desc())
	else: 
		return jsonify({"error": "Order Invalido(asc ou desc)"})

	pagination = query.paginate(page=page, per_page=per_page,
		error_out=False)

	return jsonify({
		"items": [t.to_dict() for t in pagination.items],
		"page": pagination.page,
		"per_page": pagination.per_page,
		"total_items": pagination.total,
		"total_pages": pagination.pages,
		"has_next": pagination.has_next,
		"has_prev": pagination.has_prev,
		})

@tasks_bp.get("/<int:task_id>")
@jwt_required()
def get_task(task_id: int):
	user_id = current_user_id()
	task = Task.query.filter_by(id=task_id, user_id=user_id).first()

	if not task:
		return jsonify({"error": "Tarefa não encontrada"}), 404
	return jsonify(task.to_dict())


@tasks_bp.put("/<int:task_id>")
@jwt_required()
def update_task(task_id: int):
	user_id = current_user_id()
	task = Task.query.filter_by(id=task_id, user_id=user_id).first()
	if not task:
		return jsonify({"error": "Tarefa não encontrada"}), 404

	data = request.get_json(silent=True) or {}

	if "title" in data:
		title = (data.get("title") or "").strip()
		if not title:
			return jsonify({"error": "title não estar vazio"}), 400
		task.title = title

	if "description" in data:
		task.description = data.get("description")

	if "status" in data:
		status = (data.get("status") or "").strip().lower()
		if status not in VALID_STATUS:
			return jsonify({"error": "status invalido(use pendente ou concluida)"}), 400
		task.status = status


	db.session.commit()
	return jsonify(task.to_dict())


@tasks_bp.put("<int:task_id>/toggle")
@jwt_required()
def toggle_task(task_id: int):
	user_id = current_user_id()
	task = Task.query.filter_by(id=task_id, user_id=user_id).first()
	if not task:
		return jsonify({"error": "tarefa não encontrada"}), 404

	task.status = "concluida" if task.status == "pendente" else "pendente"

	db.session.commit()
	return jsonify(task.to_dict())


@tasks_bp.delete("<int:task_id>")
@jwt_required()
def delete_task(task_id: int):
	user_id = current_user_id()
	task = Task.query.filter_by(id=task_id, user_id=user_id).first()
	if not task:
		return jsonify({"error": "tarefa não encontrada"}), 404

	db.session.delete(task)
	db.session.commit()
	return "", 204