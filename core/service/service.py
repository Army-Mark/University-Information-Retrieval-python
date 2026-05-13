import os
import re
import json
from typing import List, Optional, Tuple
from werkzeug.security import generate_password_hash, check_password_hash
from core.models import User, University, OperationLog, UserSettings, Favorite
from core.repository import (
    UniversityRepository,
    UserRepository,
    OperationLogRepository,
    UserSettingsRepository,
    FavoriteRepository,
)
from core.pkg.errors import AppError


class PasswordValidator:
    @staticmethod
    def validate(password: str) -> Tuple[bool, Optional[str]]:
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r"[A-Za-z]", password):
            return False, "Password must contain at least one letter"
        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one number"
        return True, None


class UniversityService:
    def __init__(
        self,
        university_repo: UniversityRepository,
        log_repo: OperationLogRepository,
        logo_dir: str = None,
    ):
        self.university_repo = university_repo
        self.log_repo = log_repo
        self.logo_dir = logo_dir
    
    def get_all(self) -> List[University]:
        return self.university_repo.get_all()
    
    def get_by_id(self, school_id: str) -> Optional[University]:
        return self.university_repo.get_by_id(school_id)
    
    def get_by_name(self, name: str) -> Optional[University]:
        return self.university_repo.get_by_name(name)
    
    def search(self, keyword: str) -> List[University]:
        return self.university_repo.search(keyword)
    
    def create(
        self,
        university: University,
        user: Optional[User] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[University, Optional[AppError]]:
        try:
            university = university.escape()
            
            # 检查ID是否已存在
            if self.university_repo.get_by_id(university.id):
                return university, AppError.bad_request("School ID already exists")
            
            if self.university_repo.get_by_name(university.name):
                return university, AppError.bad_request("School name already exists")
            
            created = self.university_repo.create(university)
            
            # 记录操作日志
            if user:
                log = OperationLog(
                    operation_type="create",
                    table_name="universities",
                    record_id=created.id,
                    user_id=user.id,
                    username=user.username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    new_data=json.dumps(university.to_dict(), ensure_ascii=False),
                )
                self.log_repo.create(log)
            
            return created, None
        except Exception as e:
            return university, AppError.internal(f"Failed to create university: {str(e)}")
    
    def update(
        self,
        university: University,
        user: Optional[User] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[bool, Optional[AppError]]:
        try:
            university = university.escape()
            
            old = self.university_repo.get_by_id(university.id)
            if not old:
                return False, AppError.not_found("University not found")
            
            success = self.university_repo.update(university)
            
            if success and user:
                log = OperationLog(
                    operation_type="update",
                    table_name="universities",
                    record_id=university.id,
                    user_id=user.id,
                    username=user.username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    old_data=json.dumps(old.to_dict(), ensure_ascii=False),
                    new_data=json.dumps(university.to_dict(), ensure_ascii=False),
                )
                self.log_repo.create(log)
            
            return success, None
        except Exception as e:
            return False, AppError.internal(f"Failed to update university: {str(e)}")
    
    def delete(
        self,
        school_id: str,
        user: Optional[User] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[bool, Optional[AppError]]:
        try:
            old = self.university_repo.get_by_id(school_id)
            if not old:
                return False, AppError.not_found("University not found")
            
            success = self.university_repo.delete(school_id)
            
            if success:
                if self.logo_dir:
                    for ext in ['.png', '.jpg', '.jpeg', '.gif']:
                        logo_path = os.path.join(self.logo_dir, f"{school_id}{ext}")
                        if os.path.exists(logo_path):
                            try:
                                os.remove(logo_path)
                            except Exception:
                                pass
                
                if user:
                    log = OperationLog(
                        operation_type="delete",
                        table_name="universities",
                        record_id=school_id,
                        user_id=user.id,
                        username=user.username,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        old_data=json.dumps(old.to_dict(), ensure_ascii=False),
                    )
                    self.log_repo.create(log)
            
            return success, None
        except Exception as e:
            return False, AppError.internal(f"Failed to delete university: {str(e)}")
    
    def get_available_id(self) -> int:
        return self.university_repo.get_available_id()


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        log_repo: OperationLogRepository,
    ):
        self.user_repo = user_repo
        self.log_repo = log_repo
    
    def authenticate(self, username: str, password: str) -> Tuple[Optional[User], Optional[AppError]]:
        user = self.user_repo.get_by_username(username)
        if not user:
            return None, AppError.unauthorized("Invalid username or password")
        
        # 检查是否是已加密的密码
        if user.password.startswith('pbkdf2:sha256:'):
            if not check_password_hash(user.password, password):
                return None, AppError.unauthorized("Invalid username or password")
        else:
            # 兼容旧密码（未加密）
            if user.password != password:
                return None, AppError.unauthorized("Invalid username or password")
        
        return user, None
    
    def get_all(self) -> List[User]:
        users = self.user_repo.get_all()
        return users
    
    def get_by_username(self, username: str) -> Optional[User]:
        return self.user_repo.get_by_username(username)
    
    def create(
        self,
        username: str,
        password: str,
        role: str = "user",
        admin_user: Optional[User] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[Optional[User], Optional[AppError]]:
        try:
            valid, msg = PasswordValidator.validate(password)
            if not valid:
                return None, AppError.bad_request(msg)
            
            if self.user_repo.get_by_username(username):
                return None, AppError.bad_request("Username already exists")
            
            # 使用 werkzeug 安全加密密码
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
            user = User(username=username, password=hashed_password, role=role)
            user = user.escape()
            created = self.user_repo.create(user)
            
            if admin_user:
                log = OperationLog(
                    operation_type="create",
                    table_name="users",
                    record_id=str(created.id),
                    user_id=admin_user.id,
                    username=admin_user.username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    new_data=str(created.to_dict()),
                )
                self.log_repo.create(log)
            
            return created, None
        except Exception as e:
            return None, AppError.internal(f"Failed to create user: {str(e)}")
    
    def update(
        self,
        user_id: int,
        new_username: str,
        new_password: str,
        new_role: Optional[str] = None,
        current_user: Optional[User] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[bool, Optional[AppError]]:
        try:
            old_user = self.user_repo.get_by_id(user_id)
            if not old_user:
                return False, AppError.not_found("User not found")
            
            # 验证密码
            valid, msg = PasswordValidator.validate(new_password)
            if not valid:
                return False, AppError.bad_request(msg)
            
            # 检查用户名冲突
            if new_username != old_user.username:
                if self.user_repo.get_by_username(new_username):
                    return False, AppError.bad_request("Username already exists")
            
            # 权限检查
            if current_user and current_user.role != "admin" and current_user.id != user_id:
                return False, AppError.forbidden("Permission denied")
            
            # 使用 werkzeug 安全加密密码
            hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            
            updated_user = User(
                id=user_id,
                username=new_username,
                password=hashed_password,
                role=new_role if new_role and current_user and current_user.role == "admin" else old_user.role,
            )
            updated_user = updated_user.escape()
            
            success = self.user_repo.update(updated_user)
            
            if success and current_user:
                log = OperationLog(
                    operation_type="update",
                    table_name="users",
                    record_id=str(user_id),
                    user_id=current_user.id,
                    username=current_user.username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    old_data=json.dumps(old_user.to_dict(), ensure_ascii=False),
                    new_data=json.dumps(updated_user.to_dict(), ensure_ascii=False),
                )
                self.log_repo.create(log)
            
            return success, None
        except Exception as e:
            return False, AppError.internal(f"Failed to update user: {str(e)}")
    
    def delete(
        self,
        user_id: int,
        admin_user: User,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Tuple[bool, Optional[AppError]]:
        try:
            if user_id == admin_user.id:
                return False, AppError.bad_request("Cannot delete your own account")
            
            old_user = self.user_repo.get_by_id(user_id)
            if not old_user:
                return False, AppError.not_found("User not found")
            
            success = self.user_repo.delete(user_id)
            
            if success:
                log = OperationLog(
                    operation_type="delete",
                    table_name="users",
                    record_id=str(user_id),
                    user_id=admin_user.id,
                    username=admin_user.username,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    old_data=json.dumps(old_user.to_dict(), ensure_ascii=False),
                )
                self.log_repo.create(log)
            
            return success, None
        except Exception as e:
            return False, AppError.internal(f"Failed to delete user: {str(e)}")


class OperationLogService:
    def __init__(self, log_repo: OperationLogRepository):
        self.log_repo = log_repo
    
    def get_all(self, limit: int = 100, username: Optional[str] = None) -> List[OperationLog]:
        return self.log_repo.get_all(limit, username)
    
    def delete(self, log_id: int, admin_user: User) -> Tuple[bool, Optional[AppError]]:
        if admin_user.role != "admin":
            return False, AppError.forbidden("Permission denied")
        success = self.log_repo.delete(log_id)
        return success, None
    
    def delete_multiple(
        self,
        log_ids: List[int],
        admin_user: User,
    ) -> Tuple[int, Optional[AppError]]:
        if admin_user.role != "admin":
            return 0, AppError.forbidden("Permission denied")
        count = self.log_repo.delete_multiple(log_ids)
        return count, None


class SettingsService:
    def __init__(self, settings_repo: UserSettingsRepository):
        self.settings_repo = settings_repo
    
    def get(self, user_id: int) -> UserSettings:
        settings = self.settings_repo.get_by_user_id(user_id)
        if settings:
            return settings
        return UserSettings(user_id=user_id)
    
    def save(
        self,
        user_id: int,
        theme: str,
        language: str,
    ) -> Tuple[UserSettings, Optional[AppError]]:
        try:
            if theme not in ["light", "dark"]:
                theme = "light"
            if language not in ["zh", "en"]:
                language = "zh"
            
            settings = UserSettings(user_id=user_id, theme=theme, language=language)
            saved = self.settings_repo.create_or_update(settings)
            return saved, None
        except Exception as e:
            return UserSettings(user_id=user_id), AppError.internal(f"Failed to save settings: {str(e)}")


class FavoriteService:
    def __init__(
        self,
        favorite_repo: FavoriteRepository,
        university_repo: UniversityRepository,
    ):
        self.favorite_repo = favorite_repo
        self.university_repo = university_repo
    
    def get_user_favorites(self, user_id: int) -> List[dict]:
        return self.favorite_repo.get_with_details(user_id)
    
    def add(
        self,
        user_id: int,
        school_id: str,
    ) -> Tuple[Optional[Favorite], Optional[AppError]]:
        try:
            university = self.university_repo.get_by_id(school_id)
            if not university:
                return None, AppError.not_found("University not found")
            
            favorite = Favorite(user_id=user_id, school_id=school_id)
            created = self.favorite_repo.create(favorite)
            return created, None
        except Exception as e:
            return None, AppError.bad_request("Already favorited")
    
    def remove(
        self,
        user_id: int,
        school_id: str,
    ) -> Tuple[bool, Optional[AppError]]:
        try:
            success = self.favorite_repo.delete(user_id, school_id)
            if not success:
                return False, AppError.not_found("Favorite not found")
            return success, None
        except Exception as e:
            return False, AppError.internal(f"Failed to remove favorite: {str(e)}")
