from functools import wraps
from flask import request, jsonify, session
from typing import Callable

from core.pkg.errors import AppError


def login_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            if request.is_json or request.accept_mimetypes.accept_json:
                return jsonify(AppError.unauthorized().to_dict()), 401
            return f(*args, **kwargs)
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return jsonify(AppError.unauthorized().to_dict()), 401
        
        role = session.get("role")
        if role != "admin":
            return jsonify(AppError.forbidden("Only admin can perform this action").to_dict()), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def get_current_user() -> dict:
    if session.get("logged_in"):
        return {
            "id": session.get("user_id"),
            "username": session.get("username"),
            "role": session.get("role"),
        }
    return None


def get_client_info() -> tuple:
    """获取客户端信息"""
    return (
        request.remote_addr or "unknown",
        request.headers.get("User-Agent", "unknown")[:200],
    )
