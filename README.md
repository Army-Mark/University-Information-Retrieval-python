# 学校信息管理系统

> 一个基于 Flask 框架开发的学校信息管理系统，提供学校信息搜索、展示、管理以及用户账户管理等功能。

---

## 📋 目录

- [功能特性](#-功能特性)
- [技术栈](#-技术栈)
- [项目架构](#-项目架构)
- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [环境变量](#-环境变量)
- [API 接口](#-api-接口)
- [数据库结构](#-数据库结构)
- [使用说明](#-使用说明)
- [Docker 部署](#-docker-部署)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## ✨ 功能特性

### 🔍 搜索功能
- **实时搜索建议**：输入时自动显示匹配结果，无需点击搜索按钮
- **多维度匹配**：支持按学校ID和学校名称进行搜索
- **智能排序算法**：
  - 精确ID匹配（优先级最高）
  - 部分ID匹配（数字匹配）
  - 名称匹配
- **匹配类型标记**：搜索结果显示匹配类型（精确匹配/ID匹配）

### 📖 学校信息展示
- **详细信息卡片**：展示学校基本信息（地址、类别、性质、归属部门等）
- **排名数据可视化**：展示各类排名数据
  - 软科综合排名
  - 校友会综合排名
  - QS世界排名
  - US News世界排名
  - 泰晤士排名
  - 人气值排名
- **标签系统**：自动识别并展示学校特色标签（985、211、双一流等）
- **Logo展示**：学校Logo图片展示
- **基本信息**：建校时间、占地面积、博士点/硕士点数量、国家重点学科数量等

### 🔐 用户认证系统
- **登录功能**：用户名密码验证登录
- **登出功能**：安全退出并清除会话
- **会话管理**：使用Flask Session管理登录状态
- **登录状态检查**：页面加载时自动检查登录状态

### 👥 账户管理（管理员）
- **账户列表查看**：展示所有用户账户信息
- **账户添加**：创建新用户账户
- **账户更新**：修改用户名和密码
- **账户删除**：删除指定账户（不可删除当前登录账户）
- **权限验证**：所有操作需管理员登录

### 🏫 学校信息管理（管理员）
- **学校信息编辑**：修改学校详细信息
- **学校信息添加**：创建新学校记录
- **学校信息删除**：删除学校记录及相关Logo文件
- **Logo上传**：支持PNG/JPG/JPEG/GIF格式，大小限制500KB
- **自动ID分配**：添加学校时自动分配可用ID

### 📊 滚动数据展示
- **实时滚动展示**：学校列表横向滚动展示
- **滚动位置记忆**：记录并恢复用户浏览位置
- **延迟加载**：按需加载数据，提升性能

---

## 🛠️ 技术栈

### 后端技术
| 分类 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 框架 | Flask | >=2.0.0 | 轻量级Web框架 |
| 数据库 | SQLite3 | 内置 | 轻量级关系型数据库 |
| 会话管理 | Flask Session | 内置 | 用户会话管理 |
| 部署 | Gunicorn | 生产环境推荐 | WSGI服务器 |

### 前端技术
| 分类 | 技术 | 版本 | 说明 |
|------|------|------|------|
| HTML | HTML5 | - | 页面结构 |
| CSS | CSS3 | - | 样式设计 |
| JavaScript | ES6+ | - | 前端交互 |
| 图标 | Font Awesome | 内置 | 图标展示 |

### 开发工具
| 工具 | 用途 |
|------|------|
| Docker | 容器化部署 |
| Docker Compose | 多容器编排 |
| Git | 版本控制 |

### 部署环境
- **操作系统**：Linux / Windows / macOS
- **Python版本**：3.10+
- **端口**：默认5000

---

## 🏗️ 项目架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        前端层 (Frontend)                        │
├─────────────────────────────────────────────────────────────────┤
│  index.html      university.html      account.html             │
│  (首页/搜索)      (学校详情)          (账户管理)                │
│  add_school.html  university_edit.html  not_found.html         │
│  (添加学校)       (编辑学校)          (404页面)                │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP请求
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        应用层 (Application)                     │
├─────────────────────────────────────────────────────────────────┤
│  app.py                                                        │
│  ├── 路由定义 (Routes)                                         │
│  │   ├── /search          # 搜索接口                           │
│  │   ├── /university/<id> # 学校详情                          │
│  │   ├── /login/logout    # 用户认证                          │
│  │   ├── /account         # 账户管理                          │
│  │   └── /add_school      # 学校管理                          │
│  ├── 业务逻辑 (Business Logic)                                 │
│  │   ├── 搜索匹配算法                                          │
│  │   ├── 用户验证逻辑                                          │
│  │   └── 数据持久化逻辑                                        │
│  └── 数据访问 (Data Access)                                    │
│      └── SQLite数据库操作                                      │
└───────────────────────────┬─────────────────────────────────────┘
                            │ SQL查询
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        数据层 (Data)                            │
├─────────────────────────────────────────────────────────────────┤
│  school.db (SQLite数据库)                                       │
│  ├── universities  # 学校信息表                                │
│  └── users         # 用户账户表                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 环境要求
- Python 3.10+
- pip 包管理工具

### 方式一：使用 Docker Compose（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd school-management

# 使用docker-compose启动（后台运行）
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

访问 http://localhost:5000 即可使用系统。

### 方式二：手动部署

```bash
# 克隆项目
git clone <repository-url>
cd school-management

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

访问 http://localhost:5000 即可使用系统。

### 方式三：使用 Gunicorn（生产环境）

```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 📁 项目结构

```
school-management/                              # 项目根目录
├── app.py                                      # Flask应用入口
│   ├── 路由定义                                 # URL路由映射
│   ├── 视图函数                                 # 请求处理逻辑
│   ├── 数据库操作                               # SQLite操作封装
│   └── 业务逻辑                                 # 搜索、认证、管理逻辑
├── school.db                                   # SQLite数据库文件
├── requirements.txt                            # Python依赖列表
├── Dockerfile                                  # Docker构建配置
├── docker-compose.yml                          # Docker Compose配置
├── .dockerignore                               # Docker忽略规则
├── README.md                                   # 项目说明文档
├── 功能.md                                     # 功能详细文档
├── logo/                                       # Logo图片目录
│   └── *.png                                   # 学校Logo图片（以学校ID命名）
└── templates/                                  # Jinja2模板目录
    ├── index.html                              # 首页（搜索+滚动展示）
    ├── university.html                         # 学校详情页
    ├── university_edit.html                    # 学校编辑页
    ├── add_school.html                         # 添加学校页
    ├── account.html                            # 账户管理页
    └── not_found.html                          # 404页面
```

### 文件说明

| 文件 | 说明 | 状态 |
|------|------|------|
| `app.py` | 主应用文件，包含所有路由和业务逻辑 | 必需 |
| `school.db` | SQLite数据库，存储学校和用户数据 | 必需 |
| `requirements.txt` | Python依赖声明 | 必需 |
| `Dockerfile` | Docker镜像构建配置 | 部署用 |
| `docker-compose.yml` | Docker Compose编排配置 | 部署用 |
| `.dockerignore` | Docker构建忽略文件 | 部署用 |
| `templates/` | HTML模板目录 | 必需 |
| `logo/` | Logo图片存储目录 | 可选 |

---

## 🔧 环境变量

### 运行时环境变量

| 变量名 | 类型 | 说明 | 默认值 | 示例 |
|--------|------|------|--------|------|
| `FLASK_APP` | string | Flask应用入口 | `app.py` | `app:app` |
| `FLASK_ENV` | string | 运行环境 | `production` | `development` |
| `FLASK_DEBUG` | bool | 调试模式 | `false` | `true` |
| `DB_PATH` | string | 数据库文件路径 | `school.db` | `/app/data/school.db` |
| `HOST` | string | 绑定地址 | `0.0.0.0` | `127.0.0.1` |
| `PORT` | int | 监听端口 | `5000` | `8080` |
| `SECRET_KEY` | string | 会话密钥 | `your-secret-key-here` | 随机字符串 |

### Docker环境变量

在 `docker-compose.yml` 中配置：

```yaml
environment:
  - FLASK_ENV=production
  - FLASK_DEBUG=false
  - DB_PATH=/app/data/school.db
  - HOST=0.0.0.0
  - PORT=5000
```

---

## 📡 API 接口

### 基础路径

所有接口均以 `/` 为基础路径。

### 搜索接口

#### GET /search
搜索学校信息

**请求参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `keyword` | string | 是 | 搜索关键词（学校ID或名称） |

**响应格式**：

```json
[
  {
    "id": "31",
    "name": "清华大学",
    "match_type": "exact_id"
  },
  {
    "id": "1001",
    "name": "北京大学",
    "match_type": "name"
  }
]
```

**match_type说明**：
- `exact_id`：精确ID匹配
- `partial_id`：部分ID匹配
- `name`：名称匹配

### 学校详情接口

#### GET /university/<id>
获取学校详情页面

**路径参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | string | 学校ID或学校名称 |

**返回**：HTML页面

### 用户认证接口

#### POST /login
用户登录

**请求体**：

```json
{
  "username": "admin",
  "password": "admin"
}
```

**响应格式**：

```json
{
  "success": true,
  "message": "登录成功"
}
```

#### POST /logout
用户登出

**响应格式**：

```json
{
  "success": true,
  "message": "退出成功"
}
```

#### GET /check_login
检查登录状态

**响应格式**：

```json
{
  "logged_in": true,
  "username": "admin"
}
```

### 账户管理接口（需登录）

#### GET /get_accounts
获取账户列表

**响应格式**：

```json
{
  "success": true,
  "accounts": [
    {
      "username": "admin",
      "password": "******"
    }
  ]
}
```

#### POST /add_account
添加账户

**请求体**：

```json
{
  "username": "newuser",
  "password": "newpassword"
}
```

**响应格式**：

```json
{
  "success": true,
  "message": "添加成功"
}
```

#### POST /update_account
更新账户

**请求体**：

```json
{
  "oldUsername": "admin",
  "newUsername": "admin_new",
  "newPassword": "newpassword"
}
```

**响应格式**：

```json
{
  "success": true,
  "message": "更新成功"
}
```

#### POST /delete_account
删除账户

**请求体**：

```json
{
  "username": "user_to_delete"
}
```

**响应格式**：

```json
{
  "success": true,
  "message": "删除成功"
}
```

### 学校管理接口（需登录）

#### GET /add_school
获取添加学校页面

**返回**：HTML页面

#### POST /add_school
添加学校

**请求体**：

```json
{
  "学校ID": "1001",
  "学校名称": "示例大学",
  "地址": "北京市海淀区",
  "类别": "综合类",
  "性质": "公办",
  "归属部门": "教育部",
  "标签": "985, 211, 双一流",
  "建校时间": "1950年",
  "占地面积": "5000亩",
  "保研星级": "5星",
  "博士点数量": "50",
  "硕士点数量": "60",
  "国家重点学科数量": "10",
  "软科综合排名": "10",
  "校友会综合排名": "12",
  "QS世界排名": "500",
  "US世界排名": "600",
  "泰晤士排名": "501-600",
  "人气值排名": "50",
  "基本信息": "学校简介...",
  "logo_path": "logo/1001.png"
}
```

**响应格式**：

```json
{
  "success": true,
  "message": "添加成功"
}
```

#### POST /save
保存学校修改

**请求体**：与添加学校相同

**响应格式**：

```json
{
  "success": true,
  "message": "保存成功"
}
```

#### POST /delete_school
删除学校

**请求体**：

```json
{
  "school_id": "1001"
}
```

**响应格式**：

```json
{
  "success": true,
  "message": "删除成功"
}
```

#### POST /upload_logo
上传Logo图片

**请求体**：`multipart/form-data`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `logo` | file | 是 | Logo图片文件 |
| `available_id` | string | 是 | 学校ID |

**响应格式**：

```json
{
  "success": true,
  "file_path": "logo/1001.png",
  "logo_id": "1001"
}
```

### 滚动数据接口

#### GET /api/scrolling_data
获取滚动数据

**响应格式**：

```json
{
  "data": [
    {
      "学校ID": "31",
      "学校名称": "清华大学",
      "地址": "北京市海淀区",
      "类别": "综合类",
      "性质": "公办"
    }
  ],
  "position": 0
}
```

#### POST /api/scrolling_position
更新滚动位置

**请求体**：

```json
{
  "position": 5
}
```

**响应格式**：

```json
{
  "success": true
}
```

---

## 🗄️ 数据库结构

### universities 表（学校信息表）

| 字段名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| 学校ID | TEXT | 学校唯一标识（主键） | - |
| 学校名称 | TEXT | 学校全称 | - |
| 地址 | TEXT | 学校地址 | - |
| 类别 | TEXT | 学校类别（综合类/理工类/财经类等） | - |
| 性质 | TEXT | 办学性质（公办/民办） | - |
| 归属部门 | TEXT | 主管部门（教育部/省属等） | - |
| 标签 | TEXT | 特色标签（逗号分隔） | - |
| 建校时间 | TEXT | 建校年份 | - |
| 占地面积 | TEXT | 占地面积（亩） | - |
| 保研星级 | TEXT | 保研评级 | - |
| 博士点数量 | INTEGER | 博士点数量 | 0 |
| 硕士点数量 | INTEGER | 硕士点数量 | 0 |
| 国家重点学科数量 | INTEGER | 国家重点学科数量 | 0 |
| 软科综合排名 | TEXT | 软科中国大学排名 | - |
| 校友会综合排名 | TEXT | 校友会中国大学排名 | - |
| QS世界排名 | TEXT | QS世界大学排名 | - |
| US世界排名 | TEXT | US News世界大学排名 | - |
| 泰晤士排名 | TEXT | 泰晤士高等教育排名 | - |
| 人气值排名 | TEXT | 人气值排名 | - |
| 基本信息 | TEXT | 学校简介 | - |
| logo_path | TEXT | Logo文件路径 | - |

### users 表（用户账户表）

| 字段名 | 类型 | 说明 | 默认值 |
|--------|------|------|--------|
| username | TEXT | 用户名（主键） | - |
| password | TEXT | 密码（明文存储） | - |

---

## 📱 使用说明

### 搜索学校

1. 在首页搜索框中输入学校名称或ID
2. 系统会实时显示匹配结果（搜索建议）
3. 点击搜索建议项直接跳转到学校详情页
4. 或点击搜索按钮/按回车键进行搜索

### 查看学校详情

1. 通过搜索结果点击学校名称
2. 或直接访问 URL：`http://localhost:5000/university/<学校ID>`

### 登录系统

1. 点击页面右上角的"登录"按钮
2. 在登录弹窗中输入用户名和密码
3. 点击"登录"按钮完成登录

### 管理账户

1. 登录系统后，点击"账户管理"按钮
2. 在账户管理页面可以查看、添加、编辑、删除账户

### 管理学校

1. 登录系统后，点击"添加学校"按钮添加新学校
2. 在学校详情页点击"编辑"按钮修改学校信息
3. 在学校详情页点击"删除"按钮删除学校

### 上传Logo

1. 在添加或编辑学校页面
2. 点击Logo上传区域选择图片文件
3. 系统自动保存并显示预览

---

## 🔒 默认账户

系统预置了管理员账户：

| 用户名 | 密码 | 权限 |
|--------|------|------|
| admin | admin | 管理员 |

> ⚠️ **安全提醒**：建议在生产环境中修改默认密码，避免使用弱密码。

---

## 🐳 Docker 部署

### 基础部署

```bash
# 构建镜像
docker build -t school-management .

# 运行容器（后台模式）
docker run -d \
  --name school-management-system \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DB_PATH=/app/data/school.db \
  -v school-data:/app/data \
  --restart unless-stopped \
  school-management
```

### Docker Compose 部署

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps
```

### Docker Compose 配置说明

```yaml
version: '3.8'

services:
  school-management:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: school-management-system
    ports:
      - "5000:5000"
    volumes:
      # 使用命名卷持久化数据库
      - school-data:/app/data
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=false
      - DB_PATH=/app/data/school.db
      - HOST=0.0.0.0
      - PORT=5000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  school-data:
    driver: local
```

### 健康检查

容器配置了健康检查，每30秒检查一次服务状态：

- 检查地址：`http://localhost:5000/`
- 超时时间：10秒
- 重试次数：3次
- 启动等待：40秒

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 贡献流程

1. **Fork** 本仓库到你的GitHub账户
2. **克隆** 你的Fork到本地：
   ```bash
   git clone https://github.com/your-username/school-management.git
   cd school-management
   ```
3. **创建分支**：
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **修改代码**并提交：
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```
5. **推送分支**：
   ```bash
   git push origin feature/your-feature-name
   ```
6. **创建 Pull Request**：在GitHub上创建PR

### 代码规范

- Python代码遵循PEP 8规范
- 使用4空格缩进
- 变量命名使用下划线命名法（snake_case）
- 函数和方法使用清晰的文档注释
- 提交信息使用英文或中文，描述清晰

---

## 📄 许可证

MIT License

```
MIT License

Copyright (c) 2026 School Management System

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
```

---

## 📧 联系方式

如有问题或建议，请通过以下方式联系：

- **GitHub Issues**：提交Issue到本仓库
- **邮件**：your-email@example.com

---

## 📊 项目状态

![项目状态](https://img.shields.io/badge/status-stable-green.svg)
![Python版本](https://img.shields.io/badge/python-3.10+-blue.svg)
![Flask版本](https://img.shields.io/badge/flask-2.0+-yellow.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)

---

*最后更新: 2026年4月*

---