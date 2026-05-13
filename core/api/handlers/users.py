"""
用户管理API处理器模块

提供用户的增删改查操作接口。
"""

from flask import Blueprint, jsonify, request, session, render_template

users_bp = Blueprint("users", __name__, url_prefix="")


def init_users(services: dict):
    """初始化用户路由所需的服务"""
    users_bp.user_service = services.get("user_service")
    users_bp.get_current_user = services.get("get_current_user")
    users_bp.get_client_info = services.get("get_client_info")
    users_bp.User = services.get("User")
    users_bp.AppError = services.get("AppError")


@users_bp.route("/account")
def account_page():
    """用户账户管理页面"""
    current_user = users_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    return render_template("account.html")


@users_bp.route("/get_accounts", methods=["POST"])
def get_accounts():
    """获取账户列表"""
    current_user = users_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    current_username = data.get("username", "")
    current_role = data.get("role", "user")
    
    users = users_bp.user_service.get_all()
    
    if current_role != "admin":
        users = [u for u in users if u.username == current_username]
    
    return jsonify({
        "success": True,
        "accounts": [u.to_dict() for u in users],
    })


@users_bp.route("/add_account", methods=["POST"])
def add_account():
    """添加账户"""
    current_user = users_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    if current_user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403
    
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify(users_bp.AppError.bad_request("Username and password required").to_dict()), 400

    ip, ua = users_bp.get_client_info()

    admin_user = users_bp.User(
        id=current_user["id"],
        username=current_user["username"],
        role=current_user["role"],
    )

    created, error = users_bp.user_service.create(username, password, role, admin_user, ip, ua)

    if error:
        return jsonify(error.to_dict()), error.status_code

    return jsonify({"success": True, "message": "Account added successfully"})


@users_bp.route("/update_account", methods=["POST"])
def update_account():
    """更新账户"""
    current_user = users_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    old_username = data.get("oldUsername")
    new_username = data.get("newUsername", "").strip()
    new_password = data.get("newPassword", "")
    new_role = data.get("newRole", "user")
    current_user_role = data.get("currentUserRole", "user")

    if not new_password or not new_username:
        return jsonify(users_bp.AppError.bad_request("New username and password required").to_dict()), 400

    ip, ua = users_bp.get_client_info()

    user_obj = users_bp.User(
        id=current_user["id"],
        username=current_user["username"],
        role=current_user["role"],
    )

    users = users_bp.user_service.get_all()
    target_user = None
    for u in users:
        if u.username == old_username:
            target_user = u
            break

    if not target_user:
        return jsonify(users_bp.AppError.not_found("User not found").to_dict()), 404

    if current_user["role"] != "admin" and current_user["username"] != old_username:
        return jsonify(users_bp.AppError.forbidden("You can only edit your own account").to_dict()), 403

    if current_user["role"] != "admin":
        new_role = target_user.role

    success, error = users_bp.user_service.update(
        target_user.id,
        new_username,
        new_password,
        new_role,
        user_obj,
        ip,
        ua,
    )

    if error:
        return jsonify(error.to_dict()), error.status_code

    if session.get("username") == old_username:
        session["username"] = new_username

    return jsonify({"success": True, "message": "Updated successfully"})


@users_bp.route("/delete_account", methods=["POST"])
def delete_account():
    """删除账户"""
    current_user = users_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    if current_user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403
    
    data = request.get_json()
    username = data.get("username")

    ip, ua = users_bp.get_client_info()

    users = users_bp.user_service.get_all()
    target_user = None
    for u in users:
        if u.username == username:
            target_user = u
            break

    if not target_user:
        return jsonify(users_bp.AppError.not_found("User not found").to_dict()), 404

    admin_user = users_bp.User(
        id=current_user["id"],
        username=current_user["username"],
        role=current_user["role"],
    )

    success, error = users_bp.user_service.delete(target_user.id, admin_user, ip, ua)

    if error:
        return jsonify(error.to_dict()), error.status_code

    return jsonify({"success": True, "message": "Deleted successfully"})
