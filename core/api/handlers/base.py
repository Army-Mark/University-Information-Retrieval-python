from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
)

from core.service import SettingsService, FavoriteService, UniversityService
from core.api.middleware import login_required, get_current_user
from core.pkg.errors import AppError


def create_api_routes(
    settings_service: SettingsService,
    favorite_service: FavoriteService,
    university_service: UniversityService,
) -> Blueprint:
    bp = Blueprint("api", __name__)
    
    @bp.route("/")
    def index():
        return render_template("index.html")
    
    @bp.route("/search")
    def search():
        keyword = request.args.get("keyword", "").strip()
        if not keyword:
            return jsonify([])
        
        schools = university_service.search(keyword)
        results = []
        for school in schools:
            results.append({
                "id": school.id,
                "name": school.name,
            })
        
        # 优先匹配精确结果
        exact_id = next((s for s in results if s["id"] == keyword), None)
        if exact_id:
            results.remove(exact_id)
            results.insert(0, exact_id)
        
        return jsonify(results)
    
    @bp.route("/api/scrolling_data")
    def scrolling_data():
        schools = university_service.get_all()
        data = []
        for school in schools:
            data.append({
                "学校ID": school.id,
                "学校名称": school.name,
                "地址": school.address,
                "类别": school.category,
                "性质": school.nature,
            })
        return jsonify({
            "data": data,
            "position": 0,
        })
    
    @bp.route("/api/scrolling_position", methods=["POST"])
    def update_scrolling_position():
        data = request.get_json()
        return jsonify({"success": True})
    
    @bp.route("/api/settings", methods=["GET"])
    @login_required
    def get_settings():
        current_user = get_current_user()
        settings = settings_service.get(current_user["id"])
        return jsonify({
            "success": True,
            "settings": settings.to_dict(),
        })
    
    @bp.route("/api/settings", methods=["POST"])
    @login_required
    def save_settings():
        current_user = get_current_user()
        data = request.get_json()
        theme = data.get("theme", "light")
        language = data.get("language", "zh")
        
        settings, error = settings_service.save(
            current_user["id"],
            theme,
            language,
        )
        
        if error:
            return jsonify(error.to_dict()), error.status_code
        
        return jsonify({
            "success": True,
            "settings": settings.to_dict(),
        })
    
    @bp.route("/api/favorites", methods=["GET"])
    @login_required
    def get_favorites():
        current_user = get_current_user()
        favorites = favorite_service.get_user_favorites(current_user["id"])
        return jsonify({
            "success": True,
            "favorites": favorites,
        })
    
    @bp.route("/api/favorites", methods=["POST"])
    @login_required
    def add_favorite():
        current_user = get_current_user()
        data = request.get_json()
        school_id = data.get("school_id")
        
        if not school_id:
            return jsonify(AppError.bad_request("School ID required").to_dict()), 400
        
        favorite, error = favorite_service.add(current_user["id"], school_id)
        
        if error:
            return jsonify(error.to_dict()), error.status_code
        
        return jsonify({
            "success": True,
            "message": "Added to favorites",
        })
    
    @bp.route("/api/favorites/<school_id>", methods=["DELETE"])
    @login_required
    def remove_favorite(school_id):
        current_user = get_current_user()
        success, error = favorite_service.remove(current_user["id"], school_id)
        
        if error:
            return jsonify(error.to_dict()), error.status_code
        
        return jsonify({
            "success": True,
            "message": "Removed from favorites",
        })
    
    return bp
