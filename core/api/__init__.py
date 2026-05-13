"""
API模块初始化文件

整合所有API处理器blueprints。
"""

from flask import Flask

from core.api.handlers.index import index_bp
from core.api.handlers.search import search_bp
from core.api.handlers.university import university_bp
from core.api.handlers.auth import auth_bp
from core.api.handlers.users import users_bp
from core.api.handlers.logs import logs_bp
from core.api.handlers.settings import settings_bp
from core.api.handlers.media import media_bp


def register_api_handlers(app: Flask, services: dict):
    """
    注册所有API处理器到Flask应用
    
    Args:
        app: Flask应用实例
        services: 服务字典，包含所有需要的服务实例
    """
    index_bp.university_service = services.get("university_service")
    search_bp.university_service = services.get("university_service")
    
    university_bp.university_service = services.get("university_service")
    university_bp.log_service = services.get("log_service")
    university_bp.get_current_user = services.get("get_current_user")
    university_bp.get_client_info = services.get("get_client_info")
    university_bp.University = services.get("University")
    university_bp.User = services.get("User")
    university_bp.AppError = services.get("AppError")
    university_bp.logo_dir = services.get("logo_dir")
    
    auth_bp.user_service = services.get("user_service")
    auth_bp.AppError = services.get("AppError")
    
    users_bp.user_service = services.get("user_service")
    users_bp.get_current_user = services.get("get_current_user")
    users_bp.get_client_info = services.get("get_client_info")
    users_bp.User = services.get("User")
    users_bp.AppError = services.get("AppError")
    
    logs_bp.log_service = services.get("log_service")
    logs_bp.get_current_user = services.get("get_current_user")
    logs_bp.User = services.get("User")
    logs_bp.AppError = services.get("AppError")
    
    settings_bp.settings_service = services.get("settings_service")
    settings_bp.university_service = services.get("university_service")
    settings_bp.get_current_user = services.get("get_current_user")
    settings_bp.AppError = services.get("AppError")
    
    media_bp.logo_dir = services.get("logo_dir")
    media_bp.AppError = services.get("AppError")
    
    app.register_blueprint(index_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(university_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(media_bp)


__all__ = [
    "register_api_handlers",
]
