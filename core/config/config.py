import os
from dataclasses import dataclass
from typing import Optional


def get_project_root() -> str:
    """获取项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class Config:
    PORT: int = 5000
    HOST: str = "0.0.0.0"
    DB_PATH: str = "data/school.db"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    FLASK_DEBUG: bool = False
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_SAMESITE: str = "Lax"
    
    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载配置"""
        db_path = os.environ.get("DB_PATH", "data/school.db")
        
        if not os.path.isabs(db_path):
            db_path = os.path.join(get_project_root(), db_path)
        
        return cls(
            PORT=int(os.environ.get("PORT", 5000)),
            HOST=os.environ.get("HOST", "0.0.0.0"),
            DB_PATH=db_path,
            SECRET_KEY=os.environ.get("SECRET_KEY", "your-secret-key-change-in-production"),
            FLASK_DEBUG=os.environ.get("FLASK_DEBUG", "False").lower() == "true",
        )
