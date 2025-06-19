# README.md
# FastAPI JWT Starter

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动服务
```bash
uvicorn main:app --reload
```

### 访问接口
- POST /register 创建用户
- POST /login 获取 token
- GET /me 带 Bearer Token 访问用户信息
