"""
搜索API处理器模块

提供学校搜索功能，支持关键字搜索、ID搜索和模糊匹配。
"""

from flask import Blueprint, jsonify, request

search_bp = Blueprint("search", __name__, url_prefix="")


def init_search(services: dict):
    """初始化搜索路由所需的服务"""
    search_bp.university_service = services.get("university_service")


@search_bp.route("/search")
def search():
    """处理搜索请求，返回匹配的学校列表"""
    keyword = request.args.get("keyword", "").strip()
    if not keyword:
        return jsonify([])

    schools = search_bp.university_service.search(keyword)
    results = []
    for school in schools:
        results.append({
            "id": school.id,
            "name": school.name,
            "match_type": None,
        })

    is_id_search = keyword.isdigit()

    exact_match = None
    id_match_list = []
    fuzzy_match_list = []

    for item in results:
        item_id = str(item["id"])
        item_name = item["name"]

        if is_id_search:
            if item_id == keyword:
                exact_match = item
                item["match_type"] = "exact"
            elif item_id.startswith(keyword):
                id_match_list.append(item)
                item["match_type"] = "id_match"
        else:
            if item_name == keyword:
                exact_match = item
                item["match_type"] = "exact"
            elif keyword.lower() in item_name.lower():
                fuzzy_match_list.append(item)
                item["match_type"] = "fuzzy"

    final_results = []
    if exact_match:
        final_results.append(exact_match)
    if is_id_search:
        final_results.extend(id_match_list)
    else:
        final_results.extend(fuzzy_match_list)

    return jsonify(final_results)
