import sqlite3
from typing import List, Optional
from contextlib import contextmanager
import os

from core.models import User, University, OperationLog, UserSettings, Favorite


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_db(self):
        """初始化数据库表结构"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 创建操作日志表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS operation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_type TEXT NOT NULL,
                    table_name TEXT NOT NULL,
                    record_id TEXT,
                    user_id INTEGER,
                    username TEXT,
                    operation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    old_data TEXT,
                    new_data TEXT,
                    ip_address TEXT,
                    user_agent TEXT
                )
            ''')
            
            # 创建用户设置表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    theme TEXT DEFAULT 'light',
                    language TEXT DEFAULT 'zh',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id)
                )
            ''')
            
            # 创建收藏表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    school_id TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, school_id)
                )
            ''')
            
            # 检查users表是否有role字段
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            if "role" not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
            
            # 创建索引
            try:
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_school_id ON universities(学校ID)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_school_name ON universities(学校名称)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_operation_logs_time ON operation_logs(operation_time)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id)')
            except Exception:
                pass
    
    def ensure_admin_user(self):
        """确保存在管理员用户"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin", "admin", "admin")
                )


class UniversityRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def get_all(self) -> List[University]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM universities")
            universities = []
            for row in cursor.fetchall():
                universities.append(University.from_row(dict(row)))
            return universities
    
    def get_by_id(self, school_id: str) -> Optional[University]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM universities WHERE 学校ID = ?", (school_id,))
            row = cursor.fetchone()
            if row:
                return University.from_row(dict(row))
            return None
    
    def get_by_name(self, name: str) -> Optional[University]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM universities WHERE 学校名称 = ?", (name,))
            row = cursor.fetchone()
            if row:
                return University.from_row(dict(row))
            return None
    
    def search(self, keyword: str) -> List[University]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM universities WHERE 学校名称 LIKE ? OR 学校ID LIKE ?",
                (f"%{keyword}%", f"{keyword}%")
            )
            universities = []
            for row in cursor.fetchall():
                universities.append(University.from_row(dict(row)))
            return universities
    
    def create(self, university: University) -> University:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            row = university.to_row()
            columns = list(row.keys())
            placeholders = ", ".join("?" * len(columns))
            values = list(row.values())
            sql = f"INSERT INTO universities ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            return university
    
    def update(self, university: University) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            row = university.to_row()
            update_fields = []
            values = []
            for key, value in row.items():
                if key != "学校ID":
                    update_fields.append(f"{key} = ?")
                    values.append(value)
            values.append(university.id)
            sql = f"UPDATE universities SET {', '.join(update_fields)} WHERE 学校ID = ?"
            cursor.execute(sql, values)
            return cursor.rowcount > 0
    
    def delete(self, school_id: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM universities WHERE 学校ID = ?", (school_id,))
            return cursor.rowcount > 0
    
    def get_max_id(self) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(CAST(学校ID AS INTEGER)) FROM universities WHERE 学校ID GLOB '[0-9]*'")
            result = cursor.fetchone()[0]
            return int(result) if result else 0
    
    def get_available_id(self) -> int:
        used_ids = set()
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 学校ID FROM universities WHERE 学校ID GLOB '[0-9]*'")
            for row in cursor.fetchall():
                try:
                    used_ids.add(int(row[0]))
                except (ValueError, TypeError):
                    pass
        
        for i in range(1, max(used_ids, default=0) + 2):
            if i not in used_ids:
                return i
        return 1


class UserRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def get_all(self) -> List[User]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, role FROM users")
            users = []
            for row in cursor.fetchall():
                row_dict = dict(row)
                users.append(User(
                    id=row_dict["id"],
                    username=row_dict["username"],
                    password=row_dict["password"],
                    role=row_dict.get("role", "user"),
                ))
            return users
    
    def get_by_username(self, username: str) -> Optional[User]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                row_dict = dict(row)
                return User(
                    id=row_dict["id"],
                    username=row_dict["username"],
                    password=row_dict["password"],
                    role=row_dict.get("role", "user"),
                )
            return None
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, role FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                row_dict = dict(row)
                return User(
                    id=row_dict["id"],
                    username=row_dict["username"],
                    password=row_dict["password"],
                    role=row_dict.get("role", "user"),
                )
            return None
    
    def create(self, user: User) -> User:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (user.username, user.password, user.role)
            )
            user.id = cursor.lastrowid
            return user
    
    def update(self, user: User) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET username = ?, password = ?, role = ? WHERE id = ?",
                (user.username, user.password, user.role, user.id)
            )
            return cursor.rowcount > 0
    
    def delete(self, user_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return cursor.rowcount > 0


class OperationLogRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def get_all(self, limit: int = 100, username: Optional[str] = None) -> List[OperationLog]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            if username:
                cursor.execute(
                    "SELECT * FROM operation_logs WHERE username = ? ORDER BY operation_time DESC LIMIT ?",
                    (username, limit)
                )
            else:
                cursor.execute(
                    "SELECT * FROM operation_logs ORDER BY operation_time DESC LIMIT ?",
                    (limit,)
                )
            logs = []
            for row in cursor.fetchall():
                logs.append(OperationLog.from_row(dict(row)))
            return logs
    
    def create(self, log: OperationLog) -> OperationLog:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO operation_logs 
                (operation_type, table_name, record_id, user_id, username, old_data, new_data, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                log.operation_type,
                log.table_name,
                log.record_id,
                log.user_id,
                log.username,
                log.old_data,
                log.new_data,
                log.ip_address,
                log.user_agent,
            ))
            log.id = cursor.lastrowid
            return log
    
    def delete(self, log_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM operation_logs WHERE id = ?", (log_id,))
            return cursor.rowcount > 0
    
    def delete_multiple(self, log_ids: List[int]) -> int:
        if not log_ids:
            return 0
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            placeholders = ", ".join("?" for _ in log_ids)
            cursor.execute(f"DELETE FROM operation_logs WHERE id IN ({placeholders})", log_ids)
            return cursor.rowcount


class UserSettingsRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def get_by_user_id(self, user_id: int) -> Optional[UserSettings]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return UserSettings.from_row(dict(row))
            return None
    
    def create(self, settings: UserSettings) -> UserSettings:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_settings (user_id, theme, language) VALUES (?, ?, ?)",
                (settings.user_id, settings.theme, settings.language)
            )
            settings.id = cursor.lastrowid
            return settings
    
    def update(self, settings: UserSettings) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_settings 
                SET theme = ?, language = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (settings.theme, settings.language, settings.user_id))
            return cursor.rowcount > 0
    
    def create_or_update(self, settings: UserSettings) -> UserSettings:
        existing = self.get_by_user_id(settings.user_id)
        if existing:
            settings.id = existing.id
            self.update(settings)
            return settings
        else:
            return self.create(settings)


class FavoriteRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def get_by_user_id(self, user_id: int) -> List[Favorite]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM favorites WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
            favorites = []
            for row in cursor.fetchall():
                favorites.append(Favorite.from_row(dict(row)))
            return favorites
    
    def get_with_details(self, user_id: int) -> List[dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT f.id, f.school_id, f.created_at,
                       u.学校名称 AS school_name, u.地址 AS address
                FROM favorites f
                JOIN universities u ON f.school_id = u.学校ID
                WHERE f.user_id = ?
                ORDER BY f.created_at DESC
            ''', (user_id,))
            return [
                {
                    "id": row["id"],
                    "school_id": row["school_id"],
                    "school_name": row["school_name"],
                    "address": row["address"],
                    "created_at": row["created_at"],
                }
                for row in cursor.fetchall()
            ]
    
    def create(self, favorite: Favorite) -> Favorite:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO favorites (user_id, school_id) VALUES (?, ?)",
                (favorite.user_id, favorite.school_id)
            )
            favorite.id = cursor.lastrowid
            return favorite
    
    def delete(self, user_id: int, school_id: str) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM favorites WHERE user_id = ? AND school_id = ?",
                (user_id, school_id)
            )
            return cursor.rowcount > 0
