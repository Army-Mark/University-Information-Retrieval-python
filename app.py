"""
Flask应用入口文件

应用程序的主入口点，负责：
1. 加载配置
2. 初始化数据库
3. 初始化服务层
4. 注册API处理器
5. 启动应用

使用方法：
    python app.py

环境变量：
    HOST: 服务器监听地址，默认 0.0.0.0
    PORT: 服务器监听端口，默认 5000
    FLASK_DEBUG: 是否开启调试模式，默认 False
    DB_PATH: 数据库路径，默认 data/school.db
"""

import os
from flask import Flask

from core.config import Config
from core.repository import (
    Database,
    UniversityRepository,
    UserRepository,
    OperationLogRepository,
    UserSettingsRepository,
)
from core.service import (
    UniversityService,
    UserService,
    OperationLogService,
    SettingsService,
)
from core.api.middleware import login_required, admin_required, get_current_user, get_client_info
from core.api import register_api_handlers
from core.models import University, User
from core.pkg.errors import AppError


def create_app(config: Config = None) -> Flask:
    """
    创建并配置Flask应用实例

    Args:
        config: 配置对象，默认从环境变量加载

    Returns:
        配置好的Flask应用实例
    """
    config = config or Config.from_env()

    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    app.config["SESSION_COOKIE_HTTPONLY"] = config.SESSION_COOKIE_HTTPONLY
    app.config["SESSION_COOKIE_SECURE"] = config.SESSION_COOKIE_SECURE
    app.config["SESSION_COOKIE_SAMESITE"] = config.SESSION_COOKIE_SAMESITE

    logo_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo")
    os.makedirs(logo_dir, exist_ok=True)

    db = Database(config.DB_PATH)
    db.ensure_admin_user()

    university_repo = UniversityRepository(db)
    user_repo = UserRepository(db)
    log_repo = OperationLogRepository(db)
    settings_repo = UserSettingsRepository(db)

    university_service = UniversityService(university_repo, log_repo)
    user_service = UserService(user_repo, log_repo)
    log_service = OperationLogService(log_repo)
    settings_service = SettingsService(settings_repo)

    services = {
        "db": db,
        "university_service": university_service,
        "user_service": user_service,
        "log_service": log_service,
        "settings_service": settings_service,
        "login_required": login_required,
        "admin_required": admin_required,
        "get_current_user": get_current_user,
        "get_client_info": get_client_info,
        "University": University,
        "User": User,
        "AppError": AppError,
        "logo_dir": logo_dir,
    }

    register_api_handlers(app, services)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", 5000)),
        debug=os.environ.get("FLASK_DEBUG", "False").lower() == "true",
    )
