from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import html


@dataclass
class User:
    id: Optional[int] = None
    username: str = ""
    password: str = ""
    role: str = "user"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
        }
    
    def escape(self) -> "User":
        """XSS防护：转义字符串字段"""
        return User(
            id=self.id,
            username=html.escape(self.username),
            password=self.password,
            role=html.escape(self.role),
        )


@dataclass
class University:
    id: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    category: Optional[str] = None
    nature: Optional[str] = None
    department: Optional[str] = None
    tags: Optional[str] = None
    founded_year: Optional[str] = None
    area: Optional[str] = None
    baoyan_star: Optional[str] = None
    phd_count: Optional[str] = None
    master_count: Optional[str] = None
    key_subject_count: Optional[str] = None
    rank_ruanke: Optional[str] = None
    rank_xyh: Optional[str] = None
    rank_qs: Optional[str] = None
    rank_us: Optional[str] = None
    rank_times: Optional[str] = None
    rank_popularity: Optional[str] = None
    basic_info: Optional[str] = None
    logo_path: Optional[str] = None
    
    @classmethod
    def from_row(cls, row) -> "University":
        """从数据库行创建对象"""
        return cls(
            id=row.get("学校ID"),
            name=row.get("学校名称"),
            address=row.get("地址"),
            category=row.get("类别"),
            nature=row.get("性质"),
            department=row.get("归属部门"),
            tags=row.get("标签"),
            founded_year=row.get("建校时间"),
            area=row.get("占地面积"),
            baoyan_star=row.get("保研星级"),
            phd_count=row.get("博士点数量"),
            master_count=row.get("硕士点数量"),
            key_subject_count=row.get("国家重点学科数量"),
            rank_ruanke=row.get("软科综合排名"),
            rank_xyh=row.get("校友会综合排名"),
            rank_qs=row.get("QS世界排名"),
            rank_us=row.get("US世界排名"),
            rank_times=row.get("泰晤士排名"),
            rank_popularity=row.get("人气值排名"),
            basic_info=row.get("基本信息"),
            logo_path=row.get("logo_path"),
        )
    
    def to_row(self) -> dict:
        """转换为数据库行格式"""
        return {
            "学校ID": self.id,
            "学校名称": self.name,
            "地址": self.address,
            "类别": self.category,
            "性质": self.nature,
            "归属部门": self.department,
            "标签": self.tags,
            "建校时间": self.founded_year,
            "占地面积": self.area,
            "保研星级": self.baoyan_star,
            "博士点数量": self.phd_count,
            "硕士点数量": self.master_count,
            "国家重点学科数量": self.key_subject_count,
            "软科综合排名": self.rank_ruanke,
            "校友会综合排名": self.rank_xyh,
            "QS世界排名": self.rank_qs,
            "US世界排名": self.rank_us,
            "泰晤士排名": self.rank_times,
            "人气值排名": self.rank_popularity,
            "基本信息": self.basic_info,
            "logo_path": self.logo_path,
        }
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "category": self.category,
            "nature": self.nature,
            "tags": self.tags,
            "founded_year": self.founded_year,
            "area": self.area,
            "basic_info": self.basic_info,
            "logo_path": self.logo_path,
        }
    
    def escape(self) -> "University":
        """XSS防护：转义所有字符串字段"""
        return University(
            id=self.id,
            name=html.escape(self.name) if self.name else None,
            address=html.escape(self.address) if self.address else None,
            category=html.escape(self.category) if self.category else None,
            nature=html.escape(self.nature) if self.nature else None,
            department=html.escape(self.department) if self.department else None,
            tags=html.escape(self.tags) if self.tags else None,
            founded_year=html.escape(self.founded_year) if self.founded_year else None,
            area=html.escape(self.area) if self.area else None,
            baoyan_star=html.escape(self.baoyan_star) if self.baoyan_star else None,
            phd_count=html.escape(self.phd_count) if self.phd_count else None,
            master_count=html.escape(self.master_count) if self.master_count else None,
            key_subject_count=html.escape(self.key_subject_count) if self.key_subject_count else None,
            rank_ruanke=html.escape(self.rank_ruanke) if self.rank_ruanke else None,
            rank_xyh=html.escape(self.rank_xyh) if self.rank_xyh else None,
            rank_qs=html.escape(self.rank_qs) if self.rank_qs else None,
            rank_us=html.escape(self.rank_us) if self.rank_us else None,
            rank_times=html.escape(self.rank_times) if self.rank_times else None,
            rank_popularity=html.escape(self.rank_popularity) if self.rank_popularity else None,
            basic_info=html.escape(self.basic_info) if self.basic_info else None,
            logo_path=html.escape(self.logo_path) if self.logo_path else None,
        )


@dataclass
class OperationLog:
    id: Optional[int] = None
    operation_type: str = ""
    table_name: str = ""
    record_id: Optional[str] = None
    user_id: Optional[int] = None
    username: str = ""
    operation_time: Optional[datetime] = None
    old_data: Optional[str] = None
    new_data: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    
    @classmethod
    def from_row(cls, row) -> "OperationLog":
        return cls(
            id=row.get("id"),
            operation_type=row.get("operation_type"),
            table_name=row.get("table_name"),
            record_id=row.get("record_id"),
            user_id=row.get("user_id"),
            username=row.get("username"),
            operation_time=row.get("operation_time"),
            old_data=row.get("old_data"),
            new_data=row.get("new_data"),
            ip_address=row.get("ip_address"),
            user_agent=row.get("user_agent"),
        )
    
    def to_dict(self) -> dict:
        operation_time_str = None
        if self.operation_time:
            if hasattr(self.operation_time, 'isoformat'):
                operation_time_str = self.operation_time.isoformat()
            else:
                operation_time_str = str(self.operation_time)
        
        return {
            "id": self.id,
            "operation_type": self.operation_type,
            "table_name": self.table_name,
            "record_id": self.record_id,
            "username": self.username,
            "operation_time": operation_time_str,
            "ip_address": self.ip_address,
            "old_data": self.old_data,
            "new_data": self.new_data,
        }


@dataclass
class UserSettings:
    id: Optional[int] = None
    user_id: int = 0
    theme: str = "light"
    language: str = "zh"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_row(cls, row) -> "UserSettings":
        return cls(
            id=row.get("id"),
            user_id=row.get("user_id"),
            theme=row.get("theme"),
            language=row.get("language"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )
    
    def to_dict(self) -> dict:
        return {
            "theme": self.theme,
            "language": self.language,
        }


@dataclass
class Favorite:
    id: Optional[int] = None
    user_id: int = 0
    school_id: str = ""
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_row(cls, row) -> "Favorite":
        return cls(
            id=row.get("id"),
            user_id=row.get("user_id"),
            school_id=row.get("school_id"),
            created_at=row.get("created_at"),
        )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "school_id": self.school_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
