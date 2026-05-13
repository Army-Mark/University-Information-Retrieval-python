# University Information Retrieval System - 高校信息管理系统

基于 Python Flask 的高校信息管理系统，采用分层架构设计，提供完整的院校信息管理功能。

## 📋 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
  - [Docker部署（推荐）](#docker部署推荐)
  - [本地运行](#本地运行)
  - [Docker Compose多容器部署](#docker-compose多容器部署)
- [默认账户](#默认账户)
- [API文档](#api文档)
  - [认证相关API](#认证相关api)
  - [学校管理API](#学校管理api)
  - [用户管理API](#用户管理api)
  - [操作日志API](#操作日志api)
  - [用户设置API](#用户设置api)
  - [滚动数据API](#滚动数据api)
- [配置说明](#配置说明)
- [数据库表结构](#数据库表结构)
- [开发指南](#开发指南)
  - [项目架构说明](#项目架构说明)
  - [添加新功能流程](#添加新功能流程)
  - [数据库迁移](#数据库迁移)
- [部署指南](#部署指南)
  - [生产环境部署](#生产环境部署)
  - [Nginx反向代理](#nginx反向代理)
  - [HTTPS配置](#https配置)
- [安全建议](#安全建议)
- [常见问题](#常见问题)
- [许可证](#许可证)

---

## 项目简介

高校信息管理系统是一个用于管理高校信息的Web应用系统，主要功能包括：

- 📚 **学校信息管理**：完整的高校信息CRUD操作
- 👤 **用户认证系统**：安全的登录/注销机制
- 🔐 **权限控制**：Admin和User两级角色权限
- 📝 **操作日志**：完整的操作审计追踪
- 🔍 **智能搜索**：支持ID和名称搜索
- 🎨 **个性化设置**：主题、语言等配置
- 🎨 **Logo管理**：支持上传和管理学校Logo
- 🔄 **滚动展示**：首页自动滚动展示学校列表

---

## 功能特性

### 核心功能

| 功能 | 说明 | 权限要求 |
|------|------|----------|
| 学校信息管理 | 增删改查学校完整信息，包括基本信息、排名、学科建设等 | 登录用户可编辑，Admin可删除 |
| 用户认证 | 安全的登录/注销机制，支持会话管理 | 公开 |
| 角色权限 | Admin（管理员）/ User（普通用户）两级权限控制 | 系统内置 |
| 操作日志 | 完整记录用户操作，便于审计追踪 | 登录用户可查看，Admin可删除 |
| 个人设置 | 主题、语言等个性化配置 | 登录用户 |
| 智能搜索 | 支持按ID或名称精确/模糊搜索 | 公开 |
| Logo管理 | 上传和管理学校Logo图片 | 登录用户可上传 |
| 滚动展示 | 首页自动滚动展示学校列表 | 公开 |

### 安全特性

| 特性 | 说明 |
|------|------|
| XSS防护 | 所有用户输入自动转义，防止跨站脚本攻击 |
| SQL注入防护 | 使用参数化查询，防止SQL注入 |
| 密码安全 | 支持密码强度验证，建议8字符以上包含字母数字 |
| 安全Cookie | 配置HttpOnly、SameSite等安全属性 |
| 权限验证 | 敏感操作需登录验证，管理员操作需Admin权限 |

---

## 技术栈

| 类别 | 技术 |
|------|------|
| 后端框架 | Flask 2.x |
| 数据库 | SQLite 3 |
| 前端 | HTML5 + CSS3 + JavaScript |
| 容器化 | Docker + Docker Compose |
| Web服务器 | Nginx（生产环境） |

---

## 项目结构

```
school/
├── app.py                        # 应用入口文件
│
├── core/                         # 核心业务模块
│   ├── __init__.py
│   ├── config/                   # 配置管理
│   │   ├── __init__.py
│   │   └── config.py            # 配置类，读取环境变量
│   │
│   ├── models/                   # 数据模型
│   │   ├── __init__.py
│   │   └── models.py            # 数据模型定义（University, User等）
│   │
│   ├── repository/               # 数据访问层
│   │   ├── __init__.py
│   │   └── repository.py        # 数据访问接口实现
│   │
│   ├── service/                  # 业务逻辑层
│   │   ├── __init__.py
│   │   └── service.py           # 业务逻辑实现
│   │
│   ├── api/                     # API处理器模块
│   │   ├── __init__.py          # API注册和初始化
│   │   ├── handlers/            # API处理器
│   │   │   ├── __init__.py
│   │   │   ├── index.py         # 首页
│   │   │   ├── search.py        # 搜索
│   │   │   ├── university.py    # 学校管理
│   │   │   ├── auth.py          # 认证
│   │   │   ├── users.py         # 用户管理
│   │   │   ├── logs.py          # 操作日志
│   │   │   ├── settings.py      # 用户设置
│   │   │   └── media.py         # 媒体上传
│   │   │
│   │   └── middleware/          # 中间件
│   │       ├── __init__.py
│   │       └── auth.py          # 认证中间件
│   │
│   └── pkg/                     # 公共包
│       ├── __init__.py
│       └── errors/              # 错误处理
│           ├── __init__.py
│           └── errors.py        # 自定义异常类
│
├── templates/                    # HTML模板
│   ├── index.html               # 首页
│   ├── university.html          # 学校详情页
│   ├── university_edit.html     # 学校编辑页
│   ├── add_school.html          # 添加学校页
│   ├── account.html             # 账户管理页
│   ├── operation_logs.html      # 操作日志页
│   └── not_found.html           # 404页面
│
├── data/                        # 数据目录
│   └── school.db                # SQLite数据库文件
│
├── logo/                        # 学校Logo存储目录
│
├── Dockerfile                    # Docker镜像构建文件
├── docker-compose.yml            # Docker Compose编排文件
├── .dockerignore                # Docker忽略文件
├── .env.example                 # 环境变量示例
├── requirements.txt             # Python依赖
├── check_db.py                  # 数据库检查工具
├── migrate_db.py                # 数据库迁移工具
│
└── README.md                    # 项目文档
```

---

## 快速开始

### Docker部署（推荐）

#### 方式一：使用Docker Compose（推荐）

```bash
# 1. 克隆项目
git clone <repository-url>
cd school

# 2. 启动服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps

# 4. 查看日志
docker-compose logs -f

# 5. 访问应用
# 打开浏览器访问 http://localhost:5000
```

#### 方式二：手动构建镜像

```bash
# 1. 构建镜像
docker build -t school-info-system .

# 2. 运行容器
docker run -d \
  --name school-info \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logo:/app/logo \
  -e DB_PATH=/app/data/school.db \
  school-info-system

# 3. 访问应用
# 打开浏览器访问 http://localhost:5000
```

### 本地运行

#### 环境要求

- Python 3.8+
- pip 包管理器

#### 安装步骤

```bash
# 1. 克隆项目
git clone <repository-url>
cd school

# 2. 创建虚拟环境（推荐）
python -m venv venv

# Windows激活虚拟环境
venv\Scripts\activate

# Linux/Mac激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 初始化数据库（首次运行）
# 系统会自动创建数据库和默认管理员账户
python app.py

# 5. 启动应用
python app.py
```

#### 使用说明

1. 应用启动后，默认访问地址：`http://localhost:5000`
2. 默认管理员账户：`admin` / `admin123`
3. 数据库文件位于：`data/school.db`
4. Logo文件存储于：`logo/` 目录

### Docker Compose多容器部署

对于生产环境，建议使用完整的多容器架构：

```bash
# 启动所有服务（包括数据卷、网络等）
docker-compose up -d --build

# 查看所有容器状态
docker-compose ps -a

# 查看日志
docker-compose logs -f school-app

# 停止所有服务
docker-compose down

# 停止并删除数据卷（谨慎操作，会删除数据库）
docker-compose down -v
```

---

## 默认账户

| 角色 | 用户名 | 密码 | 权限说明 |
|------|--------|------|----------|
| 管理员 | admin | admin123 | 全部功能，包括账户管理、日志删除、学校增删改等 |
| 普通用户 | user | user1234 | 查看学校信息、管理自己的账户 |

> ⚠️ **安全提示**：生产环境请立即修改默认密码！

---

## API文档

### 认证相关API

#### 用户登录

```
POST /login
Content-Type: application/json

请求体：
{
    "username": "admin",
    "password": "admin123"
}

成功响应：
{
    "success": true,
    "message": "Login successful",
    "role": "admin"
}

失败响应：
{
    "error": "Invalid username or password"
}
```

#### 用户注销

```
POST /logout

成功响应：
{
    "success": true,
    "message": "Logged out"
}
```

#### 检查登录状态

```
GET /check_login

已登录响应：
{
    "success": true,
    "logged_in": true,
    "username": "admin",
    "role": "admin"
}

未登录响应：
{
    "logged_in": false
}
```

---

### 学校管理API

#### 首页

```
GET /

返回：HTML页面，包含滚动展示的学校列表
```

#### 搜索学校

```
GET /search?keyword=<关键词>

参数：
- keyword: 搜索关键词（学校名称或ID）

响应：JSON数组，包含匹配的学校列表
[
    {
        "id": "1001",
        "name": "北京大学",
        "match_type": "exact"  // exact:精确匹配, fuzzy:模糊匹配, id_match:ID前缀匹配
    }
]
```

#### 查看学校详情

```
GET /university/<school_id>

参数：
- school_id: 学校ID或学校名称

返回：HTML页面，显示学校详细信息
```

#### 编辑学校页面

```
GET /edit/<school_id>
权限：需要登录

返回：HTML页面，学校编辑表单
```

#### 保存学校信息

```
POST /save
权限：需要登录
Content-Type: application/json

请求体：
{
    "学校ID": "1001",
    "学校名称": "北京大学",
    "地址": "北京市海淀区",
    "类别": "综合类",
    "性质": "公办",
    "归属部门": "教育部",
    "标签": "985,211,双一流",
    "建校时间": "1898年",
    "占地面积": "3000亩",
    "保研星级": "5星",
    "博士点数量": "50",
    "硕士点数量": "100",
    "国家重点学科数量": "20",
    "软科综合排名": "1",
    "校友会综合排名": "1",
    "QS世界排名": "100",
    "US世界排名": "100",
    "泰晤士排名": "100",
    "人气值排名": "5",
    "基本信息": "北京大学是中国著名大学...",
    "logo_path": "1001.png"
}

成功响应：
{
    "success": true,
    "message": "Saved successfully"
}

失败响应（如未登录）：
{
    "error": "Unauthorized"
}
```

#### 添加学校页面

```
GET /add_school
权限：需要登录

返回：HTML页面，添加学校表单
```

#### 添加学校

```
POST /add_school
权限：需要登录
Content-Type: application/json

请求体：同 /save

成功响应：
{
    "success": true,
    "message": "Added successfully"
}

失败响应：
{
    "error": "学校ID已存在"  // 或其他错误信息
}
```

#### 删除学校

```
POST /delete_school
权限：仅Admin
Content-Type: application/json

请求体：
{
    "school_id": "1001"
}

成功响应：
{
    "success": true,
    "message": "Deleted successfully"
}

失败响应（如权限不足）：
{
    "error": "Forbidden"
}
```

#### 上传Logo

```
POST /upload_logo
Content-Type: multipart/form-data

表单字段：
- logo: 图片文件（PNG/JPG/JPEG/GIF，最大500KB）
- available_id: 学校ID

成功响应：
{
    "success": true,
    "filename": "1001.png",
    "logo_id": "1001"
}

失败响应：
{
    "success": false,
    "message": "No file provided"  // 或其他错误信息
}
```

#### 获取Logo

```
GET /logo/<filename>

参数：
- filename: Logo文件名

返回：图片文件

示例：GET /logo/1001.png
```

---

### 用户管理API

#### 账户管理页面

```
GET /account
权限：需要登录

返回：HTML页面，账户管理界面
```

#### 获取账户列表

```
POST /get_accounts
权限：需要登录
Content-Type: application/json

请求体：
{
    "username": "admin",
    "role": "admin"
}

成功响应：
{
    "success": true,
    "accounts": [
        {
            "id": 1,
            "username": "admin",
            "role": "admin",
            "created_at": "2024-01-01 00:00:00"
        }
    ]
}

说明：
- Admin用户可以看到所有账户
- 普通用户只能看到自己的账户
```

#### 添加账户

```
POST /add_account
权限：仅Admin
Content-Type: application/json

请求体：
{
    "username": "newuser",
    "password": "password123",
    "role": "user"
}

成功响应：
{
    "success": true,
    "message": "Account added successfully"
}

失败响应：
{
    "code": "USER_EXISTS",
    "message": "用户名已存在"
}
```

#### 更新账户

```
POST /update_account
权限：需要登录
Content-Type: application/json

请求体：
{
    "oldUsername": "admin",
    "newUsername": "admin",
    "newPassword": "newpassword123",
    "newRole": "admin",
    "currentUserRole": "admin"
}

成功响应：
{
    "success": true,
    "message": "Updated successfully"
}

说明：
- 普通用户只能修改自己的账户
- 普通用户不能修改自己的角色
- 修改其他账户需要Admin权限
```

#### 删除账户

```
POST /delete_account
权限：仅Admin
Content-Type: application/json

请求体：
{
    "username": "user"
}

成功响应：
{
    "success": true,
    "message": "Deleted successfully"
}

失败响应：
{
    "code": "CANNOT_DELETE_SELF",
    "message": "不能删除自己的账户"
}
```

---

### 操作日志API

#### 操作日志页面

```
GET /operation_logs
权限：需要登录

返回：HTML页面，操作日志列表

说明：
- Admin用户可以看到所有操作日志
- 普通用户只能看到自己的操作日志
```

#### 获取日志列表

```
GET /get_operation_logs
权限：需要登录

成功响应：
{
    "success": true,
    "logs": [
        {
            "id": 1,
            "operation_type": "CREATE",
            "table_name": "universities",
            "record_id": "1001",
            "username": "admin",
            "operation_time": "2024-01-01 12:00:00",
            "ip_address": "127.0.0.1",
            "user_agent": "Mozilla/5.0...",
            "details": "创建学校: 北京大学",
            "changes": "{\"学校ID\": [null, \"1001\"]}"
        }
    ]
}
```

#### 删除日志

```
POST /delete_operation_logs
权限：仅Admin
Content-Type: application/json

请求体：
{
    "ids": [1, 2, 3]
}

成功响应：
{
    "success": true,
    "message": "Deleted 3 logs"
}

失败响应：
{
    "code": "INVALID_INPUT",
    "message": "No log IDs provided"
}
```

---

### 用户设置API

#### 获取用户设置

```
GET /api/settings
权限：需要登录

成功响应：
{
    "success": true,
    "settings": {
        "id": 1,
        "user_id": 1,
        "theme": "light",
        "language": "zh",
        "created_at": "2024-01-01 00:00:00",
        "updated_at": "2024-01-01 00:00:00"
    }
}
```

#### 保存用户设置

```
POST /api/settings
权限：需要登录
Content-Type: application/json

请求体：
{
    "theme": "dark",
    "language": "zh"
}

成功响应：
{
    "success": true,
    "settings": {
        "id": 1,
        "user_id": 1,
        "theme": "dark",
        "language": "zh",
        "created_at": "2024-01-01 00:00:00",
        "updated_at": "2024-01-02 00:00:00"
    }
}
```

---

### 滚动数据API

#### 获取滚动数据

```
GET /api/scrolling_data
权限：公开

成功响应：
{
    "data": [
        {
            "学校ID": "1001",
            "学校名称": "北京大学",
            "地址": "北京市",
            "类别": "综合类",
            "性质": "公办"
        },
        {
            "学校ID": "1002",
            "学校名称": "清华大学",
            "地址": "北京市",
            "类别": "综合类",
            "性质": "公办"
        }
    ],
    "position": 0
}
```

#### 更新滚动位置

```
POST /api/scrolling_position
权限：公开

请求体：
{
    "position": 100
}

成功响应：
{
    "success": true
}
```

---

## 配置说明

### 环境变量

在项目根目录创建 `.env` 文件（参考 `.env.example`）：

```bash
# 服务器配置
PORT=5000                      # 服务端口
HOST=0.0.0.0                  # 监听地址
FLASK_DEBUG=false              # 调试模式（生产环境设为false）

# 数据库配置
DB_PATH=data/school.db        # 数据库文件路径

# 安全配置
SECRET_KEY=your-secret-key-here  # Session加密密钥（生产环境必改！）

# Cookie安全配置
SESSION_COOKIE_HTTPONLY=true   # 防止JavaScript读取Cookie
SESSION_COOKIE_SECURE=false    # 生产环境应设为true（需要HTTPS）
SESSION_COOKIE_SAMESITE=Lax    # CSRF防护：Lax/Strict/None
```

### 配置优先级

1. 环境变量（最高优先级）
2. `.env` 文件
3. 代码默认值（最低优先级）

---

## 数据库表结构

### universities（学校表）

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| 学校ID | TEXT | 主键，学校唯一标识 | "1001" |
| 学校名称 | TEXT | 学校全称 | "北京大学" |
| 地址 | TEXT | 学校地址 | "北京市海淀区" |
| 类别 | TEXT | 学校类别 | "综合类/理工类/师范类..." |
| 性质 | TEXT | 公办/民办 | "公办" |
| 归属部门 | TEXT | 教育部/省属等 | "教育部" |
| 标签 | TEXT | 学校特色标签，多个标签用逗号分隔 | "985,211,双一流" |
| 建校时间 | TEXT | 建校年份 | "1898年" |
| 占地面积 | TEXT | 校园面积 | "3000亩" |
| 保研星级 | TEXT | 保研推荐等级 | "5星" |
| 博士点数量 | TEXT | 博士授予点数量 | "50" |
| 硕士点数量 | TEXT | 硕士授予点数量 | "100" |
| 国家重点学科数量 | TEXT | 国家重点学科数 | "20" |
| 软科综合排名 | TEXT | 软科排名 | "1" |
| 校友会综合排名 | TEXT | 校友会排名 | "1" |
| QS世界排名 | TEXT | QS世界大学排名 | "100" |
| US世界排名 | TEXT | US News世界排名 | "100" |
| 泰晤士排名 | TEXT | Times世界排名 | "100" |
| 人气值排名 | TEXT | 用户访问热度排名 | "5" |
| 基本信息 | TEXT | 学校简介 | "北京大学是中国著名大学..." |
| logo_path | TEXT | Logo文件路径 | "1001.png" |

### users（用户表）

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| id | INTEGER | 主键，自增 | 1 |
| username | TEXT | 用户名，唯一索引 | "admin" |
| password | TEXT | 密码（加密存储） | "admin123" |
| role | TEXT | 角色：admin/user | "admin" |
| created_at | DATETIME | 创建时间 | "2024-01-01 00:00:00" |

### operation_logs（操作日志表）

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| id | INTEGER | 主键，自增 | 1 |
| operation_type | TEXT | 操作类型 | "CREATE/UPDATE/DELETE" |
| table_name | TEXT | 操作的数据表 | "universities" |
| record_id | TEXT | 被操作的记录ID | "1001" |
| username | TEXT | 操作用户名 | "admin" |
| operation_time | DATETIME | 操作时间 | "2024-01-01 12:00:00" |
| ip_address | TEXT | 客户端IP地址 | "127.0.0.1" |
| user_agent | TEXT | 浏览器User-Agent | "Mozilla/5.0..." |
| details | TEXT | 操作详情（JSON格式） | "创建学校: 北京大学" |
| changes | TEXT | 变更内容对比（JSON格式） | {"学校ID": [null, "1001"]} |

### user_settings（用户设置表）

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| id | INTEGER | 主键，自增 | 1 |
| user_id | INTEGER | 关联用户ID | 1 |
| theme | TEXT | 主题 | "light/dark" |
| language | TEXT | 语言 | "zh/en" |
| created_at | DATETIME | 创建时间 | "2024-01-01 00:00:00" |
| updated_at | DATETIME | 更新时间 | "2024-01-01 00:00:00" |

---

## 开发指南

### 项目架构说明

本项目采用分层架构，职责清晰分离：

```
┌─────────────────────────────────────────────────────────────┐
│                        表现层（Templates）                     │
│  index.html, university.html, account.html 等HTML页面       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     API处理器层（Handlers）                    │
│  处理HTTP请求/响应，参数验证，权限检查                        │
│  core/api/handlers/                                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     服务层（Service）                        │
│  业务逻辑处理，事务管理                                      │
│  core/service/service.py                                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     数据访问层（Repository）                  │
│  数据CRUD操作，SQL执行                                       │
│  core/repository/repository.py                              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        数据层（Database）                     │
│  SQLite数据库                                                │
└─────────────────────────────────────────────────────────────┘
```

### 添加新功能流程

#### 步骤1：定义数据模型（Model层）

在 `core/models/models.py` 中定义数据模型：

```python
@dataclass
class NewModel:
    id: int
    name: str
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }
```

#### 步骤2：实现数据访问（Repository层）

在 `core/repository/repository.py` 中实现数据访问方法：

```python
class NewModelRepository:
    def __init__(self, db: Database):
        self.db = db

    def get_by_id(self, id: int):
        cursor = self.db.execute("SELECT * FROM new_table WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return NewModel(**dict(row))
        return None

    def create(self, model: NewModel):
        cursor = self.db.execute(
            "INSERT INTO new_table (name, description) VALUES (?, ?)",
            (model.name, model.description)
        )
        return cursor.lastrowid

    def update(self, model: NewModel):
        self.db.execute(
            "UPDATE new_table SET name = ?, description = ? WHERE id = ?",
            (model.name, model.description, model.id)
        )

    def delete(self, id: int):
        self.db.execute("DELETE FROM new_table WHERE id = ?", (id,))
```

#### 步骤3：实现业务逻辑（Service层）

在 `core/service/service.py` 中实现业务逻辑：

```python
class NewModelService:
    def __init__(self, repository: NewModelRepository):
        self.repository = repository

    def get_by_id(self, id: int):
        return self.repository.get_by_id(id)

    def create(self, name: str, description: str):
        model = NewModel(
            id=0,
            name=name,
            description=description
        )
        return self.repository.create(model)

    def update(self, model: NewModel):
        return self.repository.update(model)

    def delete(self, id: int):
        return self.repository.delete(id)
```

#### 步骤4：创建API处理器（API层）

在 `core/api/handlers/` 中创建新的处理器：

```python
from flask import Blueprint, jsonify, request

new_bp = Blueprint("new", __name__, url_prefix="")


def init_new(services: dict):
    """初始化新功能所需的服务"""
    new_bp.new_service = services.get("new_service")


@new_bp.route("/api/new", methods=["GET"])
def get_new():
    """获取数据"""
    items = new_bp.new_service.get_all()
    return jsonify({
        "success": True,
        "data": [item.to_dict() for item in items]
    })


@new_bp.route("/api/new", methods=["POST"])
def create_new():
    """创建数据"""
    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    result = new_bp.new_service.create(name, description)
    return jsonify({"success": True, "id": result})
```

#### 步骤5：注册蓝图（主入口）

在 `core/api/__init__.py` 中注册蓝图：

```python
from core.api.handlers.new import new_bp

def register_api_handlers(app: Flask, services: dict):
    # ... 其他代码 ...

    new_bp.new_service = services.get("new_service")

    # ... 其他代码 ...

    app.register_blueprint(new_bp)
```

### 数据库迁移

在 `migrate_db.py` 中管理数据库迁移：

```python
from core.repository import Database

def upgrade():
    db = Database("data/school.db")

    # 创建新表
    db.execute("""
        CREATE TABLE IF NOT EXISTS new_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 添加字段
    db.execute("ALTER TABLE universities ADD COLUMN new_field TEXT")

    # 创建索引
    db.execute("CREATE INDEX IF NOT EXISTS idx_name ON new_table(name)")

    # 插入默认数据
    db.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
               ('admin', 'admin', 'admin'))

    print("Migration completed successfully!")


def downgrade():
    """回滚迁移"""
    db = Database("data/school.db")

    # 删除表
    db.execute("DROP TABLE IF EXISTS new_table")

    # 删除字段（SQLite不支持，需重建表）
    # ...

    print("Downgrade completed successfully!")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "downgrade":
        downgrade()
    else:
        upgrade()
```

---

## 部署指南

### 生产环境部署

#### 1. 服务器准备

```bash
# 更新系统
apt update && apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com | sh

# 安装Docker Compose
apt install docker-compose -y

# 启动Docker
systemctl start docker
systemctl enable docker
```

#### 2. 部署应用

```bash
# 创建部署目录
mkdir -p /opt/school
cd /opt/school

# 克隆项目或复制文件
git clone <repository-url> .

# 配置环境变量
cp .env.example .env
vim .env  # 修改SECRET_KEY等配置

# 构建并启动
docker-compose up -d --build

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f school-app
```

#### 3. 数据备份

```bash
# 备份数据库
docker exec school-app cp /app/data/school.db /app/data/backup_$(date +%Y%m%d_%H%M%S).db

# 备份Logo
docker exec school-app tar -czf /app/logo_backup.tar.gz -C /app logo

# 导出到主机
docker cp school-app:/app/data/school.db ./backup/

# 恢复数据库（需要停止容器）
docker-compose down
docker cp ./backup/school.db school-app:/app/data/school.db
docker-compose up -d
```

### Nginx反向代理

```nginx
# /etc/nginx/conf.d/school.conf

server {
    listen 80;
    server_name your-domain.com;

    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL证书
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # SSL配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;

    # 上传大小限制
    client_max_body_size 10M;

    # 代理到Flask
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Logo静态文件（可选优化）
    location /logo/ {
        alias /opt/school/logo/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 日志
    access_log /var/log/nginx/school_access.log;
    error_log /var/log/nginx/school_error.log;
}
```

### HTTPS配置

#### 使用Let's Encrypt免费证书

```bash
# 安装Certbot
apt install certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d your-domain.com

# 自动续期测试
certbot renew --dry-run

# 设置自动续期（Certbot自动添加cron任务）
systemctl status certbot.timer
```

#### 证书自动续期Cron配置

```bash
# 编辑crontab
crontab -e

# 添加以下内容（每天凌晨2点检查续期）
0 2 * * * /usr/bin/certbot renew --quiet --deploy-hook "systemctl reload nginx"
```

---

## 安全建议

### 基础安全

1. **修改默认密码**：生产环境立即修改admin账户密码
2. **设置强SECRET_KEY**：使用随机字符串，至少32字符
3. **启用HTTPS**：生产环境必须使用HTTPS
4. **更新依赖**：定期更新Python包和Docker镜像

### 服务器安全

5. **限制访问IP**：使用防火墙限制管理后台访问
6. **最小权限**：数据库和文件系统权限最小化
7. **安全SSH**：使用SSH密钥登录，禁用密码登录
8. **安装防火墙**：配置UFW或iptables

### 应用安全

9. **定期备份**：配置自动备份策略
10. **监控日志**：关注异常登录和操作
11. **输入验证**：后端验证所有用户输入
12. **安全Headers**：配置X-Frame-Options, X-Content-Type-Options等

---

## 常见问题

### 启动问题

#### Q: 应用启动失败，提示端口被占用？

```bash
# 查看端口占用
netstat -tlnp | grep 5000

# 或在Windows上
netstat -ano | findstr :5000

# 杀死占用进程或修改端口
# 修改 .env 文件
PORT=5001
```

#### Q: 数据库文件不存在？

```bash
# 首次运行会自动创建数据库
python app.py

# 如果需要手动创建
python migrate_db.py
```

### 功能问题

#### Q: Logo上传失败？

1. 检查 `logo/` 目录权限：`chmod 755 logo/`
2. 检查文件大小（最大500KB）
3. 检查文件格式（仅支持PNG/JPG/JPEG/GIF）
4. 检查磁盘空间

#### Q: 搜索功能不工作？

1. 检查浏览器控制台是否有错误
2. 确认数据库中有学校数据
3. 检查API响应：`curl http://localhost:5000/search?keyword=test`

#### Q: 登录状态无法保持？

1. 检查Cookie是否被浏览器阻止
2. 检查浏览器隐私设置
3. 确认SECRET_KEY配置正确

### Docker问题

#### Q: Docker容器无法启动？

```bash
# 查看详细日志
docker-compose logs -f

# 检查端口占用
netstat -tlnp | grep 5000

# 清理并重建
docker-compose down
docker system prune -f
docker-compose up -d --build
```

#### Q: 数据持久化问题？

```bash
# 检查数据卷
docker volume ls

# 检查挂载是否正确
docker inspect school-app

# 重建数据卷
docker-compose down -v
docker-compose up -d
```

### 操作问题

#### Q: 如何重置管理员密码？

```bash
# 方式1：使用SQLite直接修改
docker exec -it school-app sqlite3 /app/data/school.db

sqlite> UPDATE users SET password='admin' WHERE username='admin';
sqlite> .exit

# 方式2：停止容器，修改后重启
docker-compose down
# 使用SQLite工具修改
docker-compose up -d
```

#### Q: 如何查看操作日志？

```bash
# 查看所有日志
curl -X GET http://localhost:5000/get_operation_logs \
  -H "Cookie: session=your-session-cookie"

# 或在数据库中查看
docker exec -it school-app sqlite3 /app/data/school.db

sqlite> SELECT * FROM operation_logs ORDER BY operation_time DESC LIMIT 10;
sqlite> .exit
```

---

## 许可证

MIT License

Copyright (c) 2024 University Information Retrieval System

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
