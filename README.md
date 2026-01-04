# 推栏消息推送系统 / Push Notification System

一个轻量级的消息推送原型系统，支持订阅/发布模式的消息分发。

A lightweight message push notification prototype system supporting pub/sub pattern message distribution.

## 功能特性 / Features

- ✅ **订阅管理** / Subscription Management - 支持客户端注册、注销和状态管理
- ✅ **消息队列** / Message Queue - 优先级队列，支持消息排序和管理
- ✅ **广播推送** / Broadcast Push - 支持向所有订阅者广播消息
- ✅ **定向推送** / Targeted Push - 支持向特定订阅者推送消息
- ✅ **心跳检测** / Heartbeat Detection - 自动检测和清理不活跃的订阅者
- ✅ **多种消息类型** / Multiple Message Types - 支持文本、JSON、二进制消息
- ✅ **优先级支持** / Priority Support - 消息优先级队列处理

## 系统架构 / System Architecture

```
┌─────────────────┐
│   客户端/Client  │
│   (订阅者)       │
└────────┬────────┘
         │ HTTP API
         │
┌────────▼────────────────────────┐
│   推送服务/Push Service          │
│  ┌──────────────────────────┐  │
│  │  订阅管理器              │  │
│  │  Subscriber Manager      │  │
│  └──────────────────────────┘  │
│  ┌──────────────────────────┐  │
│  │  消息队列                │  │
│  │  Message Queue           │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
```

## 快速开始 / Quick Start

### 1. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 启动服务 / Start Service

```bash
python push_service.py
```

服务将在 `http://127.0.0.1:5000` 启动

Service will start at `http://127.0.0.1:5000`

### 3. 运行演示 / Run Demo

在另一个终端窗口运行演示客户端：

Run the demo client in another terminal window:

```bash
python demo_client.py
```

## API 文档 / API Documentation

### 1. 查看服务状态 / Check Service Status

```http
GET /api/status
```

响应示例 / Response Example:
```json
{
  "status": "running",
  "queue_size": 5,
  "active_subscribers": 3,
  "total_subscribers": 3,
  "stats": {
    "messages_sent": 10,
    "messages_failed": 0,
    "total_messages": 10
  }
}
```

### 2. 订阅服务 / Subscribe

```http
POST /api/subscribe
Content-Type: application/json

{
  "subscriber_id": "client_001",
  "name": "客户端1",
  "tags": ["mobile", "ios"]
}
```

响应示例 / Response Example:
```json
{
  "message": "订阅成功",
  "subscriber": {
    "id": "client_001",
    "name": "客户端1",
    "tags": ["mobile", "ios"],
    "connected_at": "2026-01-04T08:00:00.000000",
    "is_active": true
  }
}
```

### 3. 推送消息 / Push Message

```http
POST /api/push
Content-Type: application/json

{
  "content": "Hello World!",
  "type": "text",
  "priority": 5,
  "target": null
}
```

参数说明 / Parameters:
- `content`: 消息内容 / Message content (required)
- `type`: 消息类型 / Message type - text, json, binary (default: text)
- `priority`: 优先级 / Priority - 1-5, 5为最高 (default: 1)
- `target`: 目标订阅者ID / Target subscriber ID (null for broadcast)

响应示例 / Response Example:
```json
{
  "message": "消息已加入队列",
  "message_id": "550e8400-e29b-41d4-a716-446655440000",
  "details": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "content": "Hello World!",
    "type": "text",
    "priority": 5,
    "target": null,
    "timestamp": "2026-01-04T08:00:00.000000",
    "status": "pending"
  }
}
```

### 4. 拉取消息 / Pull Messages

```http
POST /api/pull
Content-Type: application/json

{
  "subscriber_id": "client_001"
}
```

响应示例 / Response Example:
```json
{
  "subscriber_id": "client_001",
  "count": 2,
  "messages": [
    {
      "id": "msg_001",
      "content": "Hello World!",
      "type": "text",
      "priority": 5,
      "timestamp": "2026-01-04T08:00:00.000000"
    }
  ]
}
```

### 5. 发送心跳 / Send Heartbeat

```http
POST /api/heartbeat
Content-Type: application/json

{
  "subscriber_id": "client_001"
}
```

