"""
系统架构说明 / System Architecture Documentation
推栏消息推送原型示意 / Push Notification Prototype Schematic
"""

# ============================================================
# 系统架构 / System Architecture
# ============================================================

"""
推栏消息推送系统采用订阅/发布模式，支持广播和定向消息推送。

The Push Notification System uses a pub/sub pattern, supporting both 
broadcast and targeted message delivery.

## 核心组件 / Core Components

1. 推送服务 (PushService)
   - 提供HTTP API接口
   - 管理消息队列和订阅者
   - 处理消息分发逻辑

2. 消息队列 (MessageQueue)
   - 按优先级存储消息
   - 支持广播和定向消息
   - 自动排序和管理

3. 订阅者管理器 (SubscriberManager)
   - 管理客户端订阅
   - 心跳检测
   - 自动清理不活跃订阅者

4. 消息对象 (Message)
   - 唯一ID标识
   - 支持多种类型（文本、JSON、二进制）
   - 优先级支持

5. 订阅者对象 (Subscriber)
   - 唯一ID标识
   - 标签分类
   - 心跳状态追踪

## 数据流 / Data Flow

┌─────────────┐                      ┌─────────────┐
│  客户端A    │                      │  客户端B    │
│  Client A   │                      │  Client B   │
└──────┬──────┘                      └──────┬──────┘
       │                                    │
       │ 1. 订阅 / Subscribe                │
       ├────────────────────────────────────┤
       │                                    │
       ▼                                    ▼
┌──────────────────────────────────────────────────┐
│           推送服务 / Push Service                │
│  ┌────────────────────────────────────────────┐ │
│  │  订阅者管理器 / Subscriber Manager         │ │
│  │  ┌──────────┐  ┌──────────┐               │ │
│  │  │ 客户端A  │  │ 客户端B  │               │ │
│  │  └──────────┘  └──────────┘               │ │
│  └────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────┐ │
│  │  消息队列 / Message Queue                  │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐     │ │
│  │  │ 消息1   │ │ 消息2   │ │ 消息3   │     │ │
│  │  │ (优先级5)│ │ (优先级3)│ │ (优先级1)│    │ │
│  │  └─────────┘ └─────────┘ └─────────┘     │ │
│  └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
       │                                    │
       │ 2. 推送消息 / Push Message          │
       ◄────────────────────────────────────┤
       │                                    │
       │ 3. 拉取消息 / Pull Messages         │
       ├────────────────────────────────────►
       │                                    │
       ▼                                    ▼

## 消息优先级处理 / Message Priority Handling

消息按优先级（1-5）排序，5为最高优先级。
Messages are sorted by priority (1-5), with 5 being highest.

高优先级消息优先发送：
High priority messages are sent first:

    优先级5 ───► 立即处理 / Immediate processing
    优先级4 ───► 高优先级 / High priority
    优先级3 ───► 中等优先级 / Medium priority
    优先级2 ───► 低优先级 / Low priority
    优先级1 ───► 最低优先级 / Lowest priority

## 消息类型 / Message Types

1. 文本消息 (text)
   - 简单文本内容
   - 最常用类型

2. JSON消息 (json)
   - 结构化数据
   - 支持复杂对象

3. 二进制消息 (binary)
   - 任意二进制数据
   - 支持文件传输

## API端点 / API Endpoints

GET  /api/status         - 服务状态查询
POST /api/subscribe      - 订阅服务
POST /api/unsubscribe    - 取消订阅
POST /api/push           - 推送消息
POST /api/pull           - 拉取消息
POST /api/heartbeat      - 心跳检测
GET  /api/subscribers    - 订阅者列表

## 使用场景 / Use Cases

1. 实时通知系统
   - 系统告警
   - 用户通知
   - 事件提醒

2. 聊天系统
   - 消息分发
   - 群组广播
   - 私聊消息

3. 数据同步
   - 状态更新
   - 配置分发
   - 数据推送

4. 监控告警
   - 服务监控
   - 性能告警
   - 异常通知

## 扩展建议 / Extension Recommendations

1. 持久化存储
   - 使用Redis存储消息队列
   - 使用数据库存储订阅者信息
   - 消息历史记录

2. WebSocket支持
   - 实时双向通信
   - 减少轮询开销
   - 提高实时性

3. 认证授权
   - Token认证
   - 订阅者权限管理
   - 消息加密

4. 负载均衡
   - 多实例部署
   - 消息路由
   - 高可用架构

5. 监控统计
   - 消息吞吐量
   - 订阅者活跃度
   - 系统性能指标
"""
