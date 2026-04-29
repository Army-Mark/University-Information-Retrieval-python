from flask import Flask, render_template, request, jsonify, send_from_directory, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

app.static_folder = 'static'

# 从环境变量读取数据库路径，默认使用 'school.db'
DB_PATH = os.environ.get('DB_PATH', 'school.db')

# 全局变量，延迟加载
_universities = None
_users = None

# 全局变量存储滚动位置
_scrolling_position = 0

def load_scrolling_data():
    """
    从数据库加载学校数据，只返回学校ID、学校名称、地址、类别、性质五项
    """
    data = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 学校ID, 学校名称, 地址, 类别, 性质 FROM universities')
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            data.append({
                '学校ID': row['学校ID'],
                '学校名称': row['学校名称'],
                '地址': row['地址'],
                '类别': row['类别'],
                '性质': row['性质']
            })
    except Exception as e:
        print(f'加载滚动数据错误: {e}')
    return data

def get_scrolling_position():
    """
    获取当前滚动位置
    """
    global _scrolling_position
    return _scrolling_position

def set_scrolling_position(position):
    """
    设置滚动位置
    """
    global _scrolling_position
    data = load_scrolling_data()
    if data:
        _scrolling_position = position % len(data)
    else:
        _scrolling_position = 0

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM universities')
    rows = cursor.fetchall()
    conn.close()
    data = []
    for row in rows:
        data.append(dict(row))
    return data

def load_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users')
    rows = cursor.fetchall()
    conn.close()
    users = {}
    for row in rows:
        users[row['username']] = row['password']
    return users

def get_user_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users')
    rows = cursor.fetchall()
    conn.close()
    users = []
    for row in rows:
        users.append({'username': row['username'], 'password': row['password']})
    return users

def save_users(users_list):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users')
        for user in users_list:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                          (user['username'], user['password']))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f'保存用户错误: {e}')
        return False

def get_universities():
    """延迟加载学校数据"""
    global _universities
    if _universities is None:
        _universities = load_data()
    return _universities

def get_users():
    """延迟加载用户数据"""
    global _users
    if _users is None:
        _users = load_users()
    return _users

# 为了保持向后兼容，在模块级别提供访问
universities = property(get_universities)