### 6. 取消订阅 / Unsubscribe

```http
POST /api/unsubscribe
Content-Type: application/json

{
  "subscriber_id": "client_001"
}
```

### 7. 列出订阅者 / List Subscribers

```http
GET /api/subscribers?active_only=true
```

## 使用示例 / Usage Examples

### Python 客户端示例 / Python Client Example

```python
from demo_client import PushClient

# 创建客户端 / Create client
client = PushClient(subscriber_id="my_client")

# 订阅服务 / Subscribe
client.subscribe(name="我的客户端", tags=["python", "demo"])

# 推送消息 / Push message
client.push("Hello, World!", priority=3)

# 拉取消息 / Pull messages
messages = client.pull()
for msg in messages:
    print(f"收到消息: {msg['content']}")

# 取消订阅 / Unsubscribe
client.unsubscribe()
```

### cURL 示例 / cURL Example

```bash
# 订阅 / Subscribe
curl -X POST http://127.0.0.1:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"subscriber_id":"curl_client","name":"cURL客户端"}'

# 推送消息 / Push message
curl -X POST http://127.0.0.1:5000/api/push \
  -H "Content-Type: application/json" \
  -d '{"content":"测试消息","type":"text","priority":5}'

# 拉取消息 / Pull messages
curl -X POST http://127.0.0.1:5000/api/pull \
  -H "Content-Type: application/json" \
  -d '{"subscriber_id":"curl_client"}'
```

## 配置说明 / Configuration

编辑 `config.py` 文件修改配置：

Edit `config.py` to modify configuration:

```python
class Config:
    HOST = '127.0.0.1'          # 服务器地址 / Server host
    PORT = 5000                  # 端口号 / Port number
    DEBUG = True                 # 调试模式 / Debug mode
    MAX_QUEUE_SIZE = 1000        # 最大队列大小 / Max queue size
    MAX_SUBSCRIBERS = 100        # 最大订阅者数 / Max subscribers
    MESSAGE_RETENTION_TIME = 3600  # 消息保留时间(秒) / Message retention (seconds)
    HEARTBEAT_INTERVAL = 30      # 心跳间隔(秒) / Heartbeat interval (seconds)
```

## 项目结构 / Project Structure

```
tl_msgpush/
├── config.py           # 配置文件 / Configuration file
├── message.py          # 消息和队列模块 / Message and queue module
├── subscriber.py       # 订阅者管理模块 / Subscriber management module
├── push_service.py     # 推送服务主程序 / Push service main program
├── demo_client.py      # 演示客户端 / Demo client
├── requirements.txt    # Python依赖 / Python dependencies
└── README.md          # 项目文档 / Project documentation
```

## 核心概念 / Core Concepts

### 订阅者 / Subscriber
订阅者是消息的接收者，每个订阅者有唯一的ID，可以接收广播消息或定向消息。

Subscribers are message receivers. Each subscriber has a unique ID and can receive broadcast or targeted messages.

### 消息队列 / Message Queue
消息队列按优先级和时间戳排序存储待发送的消息。高优先级消息优先处理。

Message queue stores pending messages sorted by priority and timestamp. Higher priority messages are processed first.

### 心跳机制 / Heartbeat Mechanism
客户端需要定期发送心跳以保持连接状态。长时间未发送心跳的订阅者将被系统清理。

Clients need to send heartbeats periodically to maintain connection status. Subscribers that haven't sent heartbeats will be cleaned up.

### 推送模式 / Push Modes
- **广播推送** / Broadcast Push: target=null，所有订阅者都会收到
- **定向推送** / Targeted Push: target=subscriber_id，只有指定订阅者收到

## 注意事项 / Notes

- 这是一个原型系统，适用于演示和学习，不建议直接用于生产环境
- 消息存储在内存中，服务重启后消息会丢失
- 建议在生产环境中使用持久化存储（如Redis、RabbitMQ等）

- This is a prototype system suitable for demonstration and learning, not recommended for production use
- Messages are stored in memory and will be lost on service restart
- Recommended to use persistent storage (e.g., Redis, RabbitMQ) in production

## 许可证 / License

MIT License

## 贡献 / Contributing

欢迎提交问题和拉取请求！

Issues and pull requests are welcome!