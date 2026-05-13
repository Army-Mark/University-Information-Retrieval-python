"""
操作日志API处理器模块

提供操作日志的查看和管理功能。
"""

from flask import Blueprint, jsonify, request, render_template

logs_bp = Blueprint("logs", __name__, url_prefix="")


def init_logs(services: dict):
    """初始化日志路由所需的服务"""
    logs_bp.log_service = services.get("log_service")
    logs_bp.get_current_user = services.get("get_current_user")
    logs_bp.User = services.get("User")
    logs_bp.AppError = services.get("AppError")


@logs_bp.route("/operation_logs")
def logs_page():
    """操作日志页面"""
    current_user = logs_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    return render_template("operation_logs.html")


@logs_bp.route("/get_operation_logs", methods=["GET"])
def get_logs():
    """获取操作日志列表"""
    current_user = logs_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    username = None if current_user["role"] == "admin" else current_user["username"]
    logs = logs_bp.log_service.get_all(limit=100, username=username)
    return jsonify({
        "success": True,
        "logs": [l.to_dict() for l in logs],
    })


@logs_bp.route("/delete_operation_logs", methods=["POST"])
def delete_logs():
    """删除操作日志"""
    current_user = logs_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    if current_user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403
    
    data = request.get_json()
    log_ids = data.get("ids", [])

    if not log_ids:
        return jsonify(logs_bp.AppError.bad_request("No log IDs provided").to_dict()), 400

    admin_user = logs_bp.User(
        id=current_user["id"],
        username=current_user["username"],
        role=current_user["role"],
    )

    count, error = logs_bp.log_service.delete_multiple(log_ids, admin_user)

    if error:
        return jsonify(error.to_dict()), error.status_code

    return jsonify({
        "success": True,
        "message": f"Deleted {count} logs",
    })