@app.route('/logo/<path:filename>')
def serve_logo(filename):
    return send_from_directory('logo', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        return jsonify([])
    
    universities_list = get_universities()
    results = []
    for uni in universities_list:
        school_id = uni['学校ID']
        school_name = uni['学校名称']
        
        if keyword == school_id:
            results.insert(0, {
                'id': school_id,
                'name': school_name,
                'match_type': 'exact_id'
            })
        elif keyword.isdigit() and keyword in school_id:
            results.append({
                'id': school_id,
                'name': school_name,
                'match_type': 'partial_id'
            })
        elif keyword in school_name:
            results.append({
                'id': school_id,
                'name': school_name,
                'match_type': 'name'
            })
    return jsonify(results)

@app.route('/university/<id>')
def university(id):
    universities_list = get_universities()
    for uni in universities_list:
        if uni.get('学校ID') == id:
            return render_university(uni)
    
    for uni in universities_list:
        if uni.get('学校名称') == id:
            return render_university(uni)
    
    return render_template('not_found.html')

def render_university(uni):
    tags = uni.get('标签', '').split(', ') if uni.get('标签') else []
    
    rankings = [
        {'name': '软科综合', 'value': uni.get('软科综合排名', '') if uni.get('软科综合排名', '') != '0' else ''},
        {'name': '校友会综合', 'value': uni.get('校友会综合排名', '') if uni.get('校友会综合排名', '') != '0' else ''},
        {'name': 'QS世界', 'value': uni.get('QS世界排名', '') if uni.get('QS世界排名', '') != '0' else ''},
        {'name': 'US世界', 'value': uni.get('US世界排名', '') if uni.get('US世界排名', '') != '0' else ''},
        {'name': '泰晤士 (大陆)', 'value': uni.get('泰晤士排名', '') if uni.get('泰晤士排名', '') != '0' else ''},
        {'name': '人气值排名', 'value': uni.get('人气值排名', '') if uni.get('人气值排名', '') != '0' else ''}
    ]
    
    special_tags = []
    if uni.get('是否985') == '是' or uni.get('985') == '是':
        special_tags.append('985')
    if uni.get('是否211') == '是' or uni.get('211') == '是':
        special_tags.append('211')
    for tag in tags:
        if tag == '985' or tag == '211':
            if tag not in special_tags:
                special_tags.append(tag)
    for tag in tags:
        if tag not in special_tags:
            special_tags.append(tag)
    
    return render_template('university.html', 
                       university=uni, 
                       tags=special_tags,
                       rankings=rankings)

@app.route('/edit/<id>')
def edit_university(id):
    universities_list = get_universities()
    for uni in universities_list:
        if uni.get('学校ID') == id:
            return render_template('university_edit.html', university=uni)
    
    for uni in universities_list:
        if uni.get('学校名称') == id:
            return render_template('university_edit.html', university=uni)
    
    return '学校不存在', 404

@app.route('/save', methods=['POST'])
def save_university():
    global _universities
    try:
        data = request.get_json()
        school_id = data.get('学校ID')
        
        if not school_id:
            return jsonify({'success': False, 'message': '学校ID不能为空'})
        
        universities_list = get_universities()
        updated = False
        for i, uni in enumerate(universities_list):
            if uni.get('学校ID') == school_id:
                for key in data:
                    universities_list[i][key] = data[key]
                updated = True
                break
        
        if not updated:
            return jsonify({'success': False, 'message': '未找到该学校'})
        
        if save_to_db(school_id, data):
            _universities = universities_list
            return jsonify({'success': True, 'message': '保存成功'})
        else:
            return jsonify({'success': False, 'message': '保存到数据库失败'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def save_to_db(school_id, data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        update_fields = []
        values = []
        for key, value in data.items():
            if key != 'id':
                update_fields.append(f'{key} = ?')
                values.append(value)
        
        values.append(school_id)
        
        sql = f"UPDATE universities SET {', '.join(update_fields)} WHERE 学校ID = ?"
        cursor.execute(sql, values)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f'保存数据库错误: {e}')
        return False

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    users_dict = get_users()
    if username in users_dict and users_dict[username] == password:
        session['logged_in'] = True
        session['username'] = username
        return jsonify({'success': True, 'message': '登录成功'})
    else:
        return jsonify({'success': False, 'message': '用户名或密码错误'})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({'success': True, 'message': '退出成功'})

@app.route('/check_login', methods=['GET'])
def check_login():
    if session.get('logged_in'):
        return jsonify({'logged_in': True, 'username': session.get('username')})
    else:
        return jsonify({'logged_in': False})

@app.route('/account')
def account():
    if not session.get('logged_in'):
        return render_template('index.html')
    return render_template('account.html')

@app.route('/get_accounts', methods=['GET'])
def get_accounts():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': '请先登录'})
    
    users_list = get_user_list()
    return jsonify({'success': True, 'accounts': users_list})

@app.route('/add_account', methods=['POST'])
def add_account():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': '请先登录'})
    
    global _users
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'})
    
    users_dict = get_users()
    if username in users_dict:
        return jsonify({'success': False, 'message': '用户名已存在'})
    
    users_dict[username] = password
    users_list = [{'username': u, 'password': p} for u, p in users_dict.items()]
    
    if save_users(users_list):
        _users = users_dict
        return jsonify({'success': True, 'message': '添加成功'})
    else:
        return jsonify({'success': False, 'message': '添加失败'})

@app.route('/update_account', methods=['POST'])
def update_account():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': '请先登录'})
    
    global _users
    data = request.get_json()
    old_username = data.get('oldUsername', '').strip()
    new_username = data.get('newUsername', '').strip()
    new_password = data.get('newPassword', '')
    
    if not new_username or not new_password:
        return jsonify({'success': False, 'message': '新用户名和密码不能为空'})
    
    users_dict = get_users()
    if old_username not in users_dict:
        return jsonify({'success': False, 'message': '原用户不存在'})
    
    del users_dict[old_username]
    users_dict[new_username] = new_password
    users_list = [{'username': u, 'password': p} for u, p in users_dict.items()]
    
    if session.get('username') == old_username:
        session['username'] = new_username
    
    if save_users(users_list):
        _users = users_dict
        return jsonify({'success': True, 'message': '更新成功'})
    else:
        return jsonify({'success': False, 'message': '更新失败'})

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': '请先登录'})
    
    global _users
    data = request.get_json()
    username = data.get('username', '').strip()
    
    users_dict = get_users()
    if username not in users_dict:
        return jsonify({'success': False, 'message': '用户不存在'})
    
    if session.get('username') == username:
        return jsonify({'success': False, 'message': '不能删除当前登录账户'})
    
    del users_dict[username]
    users_list = [{'username': u, 'password': p} for u, p in users_dict.items()]
    
    if save_users(users_list):
        _users = users_dict
        return jsonify({'success': True, 'message': '删除成功'})
    else:
        return jsonify({'success': False, 'message': '删除失败'})

def get_max_school_id():
    max_id = 0
    universities_list = get_universities()
    for uni in universities_list:
        try:
            uni_id = int(uni.get('学校ID', '0'))
            if uni_id > max_id:
                max_id = uni_id
        except:
            pass
    return max_id

def get_available_school_id():
    used_ids = set()
    max_id = 0
    
    universities_list = get_universities()
    for uni in universities_list:
        try:
            uni_id = int(uni.get('学校ID', '0'))
            if uni_id > 0:
                used_ids.add(uni_id)
                if uni_id > max_id:
                    max_id = uni_id
        except:
            pass
    
    for i in range(1, max_id + 1):
        if i not in used_ids:
            return i
    
    return max_id + 1

def school_exists(school_id, school_name):
    universities_list = get_universities()
    for uni in universities_list:
        if uni.get('学校ID') == school_id or uni.get('学校名称') == school_name:
            return True
    return False

@app.route('/add_school')
def add_school_page():
    if not session.get('logged_in'):
        return render_template('index.html')
    available_id = get_available_school_id()
    return render_template('add_school.html', available_id=available_id)

@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': '请先登录'})
    
    if 'logo' not in request.files:
        return jsonify({'success': False, 'message': '请选择文件'})
    
    file = request.files['logo']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': '请选择文件'})
    
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return jsonify({'success': False, 'message': '只支持图片文件'})
    
    if file.content_length > 500 * 1024:
        return jsonify({'success': False, 'message': '文件大小不能超过500KB'})
    
    # 获取可用ID作为文件名
    available_id = request.form.get('available_id', '')
    if not available_id or not available_id.isdigit():
        return jsonify({'success': False, 'message': '无效的学校ID'})
    
    # 获取原文件扩展名
    original_ext = os.path.splitext(file.filename)[1].lower()
    new_filename = f"{available_id}{original_ext}"
    
    os.makedirs('logo', exist_ok=True)
    
    file_path = os.path.join('logo', new_filename)
    file.save(file_path)
    
    return jsonify({'success': True, 'file_path': file_path, 'logo_id': available_id})

@app.route('/add_school', methods=['POST'])
def add_school():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': '请先登录'})
    
    global _universities
    data = request.get_json()
    
    school_id = data.get('学校ID', '')
    school_name = data.get('学校名称', '')
    
    if not school_id or not school_name:
        return jsonify({'success': False, 'message': '学校ID和名称不能为空'})
    
    if school_exists(school_id, school_name):
        return jsonify({'success': False, 'message': '学校ID或名称已存在'})
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO universities (
                学校ID, 学校名称, 地址, 类别, 性质, 归属部门, 标签,
                建校时间, 占地面积, 保研星级, 博士点数量, 硕士点数量,
                国家重点学科数量, 软科综合排名, 校友会综合排名, QS世界排名,
                US世界排名, 泰晤士排名, 人气值排名, 基本信息, logo_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            school_id,
            school_name,
            data.get('地址', ''),
            data.get('类别', ''),
            data.get('性质', ''),
            data.get('归属部门', ''),
            data.get('标签', ''),
            data.get('建校时间', ''),
            data.get('占地面积', ''),
            data.get('保研星级', ''),
            data.get('博士点数量', ''),
            data.get('硕士点数量', ''),
            data.get('国家重点学科数量', ''),
            data.get('软科综合排名', ''),
            data.get('校友会综合排名', ''),
            data.get('QS世界排名', ''),
            data.get('US世界排名', ''),
            data.get('泰晤士排名', ''),
            data.get('人气值排名', ''),
            data.get('基本信息', ''),
            data.get('logo_path', '')
        ))
        conn.commit()
        conn.close()
        
        _universities = load_data()
        return jsonify({'success': True, 'message': '添加成功'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'添加失败: {str(e)}'})

@app.route('/delete_school', methods=['POST'])
def delete_school():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': '请先登录'})
    
    global _universities
    data = request.get_json()
    school_id = data.get('school_id', '')
    
    universities_list = get_universities()
    print(f'删除院校请求，school_id: {school_id}')
    print(f'当前院校数量: {len(universities_list)}')
    
    if not school_id:
        return jsonify({'success': False, 'message': '学校ID不能为空'})
    
    target_index = None
    logo_path = ''
    for i, uni in enumerate(universities_list):
        print(f'检查院校 {i}: ID={uni.get("学校ID")}, 名称={uni.get("学校名称")}')
        if uni.get('学校ID') == school_id:
            target_index = i
            logo_path = uni.get('logo_path', '')
            print(f'找到匹配的院校，索引: {target_index}')
            break
    
    if target_index is None:
        print(f'未找到学校ID为 {school_id} 的院校')
        return jsonify({'success': False, 'message': '未找到该学校'})
    
    print(f'Logo路径: {logo_path}')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM universities WHERE 学校ID = ?', (school_id,))
        conn.commit()
        conn.close()
        
        deleted_uni = universities_list.pop(target_index)
        _universities = universities_list
        print(f'已删除院校: {deleted_uni.get("学校名称")}')
        
        if logo_path and os.path.exists(logo_path):
            try:
                os.remove(logo_path)
                print(f'已删除logo文件: {logo_path}')
            except Exception as e:
                print(f'删除logo文件错误: {e}')
        else:
            print(f'Logo文件不存在或路径为空: {logo_path}')
        
        print('从数据库删除成功')
        return jsonify({'success': True, 'message': '删除成功'})
    except Exception as e:
        print(f'删除失败: {e}')
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'})

@app.route('/api/scrolling_data', methods=['GET'])
def get_scrolling_data():
    data = load_scrolling_data()
    position = get_scrolling_position()
    return jsonify({
        'data': data,
        'position': position
    })

@app.route('/api/scrolling_position', methods=['POST'])
def update_scrolling_position():
    data = request.get_json()
    position = data.get('position', 0)
    set_scrolling_position(position)
    return jsonify({'success': True})

if __name__ == '__main__':
    # 从环境变量获取配置，支持 Docker 部署
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')  # Docker 需要绑定到 0.0.0.0
    
    app.run(debug=debug_mode, host=host, port=port)
