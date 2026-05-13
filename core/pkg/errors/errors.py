from http import HTTPStatus
from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class AppError:
    status_code: int
    message: str
    error_code: str
    details: Optional[Any] = None
    
    @classmethod
    def bad_request(cls, message: str = "Bad Request", details: Optional[Any] = None) -> "AppError":
        return cls(
            status_code=HTTPStatus.BAD_REQUEST,
            message=message,
            error_code="BAD_REQUEST",
            details=details,
        )
    
    @classmethod
    def unauthorized(cls, message: str = "Unauthorized", details: Optional[Any] = None) -> "AppError":
        return cls(
            status_code=HTTPStatus.UNAUTHORIZED,
            message=message,
            error_code="UNAUTHORIZED",
            details=details,
        )
    
    @classmethod
    def forbidden(cls, message: str = "Forbidden", details: Optional[Any] = None) -> "AppError":
        return cls(
            status_code=HTTPStatus.FORBIDDEN,
            message=message,
            error_code="FORBIDDEN",
            details=details,
        )
    
    @classmethod
    def not_found(cls, message: str = "Not Found", details: Optional[Any] = None) -> "AppError":
        return cls(
            status_code=HTTPStatus.NOT_FOUND,
            message=message,
            error_code="NOT_FOUND",
            details=details,
        )
    
    @classmethod
    def internal(cls, message: str = "Internal Server Error", details: Optional[Any] = None) -> "AppError":
        return cls(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message=message,
            error_code="INTERNAL_SERVER_ERROR",
            details=details,
        )
    
    def to_dict(self) -> dict:
        result = {
            "success": False,
            "error": self.error_code,
            "message": self.message,
        }
        if self.details:
            result["details"] = self.details
        return result
