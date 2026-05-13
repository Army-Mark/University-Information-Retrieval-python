"""
首页API处理器模块

提供应用首页的渲染和展示功能。
"""

from flask import Blueprint, render_template

index_bp = Blueprint("index", __name__, url_prefix="")


@index_bp.route("/")
def index():
    """渲染并返回首页模板"""
    return render_template("index.html")
