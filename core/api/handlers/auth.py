"""
认证API处理器模块

提供用户登录、登出和状态检查功能。
"""

from flask import Blueprint, jsonify, request, session

auth_bp = Blueprint("auth", __name__, url_prefix="")


def init_auth(services: dict):
    """初始化认证路由所需的服务"""
    auth_bp.user_service = services.get("user_service")
    auth_bp.AppError = services.get("AppError")


@auth_bp.route("/login", methods=["POST"])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request"}), 400

        username = data.get("username", "").strip()
        password = data.get("password", "")

        user, error = auth_bp.user_service.authenticate(username, password)

        if error or not user:
            return jsonify(auth_bp.AppError.unauthorized("Invalid username or password").to_dict()), 401

        session["logged_in"] = True
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        return jsonify({"success": True, "message": "Login successful", "role": user.role})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """用户登出"""
    session.clear()
    return jsonify({"success": True, "message": "Logged out"})


@auth_bp.route("/check_login", methods=["GET"])
def check_login():
    """检查登录状态"""
    if session.get("logged_in"):
        return jsonify({
            "success": True,
            "logged_in": True,
            "username": session.get("username"),
            "role": session.get("role", "user"),
        })
    return jsonify({"logged_in": False})
