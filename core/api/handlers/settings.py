"""
设置API处理器模块

提供用户设置功能的API接口。
"""

from flask import Blueprint, jsonify, request

settings_bp = Blueprint("settings", __name__, url_prefix="")


def init_settings(services: dict):
    """初始化设置路由所需的服务"""
    settings_bp.settings_service = services.get("settings_service")
    settings_bp.university_service = services.get("university_service")
    settings_bp.get_current_user = services.get("get_current_user")
    settings_bp.AppError = services.get("AppError")


@settings_bp.route("/api/scrolling_data")
def scrolling_data():
    """获取滚动显示的学校数据"""
    schools = settings_bp.university_service.get_all()
    data = []
    for school in schools:
        data.append({
            "学校ID": school.id,
            "学校名称": school.name,
            "地址": school.address,
            "类别": school.category,
            "性质": school.nature,
        })
    return jsonify({
        "data": data,
        "position": 0,
    })


@settings_bp.route("/api/scrolling_position", methods=["POST"])
def update_scrolling_position():
    """更新滚动位置"""
    return jsonify({"success": True})


@settings_bp.route("/api/settings", methods=["GET"])
def get_settings():
    """获取用户设置"""
    current_user = settings_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    settings = settings_bp.settings_service.get(current_user["id"])
    return jsonify({
        "success": True,
        "settings": settings.to_dict(),
    })


@settings_bp.route("/api/settings", methods=["POST"])
def save_settings():
    """保存用户设置"""
    current_user = settings_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()
    theme = data.get("theme", "light")
    language = data.get("language", "zh")

    settings, error = settings_bp.settings_service.save(
        current_user["id"],
        theme,
        language,
    )

    if error:
        return jsonify(error.to_dict()), error.status_code

    return jsonify({
        "success": True,
        "settings": settings.to_dict(),
    })
