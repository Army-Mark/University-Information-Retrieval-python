"""
媒体文件API处理器模块

提供Logo上传和访问功能。
"""

import os
from flask import Blueprint, jsonify, request, send_from_directory

media_bp = Blueprint("media", __name__, url_prefix="")


def init_media(services: dict):
    """初始化媒体路由所需的服务"""
    media_bp.logo_dir = services.get("logo_dir")
    media_bp.AppError = services.get("AppError")


def allowed_file(filename: str) -> bool:
    """检查文件类型是否允许"""
    allowed_extensions = {"png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


@media_bp.route("/upload_logo", methods=["POST"])
def upload_logo():
    """上传学校Logo"""
    if "logo" not in request.files:
        return jsonify({"success": False, "message": "No file provided"}), 400

    file = request.files["logo"]
    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Invalid file type"}), 400

    school_id = request.form.get("available_id", "")
    ext = os.path.splitext(file.filename)[1]

    if school_id:
        filename = f"{school_id}{ext}"
    else:
        filename = file.filename

    filepath = os.path.join(media_bp.logo_dir, filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    file.save(filepath)

    if os.path.getsize(filepath) > 500 * 1024:
        os.remove(filepath)
        return jsonify({"success": False, "message": "File too large"}), 400

    return jsonify({
        "success": True,
        "filename": filename,
        "logo_id": school_id
    })


@media_bp.route("/logo/<filename>")
def serve_logo(filename):
    """访问学校Logo"""
    return send_from_directory(media_bp.logo_dir, filename)
