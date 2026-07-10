# Trip Planner 智能旅行助手

基于 HelloAgents 多智能体框架的 AI 旅行规划助手，输入城市和日期，自动生成带景点、天气、酒店、餐饮和预算的完整旅行计划。

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | FastAPI + HelloAgents + Pydantic |
| 前端 | Vue 3 + TypeScript + Ant Design Vue + Vite |
| 地图 | 高德地图 MCP (POI/天气/路线) |
| 图片 | Unsplash API |
| LLM | 任意 OpenAI 兼容模型 |

## 快速开始

### 1. 后端

```bash
cd backend
cp .env.example .env        # 编辑 .env 填入你的 API Key
pip install -r requirements.txt
python run.py               # 启动 → http://localhost:8000
```

### 2. 前端

```bash
cd frontend
cp .env.example .env        # 编辑 .env 填入前端配置
npm install
npm run dev                 # 启动 → http://localhost:5173
```

### 3. 使用

打开 http://localhost:5173 → 填写城市、日期、偏好 → 生成旅行计划

## 项目结构

```
backend/
├── app/
│   ├── config.py              # 配置管理
│   ├── models/schemas.py      # Pydantic 数据模型
│   ├── agents/
│   │   └── trip_planner_agent.py  # 多 Agent 流水线
│   ├── services/
│   │   ├── llm_service.py     # LLM 服务
│   │   ├── amap_service.py    # 高德 MCP 服务
│   │   └── unsplash_service.py # 图片服务
│   └── api/
│       ├── main.py            # FastAPI 应用
│       └── routes/            # API 路由
└── tests/                     # 单元测试

frontend/
├── src/
│   ├── views/
│   │   ├── Home.vue           # 输入页
│   │   └── Result.vue         # 结果页
│   ├── services/api.ts        # HTTP 客户端
│   └── types/index.ts         # 类型定义
└── ...
```

## 环境变量

后端 `.env`：
```
LLM_MODEL_ID=your-model        # 模型名称
LLM_API_KEY=your-key           # API 密钥
LLM_BASE_URL=your-url          # API 地址
AMAP_API_KEY=your-key          # 高德地图 Key
UNSPLASH_ACCESS_KEY=your-key   # Unsplash Key（可选）
```

前端 `.env`：
```
VITE_API_BASE_URL=http://localhost:8000
VITE_AMAP_WEB_JS_KEY=your-key  # 高德 JS API Key
```

## 运行测试

```bash
cd backend
pytest tests/ -v
```
