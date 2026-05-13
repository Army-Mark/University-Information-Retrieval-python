"""
学校相关API处理器模块

提供学校的增删改查操作接口。
"""

from flask import Blueprint, jsonify, request, render_template

university_bp = Blueprint("university", __name__, url_prefix="")


def init_university(services: dict):
    """初始化学校路由所需的服务"""
    university_bp.university_service = services.get("university_service")
    university_bp.log_service = services.get("log_service")
    university_bp.get_current_user = services.get("get_current_user")
    university_bp.get_client_info = services.get("get_client_info")
    university_bp.University = services.get("University")
    university_bp.User = services.get("User")
    university_bp.AppError = services.get("AppError")
    university_bp.logo_dir = services.get("logo_dir")


@university_bp.route("/university/<school_id>")
def university_detail(school_id):
    """学校详情页面"""
    school = university_bp.university_service.get_by_id(school_id)
    if not school:
        school = university_bp.university_service.get_by_name(school_id)

    if not school:
        return render_template("not_found.html")

    school_dict = {
        '学校ID': school.id,
        '学校名称': school.name,
        '地址': school.address,
        '类别': school.category,
        '性质': school.nature,
        '归属部门': school.department,
        '标签': school.tags,
        '建校时间': school.founded_year,
        '占地面积': school.area,
        '保研星级': school.baoyan_star,
        '博士点数量': school.phd_count,
        '硕士点数量': school.master_count,
        '国家重点学科数量': school.key_subject_count,
        '软科综合排名': school.rank_ruanke,
        '校友会综合排名': school.rank_xyh,
        'QS世界排名': school.rank_qs,
        'US世界排名': school.rank_us,
        '泰晤士排名': school.rank_times,
        '人气值排名': school.rank_popularity,
        '基本信息': school.basic_info,
        'logo_path': school.logo_path,
    }

    return render_template("university.html", university=school_dict)


@university_bp.route("/edit/<school_id>")
def edit_school(school_id):
    """编辑学校页面"""
    current_user = university_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    school = university_bp.university_service.get_by_id(school_id)
    if not school:
        school = university_bp.university_service.get_by_name(school_id)

    if not school:
        return "School not found", 404

    school_dict = {
        '学校ID': school.id,
        '学校名称': school.name,
        '地址': school.address,
        '类别': school.category,
        '性质': school.nature,
        '归属部门': school.department,
        '标签': school.tags,
        '建校时间': school.founded_year,
        '占地面积': school.area,
        '保研星级': school.baoyan_star,
        '博士点数量': school.phd_count,
        '硕士点数量': school.master_count,
        '国家重点学科数量': school.key_subject_count,
        '软科综合排名': school.rank_ruanke,
        '校友会综合排名': school.rank_xyh,
        'QS世界排名': school.rank_qs,
        'US世界排名': school.rank_us,
        '泰晤士排名': school.rank_times,
        '人气值排名': school.rank_popularity,
        '基本信息': school.basic_info,
        'logo_path': school.logo_path,
    }

    return render_template("university_edit.html", university=school_dict)


@university_bp.route("/save", methods=["POST"])
def save_school():
    """保存学校信息"""
    current_user = university_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()

    university = university_bp.University(
        id=data.get("学校ID"),
        name=data.get("学校名称"),
        address=data.get("地址"),
        category=data.get("类别"),
        nature=data.get("性质"),
        department=data.get("归属部门"),
        tags=data.get("标签"),
        founded_year=data.get("建校时间"),
        area=data.get("占地面积"),
        baoyan_star=data.get("保研星级"),
        phd_count=data.get("博士点数量"),
        master_count=data.get("硕士点数量"),
        key_subject_count=data.get("国家重点学科数量"),
        rank_ruanke=data.get("软科综合排名"),
        rank_xyh=data.get("校友会综合排名"),
        rank_qs=data.get("QS世界排名"),
        rank_us=data.get("US世界排名"),
        rank_times=data.get("泰晤士排名"),
        rank_popularity=data.get("人气值排名"),
        basic_info=data.get("基本信息"),
        logo_path=data.get("logo_path"),
    )

    ip, ua = university_bp.get_client_info()

    user_obj = None
    if current_user:
        user_obj = university_bp.User(
            id=current_user["id"],
            username=current_user["username"],
            role=current_user["role"],
        )

    success, error = university_bp.university_service.update(university, user_obj, ip, ua)

    if error:
        return jsonify(error.to_dict()), error.status_code

    return jsonify({"success": True, "message": "Saved successfully"})


@university_bp.route("/add_school")
def add_school_page():
    """新增学校页面"""
    current_user = university_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    available_id = university_bp.university_service.get_available_id()
    return render_template("add_school.html", available_id=available_id)


@university_bp.route("/add_school", methods=["POST"])
def add_school():
    """新增学校"""
    current_user = university_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.get_json()

    university = university_bp.University(
        id=data.get("学校ID"),
        name=data.get("学校名称"),
        address=data.get("地址"),
        category=data.get("类别"),
        nature=data.get("性质"),
        department=data.get("归属部门"),
        tags=data.get("标签"),
        founded_year=data.get("建校时间"),
        area=data.get("占地面积"),
        baoyan_star=data.get("保研星级"),
        phd_count=data.get("博士点数量"),
        master_count=data.get("硕士点数量"),
        key_subject_count=data.get("国家重点学科数量"),
        rank_ruanke=data.get("软科综合排名"),
        rank_xyh=data.get("校友会综合排名"),
        rank_qs=data.get("QS世界排名"),
        rank_us=data.get("US世界排名"),
        rank_times=data.get("泰晤士排名"),
        rank_popularity=data.get("人气值排名"),
        basic_info=data.get("基本信息"),
        logo_path=data.get("logo_path"),
    )

    ip, ua = university_bp.get_client_info()

    user_obj = None
    if current_user:
        user_obj = university_bp.User(
            id=current_user["id"],
            username=current_user["username"],
            role=current_user["role"],
        )

    created, error = university_bp.university_service.create(university, user_obj, ip, ua)

    if error:
        return jsonify(error.to_dict()), error.status_code

    return jsonify({"success": True, "message": "Added successfully"})


@university_bp.route("/delete_school", methods=["POST"])
def delete_school():
    """删除学校"""
    current_user = university_bp.get_current_user()
    if not current_user:
        return jsonify({"error": "Unauthorized"}), 401
    if current_user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403
    
    data = request.get_json()
    school_id = data.get("school_id")

    if not school_id:
        return jsonify(university_bp.AppError.bad_request("School ID required").to_dict()), 400

    ip, ua = university_bp.get_client_info()

    user_obj = university_bp.User(
        id=current_user["id"],
        username=current_user["username"],
        role=current_user["role"],
    )

    success, error = university_bp.university_service.delete(school_id, user_obj, ip, ua)

    if error:
        return jsonify(error.to_dict()), error.status_code

    return jsonify({"success": True, "message": "Deleted successfully"})
