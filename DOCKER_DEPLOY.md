# Docker 部署指南

## 项目文件说明

已创建以下 Docker 相关文件：

1. **Dockerfile** - Docker 镜像构建配置
2. **docker-compose.yml** - Docker Compose 配置（推荐）
3. **.dockerignore** - 排除不需要的文件

## 部署步骤

### 方法一：使用 Docker Compose（推荐）

1. **将项目文件复制到 Linux 服务器**
   ```bash
   # 在 Windows 上打包项目
   zip -r school-management.zip school\ 2.1/
   
   # 上传到 Linux 服务器并解压
   unzip school-management.zip
   cd school\ 2.1
   ```

2. **创建数据目录**
   ```bash
   mkdir -p data
   ```

3. **构建并启动容器**
   ```bash
   docker-compose up -d
   ```

4. **查看日志**
   ```bash
   docker-compose logs -f
   ```

5. **停止服务**
   ```bash
   docker-compose down
   ```

### 方法二：使用 Docker 命令

1. **构建镜像**
   ```bash
   docker build -t school-management:latest .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     --name school-management \
     -p 5000:5000 \
     -v $(pwd)/data:/app/data \
     -e DB_PATH=/app/data/school.db \
     school-management:latest
   ```

3. **查看日志**
   ```bash
   docker logs -f school-management
   ```

4. **停止容器**
   ```bash
   docker stop school-management
   docker rm school-management
   ```

## 访问应用

部署完成后，通过浏览器访问：
- 本地访问：`http://localhost:5000`
- 远程访问：`http://<服务器IP>:5000`

## 数据持久化

- 数据库文件会保存在 `./data/` 目录中
- 即使容器被删除，数据也不会丢失
- 重新启动容器时会自动加载已有数据

## 环境变量配置

可以通过以下环境变量自定义配置：

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `PORT` | 5000 | 服务端口 |
| `HOST` | 0.0.0.0 | 绑定地址 |
| `FLASK_DEBUG` | False | 调试模式 |
| `DB_PATH` | school.db | 数据库路径 |

## 常用命令

```bash
# 查看运行中的容器
docker ps

# 进入容器内部
docker exec -it school-management bash

# 重启容器
docker restart school-management

# 更新镜像后重新部署
docker-compose down
docker-compose up -d --build
```

## 注意事项

1. **端口冲突**：确保 5000 端口未被其他服务占用
2. **防火墙**：确保服务器防火墙允许 5000 端口访问
3. **数据备份**：定期备份 `./data/` 目录中的数据库文件
